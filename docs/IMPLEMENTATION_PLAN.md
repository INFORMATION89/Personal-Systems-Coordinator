# PSC Implementation Plan: Start to First Release

**Status:** draft for owner review · 2026-11-28
**Prepared with:** Claude Code, tier O (planning only; no code). Owner review pending.
**Design:** [Architecture and design decisions](ARCHITECTURE.md). This plan builds exactly that design.

The plan has two phases:
1. **Phase A, Decide:** owner decisions, a few small throwaway experiments, and the exact specification files. **No product code.** It ends at **Design Freeze.**
2. **Phase B, Build:** product code, step by step, by **Sonnet in Claude Code**, until the first release.

Coding starts only after Design Freeze, when everything needed for the first viable product is decided.

## 1. Working agreement

**Roles**

| Who | Does |
|---|---|
| **Owner** | Answers the decisions in `ARCHITECTURE.md` §1, creates test accounts and registrations, tests on personal devices, reviews and merges PRs |
| **Sonnet** (Claude Code) | Every coding step, experiment, test, spec file and doc update in this plan |
| **Opus** | Two reviews only: R1 at Design Freeze (optional) and R2 before release (security). Nothing else, to save plan usage |

**Efficiency on the Claude Pro plan**
- One step = one Sonnet session = one PR. Steps are sized to fit one session.
- Start each session with the prompt in §5. Sonnet reads `AGENTS.md`, the step and only the files it names.
- Don't repeat research. If a question isn't answered by `ARCHITECTURE.md`, Sonnet stops and asks instead of exploring.
- No parallel sessions unless two steps are independent and the plan allows it.

**Quality rules** (from `RULES.md` and `ARCHITECTURE.md` §9)
- Follow the architecture exactly. If it seems wrong or incomplete, stop and ask; never improvise a new system.
- Use the libraries in `ARCHITECTURE.md` §9.1. New dependencies need a reason in the PR and must pass `cargo-deny`.
- No hard-coded limits, names or user-facing text.
- Every step leaves CI green, with tests for what it added.

**Explaining to the owner.** The owner doesn't read code. Every PR summary explains in plain words what changed, what it means for the product and what to test. Technical choices inside the architecture are made by the coding session and recorded in the PR. Structural choices go to the owner with pros, cons and a recommendation.

## 2. Phase A — Decide (no product code)

| Step | What | Who | Result |
|---|---|---|---|
| **A0** | ~~Owner answers D1–D7~~ **Done 2026-11-28:** Rust, macOS, Android, plain files, GitHub first, Apache-2.0, public repository | Owner | Recorded in `DECISIONS.md` |
| **A0b** | Owner creates test resources: Google Cloud project "PSC Test" with the Drive API enabled, consent screen in testing mode and **two desktop OAuth clients**; two Google test accounts; GitHub App "Personal Systems Coordinator (test)" with device flow and Contents read/write; a GitHub test account with one private repository. Client IDs stored outside the repository | Owner (Sonnet writes a step-by-step guide first, as A0a) | Resources ready |
| **A1** | **Drive experiment E1:** client A creates a folder and a file; client B (same project, different client) lists and reads it. Also E3 (a client from a second project). Throwaway script in `prototypes/a1-drive/` | Sonnet | Per-client or per-project answer. With D5, decides Drive's place in v1 |
| **A2** | **Binding experiment:** a tiny Rust library with one async function, one callback interface and one error type, called from Swift, Kotlin and C# (`uniffi-bindgen-cs`). In `prototypes/a2-bindings/` | Sonnet | Confirms the C# path, or switches to the `csbindgen` fallback |
| **A3** | **WebDAV probe** against Nextcloud in Docker: If-Match and 412, ETag behaviour, folder ETag changes when a child changes, `MOVE`, error codes. Reusable script `tools/webdav_probe.py` | Sonnet | Confirms the WebDAV design in §6 |
| **A4** | **GitHub experiment:** device-flow sign-in with the test GitHub App; one commit per cycle with the Git data API, and a branch update that fails when the tip moved; empty-repository bootstrap on a non-`main` branch; whether no-cache headers are needed to avoid stale 409s; uploads of 10, 30 and 60 MB; change detection by commit comparison and its limits (`research/GITHUB_SYNC_PATTERNS.md` §4) | Sonnet | Confirms the GitHub design and sets the file-size cap |
| **A5** | **Drive details** (only if A1 passes): does the file metadata include `sha256Checksum`; how to update only if unchanged; what files created in the Drive web UI look like to the app | Sonnet | Confirms the Drive design |
| **A6** | Update `ARCHITECTURE.md` with A1–A5 results; list any changes | Sonnet | Design updated |
| **A7** | **Specification files:** JSON Schemas for every file in §3 of the architecture (`spec/schemas/`); `spec/CONFIG.md` with every configuration value, default, unit and reason; `spec/ERRORS.md` with every error code; `spec/FIXTURES.md` describing the scenario format | Sonnet | Exact, checkable spec |
| **A8** | **Scenario list:** the sync scenarios every implementation must pass, written as data files in `fixtures/` (two devices, operations, faults, expected results), covering every row of `ARCHITECTURE.md` §5 and `RULES.md` §5. Validated against the schema by a small checker | Sonnet | `fixtures/` ready for Phase B |
| **R1** | **Optional Opus review** of the architecture, spec and scenarios together, in one session | Opus | Findings fixed in a Sonnet session or accepted by the owner |
| **Design Freeze** | Owner confirms: decisions answered, experiments done, spec and scenarios approved | Owner | `DECISIONS.md` records Design Freeze; `AGENTS.md` "Current phase" changes to "Build" |

A1–A5 are throwaway experiments that settle decisions. They are not product code, and nothing in `prototypes/` is reused in Phase B.

**If A1 fails:** apply the owner's D5 choice, then continue. **If A2's C# path fails:** use `csbindgen` and record it.

## 3. Phase B — Build (Sonnet)

Each step lists what it depends on and when it is done. Per the owner's decisions: **desktop #1 = macOS (Swift)**, **phone = Android (Kotlin)**, **desktop #2 = Windows (C#)**. GitHub is the first online route (D5).

### B.1 Foundation

| Step | What | Depends | Done when |
|---|---|---|---|
| **B0** | Cargo workspace with the crates from `ARCHITECTURE.md` §6 (empty but compiling); `rust-toolchain.toml`; lint configuration; `cargo-deny` configuration with an Apache-2.0-compatible license allowlist; CI on Linux and macOS running fmt, clippy, tests, deny and PR hygiene; an `AGENTS.md` note for crate boundaries | Design Freeze | CI green with empty crates |
| **B1** | `psc-testkit`: scenario runner reading `fixtures/`, fake clock, in-memory fault-injecting adapter (`psc-adapter`) | B0 | The runner loads every scenario and reports "not implemented" cleanly |
| **B2** | `psc-core` domain types and configuration module (from `spec/CONFIG.md`); JSON models for every file in architecture §3 with round-trip tests against `spec/schemas/`; error codes from `spec/ERRORS.md` | B0 | Schema round-trip tests pass |
| **B3** | `psc-state`: SQLite device-local state (index, bases, checkpoints, lock, route, device ID) with migrations and crash-safety tests | B2 | Crash-at-every-step tests pass |

### B.2 Sync engine

| Step | What | Depends | Done when |
|---|---|---|---|
| **B4** | Local scanner: change detection by size, modification time and hash; ignore list; allowed types; same-cycle rename detection | B3 | Scanner unit and property tests pass |
| **B5** | Sync cycle (architecture §5.2) for create, update and download against the in-memory adapter, with conditional writes and checkpoint safety | B1, B4 | Basic scenarios pass |
| **B6** | Conflicts and conflict copies (§5.3) | B5 | Conflict scenarios pass |
| **B7** | Deletions, tombstones, retention, mass-deletion guard, stale-device reconcile (§5.4) | B5 | Deletion and stale-device scenarios pass |
| **B8** | Format and version handling: unknown fields preserved, `update_required`, workspace creation race, registry and device files (§3, §4) | B5 | Version scenarios pass |
| **B9** | Status, sync report, events and cancellation and time budget | B5 | Status scenarios pass; **the full scenario suite passes against the in-memory adapter** |

### B.3 First route: local folder

| Step | What | Depends | Done when |
|---|---|---|---|
| **B10** | `psc-folder` adapter: temporary file plus atomic rename, placeholder (online-only) files handled, platform file coordination where required | B9 | Full scenario suite passes against a real temporary folder |
| **B11** | `psc-cli`: init, connect folder, sync, status, conflicts. A standalone sample with no Commonplace code | B10 | A scripted two-folder sync demo works on macOS |

**Checkpoint 1 (owner):** the owner runs the CLI demo by following a written guide. Sync works between two folders on the computer.

### B.4 Network routes

| Step | What | Depends | Done when |
|---|---|---|---|
| **B12** | `psc-transport`: HTTP client, retries and backoff with Retry-After, timeouts, offline detection, log redaction test | B9 | Transport tests pass; the redaction test proves no token is logged |
| **B13** | OAuth flows in `psc-transport`: PKCE with loopback for desktop, external browser hand-off for phones, GitHub device flow; credential store interface | B12 | Flows tested against recorded responses |
| **B14** | `psc-github` adapter (first online route, D5): one commit per cycle, private-repository check, change detection by commit comparison | B13 | Scenario suite passes on recorded responses; a manual live test passes on the test repository |
| **B15** | `psc-webdav` adapter (from A3 results) | B12 | Full scenario suite passes against Nextcloud in Docker in CI |
| **B16** | `psc-gdrive` adapter (only if Drive is in v1 after A1 and D5) | B13 | Same as B15, on the test project |
| **B17** | Route binding and mismatch guard (architecture §5.6); connect and disconnect for every route in the CLI | B14–B16 | Route-mismatch scenarios pass; the CLI connects to every route |

**Checkpoint 2 (owner):** following a guide, the owner syncs two folders on the Mac through GitHub first, then WebDAV and (if included) Google Drive, with the CLI.

### B.5 Apps and platforms

| Step | What | Depends | Done when |
|---|---|---|---|
| **B18** | `psc-ffi`: the public API from architecture §8.1, exported through UniFFI; async and callbacks; error codes | B17 | API tests pass through the Rust API |
| **B19** | macOS binding and package (Swift package with an XCFramework), Keychain credential store, `ASWebAuthenticationSession` hand-off, a minimal SwiftUI sample app | B18 | The sample app syncs through every route on macOS |
| **B20** | Android binding and package (AAR with `cargo-ndk`, Keystore-backed credentials, Custom Tabs hand-off, WorkManager example), and a sample app; emulator tests in CI | B18 | The sample syncs on the emulator; the owner confirms on a real phone |
| **B21** | Windows binding and package (C# with `uniffi-bindgen-cs`, or `csbindgen` per A2), Credential Manager store, a minimal sample app | B19 | Same as B19, on Windows |
| **B22** | Integration guide for app developers (setup, routes, status, conflicts, errors, what the host must provide), and version and compatibility policy | B19 | Guide reviewed against the API |

**Checkpoint 3 (owner):** phone-to-PC sync with the sample apps through each route.

### B.6 Commonplace and release

| Step | What | Depends | Done when |
|---|---|---|---|
| **B23** | Commonplace-shaped acceptance test: a sample workspace with notes, images and layout JSON; two devices edit offline and converge without silently losing a note | B20, B21 | Passes on desktop and phone |
| **B24** | Soak and crash tests (the process killed at random points), scale tests (large folders, many images), migration test from format 1 | B23 | No data loss across runs; limits documented |
| **R2** | **Opus security and privacy review:** sign-in flows, token handling, logging, file safety, dependency licenses | Opus | Findings fixed (Sonnet) or accepted (owner) |
| **B25** | Fix R2 findings | Sonnet | Re-checked |
| **B26** | Release preparation: Google consent screen verification for "Personal Systems Coordinator" (owner submits; Sonnet prepares the material), public GitHub App, provider-terms check for a paid Commonplace, SBOM and notices, versioned packages, release notes | Owner and Sonnet | All items done or explicitly accepted |
| **Release** | Owner approves PSC 1.0 | Owner | Commonplace switches from its mock adapter to PSC (in the Commonplace repository) |

**Rough size (estimate):** about 10 Sonnet sessions in Phase A and about 30–40 in Phase B, plus 1–2 Opus sessions. Fix-up sessions after failed CI or review are extra.

## 4. What is needed from the owner, and when

| When | Need |
|---|---|
| Now | Answers to D1–D7 (`ARCHITECTURE.md` §1) |
| A0b | Google test project with two OAuth clients, two Google test accounts, test GitHub App and test repository |
| A3, B14 | Nothing: Nextcloud runs in Docker in CI |
| Checkpoints 1–3 | Running the demos with the written guides |
| B20 | A phone (or approval to rely on the emulator plus one manual check) |
| B26 | Submitting Google verification; making the GitHub App public |
| Always | Reviewing and merging PRs; nobody else merges |

## 5. Sonnet session prompt

Paste at the start of each Claude Code session, filling in the step:

```text
Repository: INFORMATION89/Personal-Systems-Coordinator.
Read AGENTS.md. Then read step <STEP> in docs/IMPLEMENTATION_PLAN.md and only the sections of
docs/ARCHITECTURE.md and spec/ that the step needs.

Do only step <STEP>. First check that the steps it depends on are merged; if not, stop and say so.

Rules:
- Follow ARCHITECTURE.md and spec/ exactly. If something is missing, unclear or seems wrong,
  stop and ask in the PR; do not invent a new design.
- Use the libraries in ARCHITECTURE.md section 9.1. Any other dependency needs a reason in the PR.
- No hard-coded limits, names or user-facing text; use the configuration module.
- Tests for everything you add. CI must be green. After two failed fixes, stop and report.
- Never commit secrets or tokens. Live tests use test accounts only and are marked live.
- One branch, one PR using .github/pull_request_template.md, 1-3 commits.
- In the PR summary, explain in plain words for a non-programmer what changed and how to check it.
- End with the handoff: branch, commit, files changed, checks run and not run, open questions,
  next step.
```

## 6. Handoff format

Every PR ends with:
- **Step and result** (done, or partly done and why).
- **What changed,** in plain words.
- **How to check it,** for the owner, if anything is visible.
- **Verified:** commands, scenarios, tests run.
- **Not verified,** and why.
- **Questions** for the owner.
- **Next step.**

## 7. Keeping the plan current

- When a step's PR merges, mark it here with the PR link and date.
- If an experiment or review changes the design, update `ARCHITECTURE.md` first (in its own PR), then continue.
- New work becomes a new step with dependencies and a "done when". It is never added silently to another step.
