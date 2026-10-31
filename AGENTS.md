# Project Instructions (AGENTS.md)

## General Working Agreements

- Understand the existing project architecture before making changes.
- Follow the existing coding conventions and patterns.
- Prefer simple, maintainable, and readable solutions.
- Avoid unnecessary dependencies.
- Ask for confirmation before adding new production dependencies.
- Do not modify unrelated files.
- Do not introduce breaking changes without explicit approval.
- Keep security, performance, and accessibility in mind.

## Development Workflow

1. Inspect the relevant files before making changes.
2. Identify the root cause before implementing fixes.
3. Create a short implementation plan for complex tasks.
4. Implement changes in small, logical steps.
5. Run relevant tests after modifications.
6. Run linting and formatting checks when available.
7. Report modified files and explain important changes.

## Testing Requirements

- Run the relevant tests after changing code.
- Run `npm test` when applicable.
- Run `npm run lint` when available.
- Add tests for new functionality.
- Do not claim tests passed unless they were actually executed.
- Report existing failures separately from newly introduced failures.

## Code Quality

- Use clear and meaningful names.
- Avoid unnecessary code duplication.
- Follow separation of concerns.
- Handle errors explicitly.
- Validate external inputs.
- Avoid hardcoded secrets and credentials.
- Use environment variables for sensitive configuration.
- Keep functions focused and reasonably small.

## Security

- Never expose API keys, passwords, or tokens.
- Validate and sanitize untrusted inputs.
- Apply authentication and authorization checks where required.
- Avoid insecure database queries.
- Follow least-privilege principles.

## Documentation

- Update documentation when public behavior changes.
- Document new environment variables.
- Keep README instructions accurate.
- Explain important architectural decisions.

## Git Guidelines

- Do not overwrite user changes.
- Do not force-push.
- Do not delete branches or commits without permission.
- Keep changes focused and reviewable.

## Subagent Guidelines

- Use parallel subagents for independent exploration, testing, research, and code review when useful.
- Keep implementation ownership with the main agent unless tasks are safely independent.
- Ask read-only agents to inspect rather than modify files.
- Collect and summarize subagent findings before implementation.
- Avoid multiple agents editing the same files simultaneously.

## Final Response

After completing a task, report:

# Mandatory Autonomous Execution

## Instructions Loading

Before starting any task:

1. Read the complete applicable AGENTS.md instruction chain.
2. Read `.codex/IMPLEMENTATION.md`.
3. Follow the autonomous implementation protocol for all implementation assignments.

## Default Working Mode

Default to execution, not discussion.

When the user requests implementation, debugging, modification, integration, or completion:

- Investigate the repository.
- Implement the requested work.
- Complete all related in-scope requirements.
- Test and validate changes.
- Fix implementation-related failures.
- Continue until the task is complete or a genuine blocker prevents further progress.

Do not merely describe the next steps.

Do not transfer implementation responsibilities to the user.

Do not repeat instructions in conversational responses.

Do not stop after producing a plan.

Do not ask permission for normal, reversible implementation changes within the requested scope.

## Main Agent Responsibility

The main agent owns the assignment from beginning to end.

Subagents may investigate, review, research, or implement isolated tasks, but their reports are not a substitute for completed integration.

The main agent must collect results, resolve conflicts, integrate changes, test, and verify.

## Completion

Only report work that has actually been performed.

If some work remains feasible, implement it before responding.

If blocked, complete all independent work and report only the specific remaining blocker which you tried to deal but failed.


1. What was implemented.
2. Which files were modified.
3. Tests and validation performed.
4. Any remaining issues or limitations.
