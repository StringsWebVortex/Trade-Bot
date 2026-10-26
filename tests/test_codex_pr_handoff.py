"""
Claude opens a pull request; ChatGPT Codex carries it to the merge queue.

These tests pin what the handoff may do: ask Codex once per failing head or
per Codex review with findings, ignore stale and foreign events, stop after a
fixed number of requests, and never run the pull request's own code with the
owner's token.

Decides:
  - GOV-067 — A pull request Claude opened is handed to ChatGPT Codex, once per head, with a hard cap
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
import yaml

from scripts import codex_pr_handoff as handoff

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = PROJECT_ROOT / ".github" / "workflows" / "codex-pr-handoff.yml"
REPO = "owner/repo"
SHA = "a" * 40


def _run_event(**overrides) -> dict:
    run = {
        "name": "CI",
        "event": "pull_request",
        "conclusion": "failure",
        "head_sha": SHA,
        "html_url": "https://github.com/owner/repo/actions/runs/1",
        "head_repository": {"full_name": REPO},
        "pull_requests": [{"number": 7}],
    }
    run.update(overrides)
    return {"workflow_run": run}


def _review_event(login: str = handoff.CODEX_LOGIN, head_repo: str = REPO) -> dict:
    return {
        "review": {
            "id": 99,
            "user": {"login": login},
            "commit_id": SHA,
            "html_url": "https://github.com/owner/repo/pull/7#pullrequestreview-99",
        },
        "pull_request": {"number": 7, "head": {"sha": SHA, "repo": {"full_name": head_repo}}},
    }


def _pull(**overrides) -> dict:
    pull = {"state": "open", "merged": False, "draft": False, "head": {"sha": SHA}}
    pull.update(overrides)
    return pull


CI = handoff.Trigger("ci", 7, SHA, "CI", "https://example.invalid/run")


class TestTrigger:
    def test_a_failed_pull_request_run_asks_for_a_ci_fix(self):
        trigger = handoff.trigger_from_event("workflow_run", _run_event(), REPO)
        assert trigger == handoff.Trigger(
            "ci", 7, SHA, "CI", "https://github.com/owner/repo/actions/runs/1"
        )

    @pytest.mark.parametrize(
        "overrides",
        [
            {"conclusion": "success"},
            {"conclusion": "cancelled"},
            {"event": "push"},
            {"event": "merge_group"},
            {"name": "Deploy"},
            {"head_repository": {"full_name": "fork/repo"}},
            {"pull_requests": []},
        ],
    )
    def test_other_runs_ask_for_nothing(self, overrides):
        assert handoff.trigger_from_event("workflow_run", _run_event(**overrides), REPO) is None

    def test_a_codex_review_asks_for_a_review_fix(self):
        trigger = handoff.trigger_from_event("pull_request_review", _review_event(), REPO)
        assert trigger is not None
        assert (trigger.kind, trigger.pr, trigger.head_sha, trigger.review_id) == (
            "review",
            7,
            SHA,
            99,
        )

    @pytest.mark.parametrize(
        "event",
        [_review_event(login="someone"), _review_event(head_repo="fork/repo")],
        ids=["human-review", "fork-head"],
    )
    def test_other_reviews_ask_for_nothing(self, event):
        assert handoff.trigger_from_event("pull_request_review", event, REPO) is None

    def test_an_unknown_event_asks_for_nothing(self):
        assert handoff.trigger_from_event("push", {}, REPO) is None


class TestDecide:
    def test_the_first_request_mentions_codex_and_carries_its_marker(self):
        body = handoff.decide(CI, _pull(), [])
        assert body is not None
        assert body.startswith("@codex fix the failing CI")
        assert handoff.marker(CI) in body
        assert f"request 1 of {handoff.MAX_REQUESTS}" in body

    def test_a_review_request_names_the_findings(self):
        review = handoff.Trigger("review", 7, SHA, "Codex review", "u", review_id=1)
        body = handoff.decide(review, _pull(), [])
        assert body is not None
        assert body.startswith("@codex fix the P0 and P1 findings")

    @pytest.mark.parametrize(
        "pull",
        [
            _pull(state="closed"),
            _pull(merged=True),
            _pull(draft=True),
            _pull(head={"sha": "b" * 40}),
            _pull(user={"login": "dependabot[bot]", "type": "Bot"}),
        ],
        ids=["closed", "merged", "draft", "stale-head", "bot-author"],
    )
    def test_nothing_is_posted_on_a_pull_request_that_moved_on(self, pull):
        assert handoff.decide(CI, pull, []) is None

    def test_the_same_head_is_asked_about_once(self):
        assert handoff.decide(CI, _pull(), [handoff.request_body(CI, 1)]) is None

    def test_a_review_on_a_head_already_asked_about_for_ci_still_asks(self):
        review = handoff.Trigger("review", 7, SHA, "Codex review", "u", review_id=1)
        body = handoff.decide(review, _pull(), [handoff.request_body(CI, 1)])
        assert body is not None
        assert "request 2 of" in body

    def test_the_cap_posts_one_notice_and_then_nothing(self):
        earlier = [
            handoff.request_body(handoff.Trigger("ci", 7, str(n) * 40, "CI", "u"), n)
            for n in range(1, handoff.MAX_REQUESTS + 1)
        ]
        notice = handoff.decide(CI, _pull(), earlier)
        assert notice == handoff.limit_body()
        assert "@codex fix" not in notice
        assert handoff.decide(CI, _pull(), [*earlier, notice]) is None


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class TestGitHub:
    def test_requests_are_authenticated_and_paginated(self):
        seen = []
        pages = [[{"body": "x"}] * 100, [{"body": None}]]

        def opener(request):
            seen.append(request)
            payload = pages.pop(0) if "/comments" in request.full_url else {"state": "open"}
            return FakeResponse(json.dumps(payload).encode())

        github = handoff.GitHub("tok", REPO, opener)
        bodies = github.comment_bodies(7)
        assert len(bodies) == 101 and bodies[-1] == ""
        assert github.pull(7) == {"state": "open"}
        assert seen[0].get_header("Authorization") == "Bearer tok"
        assert seen[0].full_url.startswith(handoff.API_ROOT)
        assert seen[0].full_url.endswith("/repos/owner/repo/issues/7/comments?per_page=100&page=1")
        assert seen[1].full_url.endswith("page=2")

    def test_posting_sends_the_body_as_json(self):
        seen = []

        def opener(request):
            seen.append(request)
            return FakeResponse(b"{}")

        handoff.GitHub("tok", REPO, opener).post_comment(7, "hello")
        assert seen[0].get_method() == "POST"
        assert json.loads(seen[0].data) == {"body": "hello"}


class FakeClient:
    def __init__(self, findings: int = 1, comments: list[str] | None = None) -> None:
        self.findings = findings
        self.comments = comments or []
        self.posted: list[tuple[int, str]] = []

    def __call__(self, token: str, repo: str) -> FakeClient:
        assert (token, repo) == ("tok", REPO)
        return self

    def review_comment_count(self, number: int, review_id: int) -> int:
        return self.findings

    def pull(self, number: int) -> dict:
        return _pull()

    def comment_bodies(self, number: int) -> list[str]:
        return self.comments

    def post_comment(self, number: int, body: str) -> None:
        self.posted.append((number, body))


class TestMain:
    def _env(self, tmp_path, name: str, event: dict, token: str = "tok") -> dict:
        path = tmp_path / "event.json"
        path.write_text(json.dumps(event), encoding="utf-8")
        return {
            "GITHUB_REPOSITORY": REPO,
            "GITHUB_EVENT_PATH": str(path),
            "GITHUB_EVENT_NAME": name,
            handoff.TOKEN_ENV: token,
        }

    def test_a_failed_run_posts_one_request(self, tmp_path):
        client = FakeClient()
        env = self._env(tmp_path, "workflow_run", _run_event())
        assert handoff.main(env, client) == 0
        assert len(client.posted) == 1 and client.posted[0][0] == 7

    def test_an_irrelevant_event_needs_no_token(self, tmp_path):
        client = FakeClient()
        env = self._env(tmp_path, "workflow_run", _run_event(conclusion="success"), token="")
        assert handoff.main(env, client) == 0
        assert client.posted == []

    def test_a_missing_token_fails_and_posts_nothing(self, tmp_path):
        client = FakeClient()
        env = self._env(tmp_path, "workflow_run", _run_event(), token=" ")
        assert handoff.main(env, client) == 1
        assert client.posted == []

    def test_a_review_without_findings_posts_nothing(self, tmp_path):
        client = FakeClient(findings=0)
        env = self._env(tmp_path, "pull_request_review", _review_event())
        assert handoff.main(env, client) == 0
        assert client.posted == []

    def test_a_repeat_posts_nothing(self, tmp_path):
        client = FakeClient(comments=[handoff.request_body(CI, 1)])
        env = self._env(tmp_path, "workflow_run", _run_event())
        assert handoff.main(env, client) == 0
        assert client.posted == []


@pytest.fixture(scope="module")
def spec() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


class TestWorkflow:
    def test_it_watches_the_pull_request_workflows_and_codex_reviews(self, spec):
        triggers = spec.get("on") or spec.get(True)
        assert set(triggers["workflow_run"]["workflows"]) == handoff.WATCHED_WORKFLOWS
        assert triggers["workflow_run"]["types"] == ["completed"]
        assert triggers["pull_request_review"]["types"] == ["submitted"]
        # Not a gating workflow: it must never report a check on the pull request.
        assert "pull_request" not in triggers
        assert "pull_request_target" not in triggers

    def test_the_token_never_meets_pull_request_code(self, spec):
        steps = spec["jobs"]["handoff"]["steps"]
        checkout = steps[0]
        assert checkout["with"]["ref"] == "${{ github.event.repository.default_branch }}"
        assert checkout["with"]["persist-credentials"] is False
        assert steps[-1]["env"] == {"CODEX_HANDOFF_TOKEN": "${{ secrets.CODEX_HANDOFF_TOKEN }}"}

    def test_dependabot_runs_are_filtered_before_the_job_starts(self, spec):
        condition = spec["jobs"]["handoff"]["if"]
        assert "github.event.workflow_run.actor.login != 'dependabot[bot]'" in condition

    def test_it_is_read_only_and_serial_per_pull_request(self, spec):
        assert spec["permissions"] == {"contents": "read"}
        assert spec["jobs"]["handoff"]["permissions"] == {"contents": "read"}
        assert spec["concurrency"]["cancel-in-progress"] is False

    def test_it_never_merges_or_arms_auto_merge(self):
        script = Path(handoff.__file__).read_text(encoding="utf-8")
        text = WORKFLOW.read_text(encoding="utf-8") + script
        for forbidden in ("/merge", "enablePullRequestAutoMerge", "--auto", "gh pr merge"):
            assert forbidden not in text
