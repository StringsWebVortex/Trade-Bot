#!/usr/bin/env python3
"""GOV-067 — hand a failing or reviewed pull request to ChatGPT Codex.

Claude opens a pull request and then leaves it alone. From that point Codex
(the ChatGPT Codex GitHub integration) owns it until it merges: Codex code
review reviews every push, and this script asks Codex to fix what stands
between the pull request and a green merge queue entry:

  ci      a watched workflow failed on the pull request's current head
  review  Codex's own review on the current head left inline findings

The request is a pull-request comment that mentions `@codex`. Codex acts on a
mention from a person with Codex access, so the comment is posted with the
owner's token (CODEX_HANDOFF_TOKEN), not with GITHUB_TOKEN.

Three guards keep this from becoming a loop that spends the owner's plan:

  - one request per (kind, head SHA): a second failing workflow on the same
    head does not ask again;
  - a stale event is ignored: if the head moved, a newer run will report;
  - at most MAX_REQUESTS requests per pull request, then one notice saying a
    person is needed, and nothing after that.

The workflow runs this file from the default branch, never from the pull
request, so a pull request cannot change the code that holds the token.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

API_ROOT = "https://api.github.com"
CODEX_LOGIN = "chatgpt-codex-connector[bot]"
WATCHED_WORKFLOWS = frozenset({"CI", "CodeQL", "Security", "Workflow lint"})
MAX_REQUESTS = 5
MARKER_PREFIX = "<!-- codex-handoff"
LIMIT_MARKER = "<!-- codex-handoff limit -->"
TOKEN_ENV = "CODEX_HANDOFF_TOKEN"


@dataclass(frozen=True)
class Trigger:
    kind: str  # "ci" or "review"
    pr: int
    head_sha: str
    detail: str
    url: str
    review_id: int | None = None


def marker(trigger: Trigger) -> str:
    return f"{MARKER_PREFIX} kind={trigger.kind} sha={trigger.head_sha} -->"


def trigger_from_event(name: str, event: Mapping[str, Any], repo: str) -> Trigger | None:
    """The handoff this event asks for, or None when it asks for nothing."""
    if name == "workflow_run":
        run = event.get("workflow_run") or {}
        if run.get("event") != "pull_request" or run.get("conclusion") != "failure":
            return None
        if run.get("name") not in WATCHED_WORKFLOWS:
            return None
        # A fork's run lists no pull requests and gets no secrets anyway.
        if (run.get("head_repository") or {}).get("full_name") != repo:
            return None
        pulls = run.get("pull_requests") or []
        if not pulls:
            return None
        return Trigger(
            kind="ci",
            pr=int(pulls[0]["number"]),
            head_sha=str(run["head_sha"]),
            detail=str(run["name"]),
            url=str(run.get("html_url") or ""),
        )
    if name == "pull_request_review":
        review = event.get("review") or {}
        pull = event.get("pull_request") or {}
        if (review.get("user") or {}).get("login") != CODEX_LOGIN:
            return None
        if ((pull.get("head") or {}).get("repo") or {}).get("full_name") != repo:
            return None
        return Trigger(
            kind="review",
            pr=int(pull["number"]),
            head_sha=str(review.get("commit_id") or pull["head"]["sha"]),
            detail="Codex review",
            url=str(review.get("html_url") or ""),
            review_id=int(review["id"]),
        )
    return None


def request_body(trigger: Trigger, number: int) -> str:
    if trigger.kind == "ci":
        ask = (
            f"@codex fix the failing CI on this pull request. The `{trigger.detail}` "
            f"workflow failed on head `{trigger.head_sha}` ({trigger.url})."
        )
    else:
        ask = (
            "@codex fix the P0 and P1 findings from your review of head "
            f"`{trigger.head_sha}` ({trigger.url})."
        )
    return (
        f"{ask}\n\n"
        'Follow AGENTS.md, including "Pull request handoff": find the cause, make the '
        "smallest fix inside this pull request's scope, keep the quality registry and "
        "generated docs in step, and push to this branch.\n\n"
        f"Automated handoff request {number} of {MAX_REQUESTS}.\n\n"
        f"{marker(trigger)}"
    )


def limit_body() -> str:
    return (
        f"Automated Codex handoff stopped after {MAX_REQUESTS} requests on this pull "
        "request. A person needs to look at it; comment `@codex` yourself to continue."
        f"\n\n{LIMIT_MARKER}"
    )


def decide(trigger: Trigger, pull: Mapping[str, Any], comments: list[str]) -> str | None:
    """The comment to post, or None when nothing should be posted."""
    if pull.get("state") != "open" or pull.get("merged") or pull.get("draft"):
        return None
    # Bot-authored pull requests (Dependabot and the like) are not handed off.
    if (pull.get("user") or {}).get("type") == "Bot":
        return None
    if (pull.get("head") or {}).get("sha") != trigger.head_sha:
        return None
    if any(marker(trigger) in body for body in comments):
        return None
    requests = [body for body in comments if MARKER_PREFIX in body and LIMIT_MARKER not in body]
    if len(requests) >= MAX_REQUESTS:
        if any(LIMIT_MARKER in body for body in comments):
            return None
        return limit_body()
    return request_body(trigger, len(requests) + 1)


Opener = Callable[[urllib.request.Request], Any]


class GitHub:
    def __init__(self, token: str, repo: str, opener: Opener | None = None) -> None:
        self._token = token
        self._repo = repo
        self._open = opener or (lambda request: urllib.request.urlopen(request, timeout=30))

    def _call(self, method: str, path: str, body: Mapping[str, Any] | None = None) -> Any:
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = urllib.request.Request(
            f"{API_ROOT}/repos/{self._repo}{path}", data=data, method=method
        )
        request.add_header("Authorization", f"Bearer {self._token}")
        request.add_header("Accept", "application/vnd.github+json")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")
        if data is not None:
            request.add_header("Content-Type", "application/json")
        with self._open(request) as response:
            return json.loads(response.read().decode("utf-8") or "null")

    def _pages(self, path: str) -> list[Any]:
        items: list[Any] = []
        page = 1
        while True:
            batch = self._call("GET", f"{path}?per_page=100&page={page}")
            items.extend(batch)
            if len(batch) < 100:
                return items
            page += 1

    def pull(self, number: int) -> dict[str, Any]:
        return self._call("GET", f"/pulls/{number}")

    def comment_bodies(self, number: int) -> list[str]:
        return [str(c.get("body") or "") for c in self._pages(f"/issues/{number}/comments")]

    def review_comment_count(self, number: int, review_id: int) -> int:
        return len(self._pages(f"/pulls/{number}/reviews/{review_id}/comments"))

    def post_comment(self, number: int, body: str) -> None:
        self._call("POST", f"/issues/{number}/comments", {"body": body})


def main(
    env: Mapping[str, str] | None = None,
    client: Callable[[str, str], GitHub] = GitHub,
) -> int:
    env = os.environ if env is None else env
    repo = env.get("GITHUB_REPOSITORY", "")
    event = json.loads(Path(env["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    trigger = trigger_from_event(env.get("GITHUB_EVENT_NAME", ""), event, repo)
    if trigger is None:
        print("No Codex handoff needed for this event.")
        return 0
    token = env.get(TOKEN_ENV, "").strip()
    if not token:
        # Fail loudly and change nothing: a GITHUB_TOKEN comment would come
        # from github-actions[bot], and Codex does not act on it.
        print(f"{TOKEN_ENV} is not set; no handoff request was posted.", file=sys.stderr)
        return 1
    github = client(token, repo)
    if trigger.review_id is not None:
        findings = github.review_comment_count(trigger.pr, trigger.review_id)
        if not findings:
            print(f"Codex review on #{trigger.pr} has no inline findings; nothing to fix.")
            return 0
    body = decide(trigger, github.pull(trigger.pr), github.comment_bodies(trigger.pr))
    if body is None:
        print(f"#{trigger.pr}: request already made, head moved, or pull request not open.")
        return 0
    github.post_comment(trigger.pr, body)
    print(f"#{trigger.pr}: posted Codex handoff ({trigger.kind}, {trigger.head_sha}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
