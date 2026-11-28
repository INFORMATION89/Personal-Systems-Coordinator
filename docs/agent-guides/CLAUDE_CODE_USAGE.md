# Claude Code — Usage and Context Guide

**Scope:** contributors using Claude Code (terminal, IDE, desktop or web/cloud sessions) on PSC.
**Status:** optional supplement; it does not make Claude Code or any Claude model mandatory.
**Last reviewed:** 2026-11-28 · adapted from INFORMATION89/Meridian-Engine
**Authority:** `AGENTS.md`, `RULES.md`, `AI_POLICY.md` and `AI_COST_POLICY.md` remain authoritative.

## 1. Know which usage you are spending

Claude Code can run on a subscription allowance or on separately billed API or cloud-provider access. For a subscription, the scarce resource is the account's included usage and its reset windows; check **Settings → Usage**. `/cost` reports API billing only, not subscription usage. `/context` shows what fills the context window. A large context window is not unlimited usage. If prompted to continue with extra usage or credits, decline unless the owner approved it.

## 2. Keep sessions bounded

1. One session, one objective: a work-package task or one PR.
2. Start from the task, its acceptance criteria, the branch and the commit. Reuse existing handoffs; do not re-research what the repository already records.
3. Search first and open only the relevant files and line ranges.
4. Finish and verify the current task before starting another.
5. Save decisions and progress in the repository or PR, not only in chat.

**Compact to continue the same task** (`/compact` with a focus such as "keep objective, decisions, changed files, results, blockers, next action"). **Clear and hand off to start a different task** (`/clear`).

## 3. Avoid expensive habits

- Keep `CLAUDE.md` and `AGENTS.md` short; detail lives in referenced documents.
- Disable MCP servers, connectors and browser tools a task does not need.
- Do not fan out subagents or parallel sessions without a genuinely independent subtask.
- Do not have two assistants duplicate the same audit or plan.
- Use scripts and tools for mechanical checks.

## 4. Cloud sessions and network access

Cloud sessions run with a network policy. If an official documentation host is blocked, request it through the environment approval flow and say why. Never work around a block. If a source still cannot be read, label the claim as seen through search extracts (`RULES.md` §6).

## 5. Model choice

Follow `AI_COST_POLICY.md` §5 and the task tiers in `docs/RESEARCH_PLAN.md` §7. Sonnet is the default for standard work; Opus is for architecture, contracts, security and independent review; Haiku for quick mechanical edits. Do not switch models mid-task without reason. Never make one model a repository requirement.

## 6. Checklist

Before a substantial task:
- [ ] One bounded task with acceptance criteria?
- [ ] Correct sign-in (subscription versus API)?
- [ ] Handoff available instead of repeated research?
- [ ] Only the needed files and tools loaded?
- [ ] Model and effort matched to the tier?

Before ending:
- [ ] Work saved and pushed; branch and commit recorded?
- [ ] Checks and unrun checks reported accurately?
- [ ] Short handoff for the next session?

## 7. Official references

- [Models, usage, and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)
- [Usage limit best practices](https://support.claude.com/en/articles/9797557-usage-limit-best-practices)
- [Explore the Claude Code context window](https://code.claude.com/docs/en/context-window)
- [Manage Claude Code sessions](https://code.claude.com/docs/en/sessions)
- [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)

Provider limits, models and commands change. Re-check official references before relying on them.
