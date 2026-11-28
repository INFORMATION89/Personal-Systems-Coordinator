# ChatGPT Free — Session Starter

**Scope:** contributors using the free ChatGPT plan with GitHub repository access on PSC.
**Status:** optional supplement; it does not make ChatGPT or any model mandatory.
**Last reviewed:** 2026-11-28 · adapted from INFORMATION89/Meridian-Engine
**Authority:** `AGENTS.md`, `RULES.md`, `AI_POLICY.md`, `AI_COST_POLICY.md` and `docs/RESEARCH_PLAN.md` §7 remain authoritative.

## Why this exists

ChatGPT Free can open branches, push commits and open pull requests. Experience on the Meridian repository showed avoidable problems: many tiny commits for one change, CI-skip markers on code commits, hand-edited generated files, PRs stacked on unmerged branches, and abandoned branches. The rules below prevent them; `.github/workflows/pr-hygiene.yml` enforces two.

## Starter prompt

Paste this at the start of every session, filling in the task:

```text
You are working on the Personal-Systems-Coordinator repository (INFORMATION89/Personal-Systems-Coordinator).
Before doing anything, read AGENTS.md, then docs/RESEARCH_PLAN.md section 7.

Your task is: <TASK, e.g. a tier F or H item from section 7>. Do only this task. If it is assigned to
tier O or S, stop and tell me instead of doing it.

Rules:
1. Work on one new branch from the current main unless the task names another base.
   Never push to main. Never merge a PR.
2. Plan the whole change first, then push it in as few commits as possible (normally 1-3).
3. Never use [skip ci] or another CI-skip marker on a commit that changes anything other than
   documentation (*.md, docs/).
4. Do not change decisions in docs/DECISIONS.md, the research plan's scope, CI workflows or
   policies unless the task explicitly says so.
5. Do not add claims about provider behaviour without an official source and date; label anything
   else as community, inference or untested.
6. Never paste, print or commit secrets, tokens, personal data or precise personal locations.
7. Open the PR with .github/pull_request_template.md and fill in every section, including
   "Tool and tier: ChatGPT Free, tier F".
8. If CI fails, find the cause before pushing again. After two failed fixes, stop and report.
9. Finish with a short handoff: branch, commit SHA, what changed, checks run, what is not verified.
```

## Tasks it may take

Tier F tasks in `docs/RESEARCH_PLAN.md` §7, plus tier H tasks when Haiku is not in use. Tier S only when the owner assigns it explicitly. Never tier O.
