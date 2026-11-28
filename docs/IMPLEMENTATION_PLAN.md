# PSC Implementation Plan: Start to First Release

**Status:** draft for owner review · 2026-11-28 · no implementation approved until gate G0 is passed
**Prepared with:** Claude Code, tier O (planning only; no code). Opus review of this plan: pending.
**Builds on:** [Development plan](DEVELOPMENT_PLAN.md) (scope, certainty, milestones M0–M9), [Decisions](DECISIONS.md), [Research plan](RESEARCH_PLAN.md).

This is the working plan for building PSC from today to its first release, with **Sonnet (tier S) doing the coding**, **Opus (tier O) writing specifications and reviews at checkpoints**, and **the owner approving at gates**. Every task is sized to one Sonnet session and one pull request, so work can continue task after task until the release.

## 1. How the plan runs

**Roles**

| Role | Does | Does not |
|---|---|---|
| **Sonnet (S)** | All code, tests, fixtures, tooling, CI, docs for its own changes, prototype experiments | Change the contract, pick technology or license, create cloud resources, merge |
| **Opus (O)** | Specifications, comparisons, security/licensing/architecture reviews, analysis of experiment results | Write code (current owner instruction) |
| **Haiku/ChatGPT Free (H/F)** | Link fixes, formatting, PR descriptions, small doc tidy-ups | Anything in tiers S or O |
| **Owner** | Gate approvals, creating accounts and registrations, running tests on personal devices, merging | — |

**Rules for every task**
- One task per session and one PR. The task ID goes in the PR's "Task" section.
- Start only when every dependency is merged and any gate before it is passed.
- If the spec is unclear, Sonnet stops and asks in the PR. It does not guess on contract questions.
- After two failed CI fixes, Sonnet stops and reports.
- Every PR follows the template, attributes tool and tier (`AI_POLICY.md` §5), and lists what was and was not verified.
- "Opus review pending" items must be cleared before the next gate.

**Task sizes:** **S** = small, a focused change; **M** = medium, one feature with tests; **L** = large, split into sub-PRs if the diff grows past roughly 600 lines of non-test code. Sizes are estimates of effort, not dates.

## 2. Owner gates

Work stops at each gate until the owner approves. Opus prepares the evidence for each gate.

| Gate | When | Owner approves |
|---|---|---|
| **G0** | Before any code | This plan; creation of test resources (§3); starting implementation work |
| **G1** | After M0 experiments | Go/no-go per route; Google model A (one shared project) or B (per app); first API provider |
| **G2** | After the contract draft | Contract v0 (a public commitment) |
| **G3** | After the technology spikes | Core technology and language; PSC's license; clean-room policy; first desktop OS |
| **G4** | After the core is built | Core sync engine and folder adapter (fixture suite passing) |
| **G5** | After the adapters are built | Providers for the first release; security review result |
| **G6** | Before release | Release candidate, OAuth verification status, provider terms for a paid app, release itself |

## 3. Resources the owner provides at G0

| Resource | Used by | Notes |
|---|---|---|
| Google Cloud test project "PSC Test", with Drive API enabled and the consent screen in testing mode | M0, M5 | Test users only. Create two OAuth clients for E1: a desktop client and a second desktop or "limited input device" client |
| Two Google test accounts | M0, M5 | Never the owner's personal account |
| GitHub App "Personal Systems Coordinator (test)", with device flow enabled and Contents read/write only | M0, M5 | A separate test GitHub account with one private repository |
| Nextcloud test server | M0, M5 | A local Docker instance in CI is enough; optionally a hosted trial |
| Device access | M0, M7 | One Android phone or emulator; one Mac for Apple builds; owner runs device checklists |
| CI budget decision | M3 onward | macOS and Windows runners cost more on private repositories; the owner confirms the budget or makes the repository public |
| Secrets storage | All | Client IDs in untracked local config and CI secrets; never committed |

## 4. Proposed repository layout (confirmed at G3)

```
spec/            contract specification and fixture format (from docs/specs once approved)
fixtures/        language-neutral scenario files
tools/           fixture validator, reference simulator, WebDAV probe (Python, like ci/pr_hygiene.py)
core/            sync engine in the chosen technology
adapters/        folder/, webdav/, gdrive/, github/
bindings/        swift/, dotnet/, kotlin/
samples/         cli/ (standalone sample consumer), desktop sample
prototypes/      M0 throwaway experiments (never shipped)
docs/            plans, research, decisions, guides
```

## 5. Task list

### Phase 0 — Setup

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| P0.1 | Owner passes G0 and creates the §3 resources | Owner | — | — | Resources exist; client IDs stored outside the repository |
| P0.2 | Repository hygiene: `.gitignore` for secrets and local config, `local.config.example`, Markdown link-check CI job, `prototypes/README.md` labelling everything there as non-production | S | S | G0 | CI green; link check runs on docs PRs |

### Phase 1 — M0: prove the routes (throwaway prototypes)

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S0.1 | **Drive E1 on desktop only:** client A creates a folder and a file; client B (a different OAuth client, same project) lists and reads it. Also E3 (a client from another project). Scripts under `prototypes/m0-drive/` | S | M | P0.1 | Report states per-client or per-project, with exact responses; repeatable script |
| S0.2 | Drive E2, E4–E8: second app identity, folder picking, picking files created elsewhere, external edits, Drive for desktop files, revoke and re-authorize. Android parts as an owner-run checklist with a minimal test app | S | L | S0.1 | Each experiment marked passed, failed or not run, with evidence |
| S0.3 | **GitHub route:** GitHub App device flow from a desktop script; contents API create, update with the correct SHA, rejection with a stale SHA; commit listing for change detection | S | M | P0.1 | Report with responses; token refresh tested |
| S0.4 | **WebDAV probe tool** (`tools/webdav_probe.py`): checks If-Match and 412, ETag stability, folder ETag propagation, sync-collection support, 429/503 behaviour. Run against Nextcloud in Docker | S | M | P0.2 | Probe report for Nextcloud; the tool runs against any server URL |
| S0.5 | **Folder route:** desktop scripts (atomic replace, rename detection, external edits while open); Android and iOS owner-run checklists (local folder, Syncthing, Nextcloud provider, Google Drive provider) | S | M | P0.2 | Results table per platform |
| O0.6 | Analyse M0 results; recommend G1 decisions; update `DEVELOPMENT_PLAN.md` §2 certainty and `PROVIDER_AUTHORIZATION.md` | O | M | S0.1–S0.5 | Decision memo ready for G1 |
| — | **Gate G1** | Owner | — | O0.6 | Routes and first API provider recorded in `DECISIONS.md` |

### Phase 2 — M1: contract specification

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| O1.1 | Contract v0 draft, `docs/specs/CONTRACT.md`: workspace layout and marker; file identity (Markdown frontmatter ID, JSON ID field, image path + hash); PSC metadata under `.psc/`; per-device journals; tombstones; conflict copies and their naming; version and compatibility rules; capability list; language-neutral adapter interface; sync state machine; error categories; status model; security notes | O | L | G1 | Covers every rule in `RULES.md` §5 and every case in `SYNC_SEMANTICS.md` §11 |
| O1.2 | Fixture format spec, `docs/specs/FIXTURES.md`: how a scenario describes devices, initial states, operations, faults and expected outcomes | O | M | O1.1 | Can express all M2 scenarios |
| O1.3 | Commonplace worked examples in the contract: a note with an image, workspace layout JSON, a deleted note, a conflict | O | S | O1.1 | Examples match `INTEGRATION_COMMONPLACE.md` |
| — | **Gate G2** | Owner | — | O1.1–O1.3 | Contract v0 approved; Commonplace can build its mock adapter against it |

### Phase 3 — M2: fixture suite and reference simulator

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S2.1 | Fixture JSON schema and validator (`tools/fixtures/validate.py`), CI job | S | M | G2 | Invalid fixtures fail CI |
| S2.2 | Reference simulator (`tools/fixtures/simulate.py`): an in-memory model of the contract used only to check that fixtures are consistent. Not shipped | S | L | S2.1 | Runs every fixture; disagreements are reported as spec questions |
| S2.3 | Fixtures: basic create, update, rename, delete across two devices | S | M | S2.2 | Simulator passes |
| S2.4 | Fixtures: concurrent edits and conflict copies for Markdown, images and JSON | S | M | S2.2 | Simulator passes |
| S2.5 | Fixtures: faults (interrupted upload or download, duplicate delivery, lost cursor, 429, 5xx, out of storage, revoked access) | S | M | S2.2 | Simulator passes |
| S2.6 | Fixtures: stale device after weeks offline, mixed app versions, unknown fields preserved, mass-deletion guard, restore from an old backup | S | M | S2.2 | Simulator passes |
| O2.7 | Review fixtures against the contract; list gaps | O | S | S2.3–S2.6 | Gaps fixed or recorded as contract v0.x questions |

### Phase 4 — M3: core technology decision

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S3.1 | Spike A: Kotlin Multiplatform core running a five-fixture slice; called from Swift, C# and Kotlin/JVM | S | L | S2.3 | Slice passes; binding effort, build steps and binary size recorded |
| S3.2 | Spike B: Rust core with generated bindings, same slice and callers | S | L | S2.3 | Same as S3.1 |
| S3.3 | Spike C: separate native implementations (one in Swift, one in C#) of the same slice, both tested against the fixtures | S | L | S2.3 | Same as S3.1 |
| O3.4 | Comparison report and draft ADR: binding quality, maintenance, debugging, size, platform APIs, fit with Meridian's Kotlin Multiplatform baseline, dependency licenses | O | M | S3.1–S3.3 | Report covers `RESEARCH_PLAN.md` WP7 criteria |
| O3.5 | License and clean-room recommendation for PSC, given a possibly paid Commonplace (WP11) | O | M | — (can run in parallel) | Options with obligations; dependency allow/deny list |
| — | **Gate G3** | Owner | — | O3.4, O3.5 | Technology, license, clean-room policy and first desktop OS recorded in `DECISIONS.md` |

### Phase 5 — M4: core sync engine and folder adapter

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S4.1 | Project skeleton in the chosen technology; build; CI on Linux plus the first desktop OS; dependency locking; license audit job; LICENSE file per G3 | S | M | G3 | CI green; audit lists all dependencies |
| S4.2 | Fixture runner in the core language: loads `fixtures/` and drives the engine through a fake adapter | S | M | S4.1 | Runs fixtures; reports pass/fail per scenario |
| S4.3 | Domain model: workspace, file identity, metadata, versions, errors (per contract) | S | M | S4.2 | Unit tests; serialization round-trips |
| S4.4 | Device-local state store: journal, checkpoints, cursors, kept outside the workspace | S | M | S4.3 | Survives crash at every write step (fault tests) |
| S4.5 | Local change detection: scan, hash, rename detection, external-edit detection | S | M | S4.4 | S2.3 fixtures pass locally |
| S4.6 | Adapter interface and an in-memory fake adapter with fault injection | S | M | S4.3 | Fake supports every fault in S2.5 |
| S4.7 | Sync cycle: pull, apply, push with conditional writes; checkpoint advanced only after durable apply | S | L | S4.5, S4.6 | S2.3 and S2.5 fixtures pass against the fake |
| S4.8 | Conflict handling and conflict copies | S | M | S4.7 | S2.4 fixtures pass |
| S4.9 | Deletions, tombstones and mass-deletion guard; restore from backup | S | M | S4.7 | S2.6 deletion fixtures pass |
| S4.10 | Version handling: unknown fields preserved, newer-version files never corrupted | S | M | S4.7 | S2.6 version fixtures pass |
| S4.11 | Status and events API for host apps (last sync, pending changes, conflicts, errors, auth expired) | S | M | S4.7 | Contract status model covered by tests |
| S4.12 | Folder adapter for desktop (atomic writes, file-provider placeholders handled, coordination where the OS needs it) | S | L | S4.7 | Full fixture suite passes against a real temp folder |
| S4.13 | Standalone CLI sample (`samples/cli`): init workspace, sync, status, list conflicts. No dependency on Commonplace | S | M | S4.12 | Two-machine folder sync demo scripted and documented |
| O4.14 | Opus review of the core: correctness of the state machine, crash safety, conflict paths | O | M | S4.7–S4.13 | Findings fixed (S) or accepted by the owner |
| — | **Gate G4** | Owner | — | O4.14 | Core approved; Commonplace may integrate the folder route for desktop testing |

### Phase 6 — M5/M6: provider adapters (first API provider from G1 first)

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S5.1 | Transport layer: HTTP client interface, retry and backoff (Retry-After), timeouts, offline handling | S | M | G4 | Fault fixtures pass against a fake HTTP layer |
| S5.2 | Credential interface: host app supplies secure storage; tokens never logged; refresh flow abstraction | S | M | S5.1 | Log-scrubbing test; no token reaches logs |
| S5.3 | **GitHub adapter:** device-flow sign-in, repository selection, contents API with SHA-conditional writes, change detection via commits, batched commits, private-repository check | S | L | S5.2 | Fixture suite passes on recorded responses; marked live test passes on the test repository |
| S5.4 | **Google Drive adapter** (model from G1): desktop OAuth with PKCE via loopback, `drive.file`, change feed, revision-aware updates, resumable upload | S | L | S5.2 | Same as S5.3, on the test project |
| S5.5 | **WebDAV adapter:** app-password sign-in, capability probe built in, If-Match writes, folder-ETag change detection with fallback scan | S | L | S5.2 | Fixture suite passes against Nextcloud in Docker in CI |
| S5.6 | Live provider test suite: manual or scheduled, test accounts only, quota-safe | S | M | S5.3–S5.5 | Documented run; results recorded per provider |
| S5.7 | Mixed-route guard: detect and refuse a workspace reached through different routes on different devices (for example Drive API on one device and Drive for desktop on another) | S | M | S5.4 | Clear error and status; covered by tests |
| O5.8 | Security review: OAuth flows, redirect handling, PKCE/state checks, token storage, logging, threat model update | O | M | S5.3–S5.5 | Findings fixed or accepted |
| — | **Gate G5** | Owner | — | O5.8 | First-release providers confirmed |

### Phase 7 — M7: platform bindings

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S7.1 | Binding and sample for desktop OS #1 (Swift for macOS or C# for Windows): secure storage (Keychain or Credential Manager), sign-in UI hand-off to the system browser, background hook | S | L | G5 | Sample app syncs with all three providers; per-platform report |
| S7.2 | Binding and sample for desktop OS #2 | S | L | S7.1 | Same as S7.1 |
| S7.3 | Android binding (Kotlin): Keystore-backed storage, WorkManager hook, SAF for local folders, sign-in hand-off; owner runs the device checklist | S | L | G5 | Phone-to-PC sync demo through each provider; device results recorded |
| S7.4 | Linux feasibility check against the criteria in `RESEARCH_PLAN.md` WP8 | S | M | S7.1 | Go/no-go evidence for the owner |
| — | iOS binding | — | — | — | **After the first release**, when Commonplace schedules iOS |

### Phase 8 — M8: Commonplace integration support

Commonplace's own adapter lives in the Commonplace repository; PSC supplies what it needs.

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S8.1 | Integration guide: setup, provider connection, data categories, status and conflict handling, error states, what the host app must provide | S | M | S7.1 | Reviewed against the contract |
| S8.2 | Versioned internal packages per platform, with changelog and compatibility range | S | M | S7.1 | Commonplace can depend on a fixed version |
| S8.3 | Commonplace-shaped acceptance test: a sample workspace with notes, images and layout JSON; two devices edit offline and converge without silently losing a note | S | M | S8.2 | Passes on desktop and Android |
| — | Commonplace swaps its mock adapter for PSC (in the Commonplace repository) | Commonplace session | — | S8.2 | Commonplace's Phase 2 exit criterion met |

### Phase 9 — M9: hardening and first release

| ID | Task | Tier | Size | Depends | Acceptance |
|---|---|---|---|---|---|
| S9.1 | Soak and crash tests: kill the process at random points during long sync runs | S | M | G5 | No data loss across many runs; results recorded |
| S9.2 | Scale tests: large workspaces, many images, slow providers | S | M | G5 | Limits documented; no pathological polling |
| S9.3 | Migration framework and a test from contract v0 to v0.x | S | M | G5 | Old workspaces open safely |
| O9.4 | Final security and privacy review | O | M | S9.1–S9.3 | No critical findings open |
| O9.5 | Licensing and provenance review: SBOM, notices, dependency licenses against the G3 policy | O | M | S9.1–S9.3 | Clean inventory |
| O9.6 | Provider terms review for a paid Commonplace (Google, GitHub, WebDAV hosts) | O | S | — | Findings for the owner |
| P9.7 | Production registrations: Google consent screen and verification for "Personal Systems Coordinator"; public GitHub App | Owner | — | O9.6 | Verified or in progress, with known user caps |
| S9.8 | Release engineering: version 1.0.0 tags, packages per platform, release notes, integration guide final | S | M | O9.4, O9.5 | Reproducible release build |
| — | **Gate G6** | Owner | — | All above | **First release** |

## 6. Standard Sonnet session prompt

Paste at the start of each session, filling in the task ID:

```text
You are working on INFORMATION89/Personal-Systems-Coordinator.
Read AGENTS.md, then find task <TASK ID> in docs/IMPLEMENTATION_PLAN.md section 5.
Do only that task. Check that its dependencies are merged and the gate before it is passed;
if not, stop and say so.

Rules:
1. Work on one branch from the current main; open one PR with .github/pull_request_template.md.
2. Follow the approved contract (docs/specs or spec/) exactly. If it is unclear or seems wrong,
   stop and raise the question in the PR instead of guessing.
3. Keep tests deterministic and offline, except tests marked live, which use test accounts only.
4. Never commit secrets, tokens, client secrets or personal data.
5. Do not change the contract, add a dependency outside the G3 policy, create cloud resources,
   or merge. Those need the owner.
6. Few commits (1-3 per PR). No CI-skip markers on code.
7. If CI fails twice after attempted fixes, stop and report.
8. Finish with a handoff: branch, commit, files changed, checks run and not run, open questions,
   and the next task ID.
```

## 7. Handoff format

Every task ends with this in the PR description, so the next session starts from it instead of re-reading history:

- **Task and result:** ID, done or partly done.
- **Branch and commit.**
- **Changed:** files and behaviours.
- **Verified:** commands, fixtures, live tests, platforms.
- **Not verified:** and why.
- **Questions for the owner or Opus.**
- **Next task:** the next ID whose dependencies are now met.

## 8. Critical path and parallel work

**Critical path:** G0 → S0.1 (Drive E1) → G1 → O1.1 → G2 → S2.x → S3.x → G3 → S4.x → G4 → first API adapter → G5 → S7.1 → S8.3 → M9 → G6.

**Can run in parallel**
- S0.3–S0.5 alongside S0.1–S0.2.
- O3.5 (license) any time before G3.
- In M5, the adapters run in parallel once S5.2 is merged, with one session per adapter.
- S7.2 and S7.3 after S7.1.

Following `AI_COST_POLICY.md` §4, run parallel sessions only for genuinely independent tasks.

## 9. Where Sonnet cannot do the work alone

| Need | Why | Plan |
|---|---|---|
| Creating Google, GitHub or Nextcloud resources | Owner approval and owner accounts | P0.1, P9.7 |
| Physical Android or iOS devices | Cloud sessions have no devices | Owner-run checklists in S0.2, S0.5, S7.3 |
| Apple builds and signing | Needs macOS and an Apple developer account | macOS CI runner (cost decision at G0) or the owner's Mac |
| Reading some official docs | Some documentation hosts are blocked in cloud sessions | Re-check primary pages from an environment with access before G2 |
| Gate decisions | Owner-reserved | Opus prepares a memo per gate |

## 10. Keeping the plan current

- Mark tasks done in this file as their PRs merge (task ID, PR link, date).
- When a gate changes scope (for example Google model B at G1), update the affected tasks before starting them.
- New work goes in as a new task ID with tier, size, dependencies and acceptance criteria; never as unplanned scope inside another task's PR.
