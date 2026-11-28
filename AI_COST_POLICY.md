# PSC — AI Cost and Resource Efficiency Policy

**Status:** adopted at owner request · 2026-11-28 · adapted from INFORMATION89/Meridian-Engine `AI_COST_POLICY.md`
**Scope:** AI-assisted research, engineering, experiments and verification for PSC. It governs efficient use of resources and never weakens correctness, privacy, security, licensing or release requirements.

## 1. Governing principle

**Use the least costly workflow that gives enough evidence for the task. Never reduce required correctness or safety to save resources.**

Cost includes AI tokens and subscription allowance, paid tool credits, web and repository requests, CI minutes, provider API quotas (for example Google Drive), test accounts and devices, and human review time caused by oversized or duplicated changes. Do not invent a budget or assume a service is free. Label estimates as estimates.

## 2. Spending and authorization

1. Use existing approved tools, local scripts and free CI capacity where they suffice.
2. Do not create subscriptions, buy credits, enable paid models or API tiers, create cloud projects with billing, or incur any recurring charge without explicit owner approval.
3. Never enable extra usage, API fallback, auto-reload or paid overages to get past a plan limit.
4. When a task approaches a quota or usage limit, stop optional work, finish and verify the required part, and report the constraint.

## 3. Usage accounting

Subscription allowances, API billing, third-party cloud billing and local inference are different systems. For subscriptions, use the provider's own usage screen; do not convert usage into dollars with API prices or claim a remaining allowance the account does not show. A model's context window is not the same as the plan's usage allowance.

## 4. Budget the work

Before a multi-step task:

1. Confirm the objective, acceptance criteria and smallest useful deliverable.
2. Decide which agent owns the task. If research or planning already exists, hand over a short summary instead of repeating it.
3. Split large work into bounded tasks or PRs. One work-package task per session is the norm.
4. Prefer one active agent per task. Use parallel agents or subagents only for genuinely independent work whose benefit justifies the extra usage.
5. Finish with a short handoff in the PR or docs so the next session need not replay the conversation.

## 5. Context and token efficiency

- Keep always-loaded instructions (`AGENTS.md`, `CLAUDE.md`) short; detail lives in referenced documents.
- Read only the relevant sections of long documents. Search first; open line ranges.
- Do not re-read or re-research what is already recorded for the same question and commit.
- Keep the conversation on one task. Compact to continue the same task; start fresh for an unrelated one, after saving a handoff.
- Use deterministic tools (link checkers, scripts, test runners) for mechanical work instead of model reasoning.
- Do not treat a model's confident answer as evidence.

### Model selection

| Tier | Use for | Claude | ChatGPT |
|---|---|---|---|
| **H** | Routine, bounded edits: link fixes, formatting, extraction, summaries | Haiku-class | an efficient model |
| **F** | No-cost routine work: documentation tidy-ups, PR descriptions, mechanical repository tasks | — | ChatGPT Free, started with `docs/agent-guides/CHATGPT_FREE_STARTER.md` |
| **S** | Standard work: scoped research reports, experiment code, fixtures, focused reviews | Sonnet-class (default) | balanced coding model (interchangeable with Sonnet) |
| **O** | Architecture, file-format and contract design, security/encryption, technology choice, licensing analysis, independent review | Opus-class | an advanced reasoning model, with "Opus review pending" where useful |

Task-by-task assignment is in `docs/RESEARCH_PLAN.md` §7. Model names change; this table describes the strategy, not version locks. Use effort levels proportionally; maximum effort is not a default.

### Multi-agent coordination

- One primary agent owns each task: plan, work, verification and handoff.
- Add a second model only for an independent contribution: adversarial design review, a security or privacy review, or a final diff review where the risk warrants it.
- Do not have two agents duplicate the same research or implementation.
- Resolve disagreements with official documentation or a small discriminating experiment, not model confidence.

### Optional Opus review

Track an advanced second review as **"Opus review pending"** until it actually happens. Use it selectively after a first draft exists: file-format and contract decisions, security and encryption, provider authorization models, technology choice. Give the reviewer the concise spec or diff and the open questions, not the whole history. Verify every finding. Do not spend unapproved paid usage to get it; record when it was skipped and why. The whole-project review brief is `docs/RESEARCH_PLAN.md` §6.

## 6. Tool and request efficiency

1. Batch independent read-only lookups.
2. Search narrowly, then widen only if results are incomplete or contradictory.
3. Do not poll or re-fetch when nothing changed. Retry only a diagnosed transient failure; after a repeated failure, stop and investigate.
4. Keep tool output proportionate to the decision.

## 7. Cost-aware verification

| Change type | Expected verification |
|---|---|
| Documentation or research report | Link check and focused review of the diff. Claims sourced and labelled. |
| Experiment or prototype | Run it against test accounts; record exactly what ran, on which platform, and the results. |
| Sync logic or fixtures | Deterministic offline fixture tests for the changed behaviour, including failure cases. |
| File format or contract | Fixture tests plus compatibility checks with older and newer versions. |
| Security, licensing or release | Every check the risk requires. Never downgrade to a smoke test. |

Each test must protect a distinct behaviour or failure mode. Do not rerun a passing check for the same commit without a reason. Required checks still block merge.

## 8. Provider APIs and test accounts

- Automated tests use fixtures, never live providers.
- Live provider experiments are manual or explicitly marked, use dedicated test accounts and projects, stay within quotas and terms, and are not repeated to get identical results. Record permitted responses as fixtures with source and date.
- Provider quota is a cost separate from AI usage. Saving tokens never justifies wasting quota.

## 9. Stopping rules

Iterate in small steps and stop when the acceptance criteria are met. If a check fails, find whether the cause is the change, environment, dependency, provider or harness before repeating. If remaining uncertainty is non-critical and more verification would be disproportionate, state the limitation and propose the narrowest follow-up.

## 10. Ask the owner before

- any paid model, tool credit, API, subscription, hosted service or cloud project with charges;
- creating provider registrations (cloud projects, OAuth clients);
- exceeding an approved budget;
- long or expensive test runs without a clear acceptance need;
- weakening a required security, privacy or compatibility gate;
- external, destructive, publishing or irreversible actions.

## 11. Reporting

Attribute the tool and tier as `AI_POLICY.md` §5 requires. For non-trivial work, report: scope and acceptance criteria; checks chosen and why; what actually ran, with commit and environment; known external or paid usage; what was not run and why; quota or access limitations; remaining risks and the next gate. Never report estimated usage as measured, or unrun checks as passed.
