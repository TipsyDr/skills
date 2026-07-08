---
name: agent-loop
description: Run long-running or multi-step Codex work as a durable agent loop with a done contract, file-backed state, progress log, rubric, and verification. Use when the user asks for sustained implementation, debugging, research, lesson work, documentation, product/MVP work, multi-agent coordination, resumable work, or any task likely to span many steps, sessions, context windows, or subjective quality judgments.
---

# Agent Loop

## Overview

Use a short, restartable loop for work that can drift, stall, or outlive the current context. The goal is to make state explicit, quality testable, and recovery easy.

## Start The Loop

1. Identify the workspace state source.
   - Prefer an existing project note, issue, plan, test output, or repo guidance if present.
   - If no durable state exists and the task is substantial, create a small loop folder near the work, such as `.agent-loop/` in a repo or `work/agent-loop/` in a projectless thread.
   - Do not create loop files for tiny one-shot tasks.

2. Establish the done contract.
   - Write or update `contract.md` when the task is large enough to resume later.
   - Include observable acceptance checks, explicit non-goals, and any user constraints.
   - If the user already gave clear acceptance criteria, preserve their wording.
   - If the contract is uncertain, infer a conservative version and proceed unless the uncertainty is risky.

3. Record current state.
   - Write or update `progress.md` with: objective, current step, next action, blockers, touched files, verification status.
   - Keep it short enough that a future agent can recover in under a minute.

4. Define quality scoring when taste matters.
   - Write or update `rubric.md` for subjective outputs such as design, product ideas, writing, documentation, lesson quality, or UX.
   - Use 3-5 axes with simple 0-2 or 0-3 scoring.
   - Include concrete examples of good and bad when helpful.

## Run The Loop

Use this cycle until the done contract is met:

1. Plan the next smallest useful move.
2. Act by editing, researching, testing, or producing the next artifact.
3. Verify with concrete evidence: tests, lint, screenshots, rendered files, source citations, output inspection, or a rubric score.
4. Record the result in `log.md` or the project-native log.
5. Update `progress.md` with the next action.

Prefer deleting or simplifying loop machinery when it stops carrying useful state. The loop should make work clearer, not heavier.

## Role Separation

Separate these roles mentally, and use actual subagents only when the task benefits from independent work:

- Planner: converts the user request into the contract and next actions.
- Builder: changes files or produces artifacts.
- Evaluator: reads diffs, runs checks, scores subjective quality, and looks for failure modes.

Do not let the builder be the only evaluator on risky or subjective work. If using subagents, give each one a narrow task and explicit output expectations.

## File Conventions

Use these files only when they add value:

```text
.agent-loop/
  contract.md
  progress.md
  rubric.md
  log.md
  traces/
```

For projectless chats, prefer `work/agent-loop/` for intermediate files. Put user-facing deliverables in the thread's `outputs/` folder when the environment specifies one.

Keep files append-friendly but readable. Use dates or short headings in `log.md`. Avoid dumping huge transcripts unless they are needed for debugging; store only the important trace pointer or excerpt.

## Stop Conditions

Stop when:

- The done contract is satisfied.
- Verification has passed or any unrun verification is clearly reported.
- `progress.md` says there is no remaining required action.
- The final response names the result, evidence, and any residual risk.

If blocked, write the blocking condition, attempted paths, and the exact user or external input needed.
