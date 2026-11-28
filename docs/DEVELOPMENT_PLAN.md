# PSC Development Plan

**Status:** draft for owner review · 2026-11-28 · no implementation approved yet
**Prepared with:** Claude Code, tier O (research and planning only; no code). Opus review of the final plan: pending.
**Inputs:** `DECISIONS.md`, `RESEARCH_PLAN.md`, `research/PROVIDER_AUTHORIZATION.md`, `research/PROVIDER_CANDIDATES.md`, `INTEGRATION_COMMONPLACE.md`, Commonplace's own phase plan.

This plan turns the research into milestones. Each milestone has deliverables, an exit gate, the model tier that does the work and the owner decisions it needs. The research plan's work packages (WP1–WP12) remain the research backlog; this plan sequences them into a path to a first release.

## 1. First-release scope

| In scope | Notes |
|---|---|
| **Google Drive** | The average-user provider. Depends on experiments E1/E2 |
| **GitHub** | Plain files with history, for users who already use GitHub |
| **Self-hosted: WebDAV** | Nextcloud as the reference server; others after a capability probe |
| **Self-hosted: user-selected folder** | Reliable on desktop; Android local folders (for example synced by Syncthing); limited on iOS |
| **Commonplace** as the first client | Markdown notes, images, workspace JSON |
| **Desktop first** | Matches Commonplace's desktop-first plan (Windows or macOS first); Android next; iOS later |

**Deferred, not rejected:** Dropbox, OneDrive, iCloud containers, Gitea/Forgejo, other WebDAV presets, S3. For users, Dropbox and OneDrive are as easy as Google Drive; the cost of adding them falls on us, not on the user. They are good candidates once the first three work.

**Out of scope:** multi-person sharing, real-time sync, any PSC-operated server, AI in the sync path.

## 2. How certain we are

"Technical certainty" means how sure we are that PSC can sync Commonplace through this route on the phone-to-PC path. "Average-user fit" means how easily a non-technical friend could set it up.

| Route | Technical certainty | Average-user fit | Why | What would raise certainty |
|---|---|---|---|---|
| **Google Drive API** | **Medium overall.** High that one app on one platform works. **Unknown** whether the same app on Android and desktop can see each other's files, and whether separate apps can. | **High:** a Google account and one sign-in | `drive.file` access may be tied to each OAuth client. Sources conflict: one informal test suggests access is per project, others suggest per client [Community]. Files created outside the app stay invisible. | Experiments E1 and E2 (`PROVIDER_AUTHORIZATION.md` §6) |
| **GitHub API** | **High.** Documented contents API, conditional writes by SHA, a GitHub App installable on one repository [Official] | **Low:** needs a GitHub account and an understanding of repositories | Native sign-in through the device flow is documented, but partly via Enterprise Server pages; deletions persist in history | A GitHub App device-flow test on desktop and Android |
| **WebDAV (Nextcloud)** | **Medium-high.** App passwords, If-Match with 412 on conflict [Official/Community] | **Low-medium:** needs a server, or a host offering WebDAV, plus an app password | Change detection relies on folder ETags; RFC 6578 support for files is unconfirmed | The WebDAV capability probe |
| **WebDAV (other servers)** | **Medium.** Behaviour varies by server | Low | Conditional writes and limits are unverified per server | The probe, per server |
| **Folder on desktop** | **High.** Ordinary file access; the user's sync tool moves the files | Medium: the user must already run a sync tool | PSC can't see the sync tool's state; conflicts arrive as files | A desktop folder prototype with an external sync tool |
| **Folder on Android** | **Medium** for local folders (for example Syncthing); **low** for cloud providers, most of which don't offer folder selection [Official/Community] | Low | Android's tree picker shows only providers that opt in; Google Drive historically did not | A device test with Syncthing and Nextcloud |
| **Folder on iOS** | **Low-medium.** Third-party providers are often greyed out in the folder picker; it depends on the provider's extension [Community, Apple forums] | Low | Works for "On My iPhone" and iCloud Drive; third-party support varies | A device test with Nextcloud and Google Drive |

**Bottom line**
- **Only Google Drive suits average users,** and it is the least certain technically. E1/E2 are the most important open question in the project.
- **GitHub is the most certain technically,** and suits technical users.
- **Self-hosted is certain on desktop.** On phones, use WebDAV, not the folder picker.
- **The phone-to-PC path therefore needs an API route** (Drive, GitHub or WebDAV) on the phone, and every device in one workspace must use the same route (`PROVIDER_AUTHORIZATION.md` §1, point 6).

## 3. Architecture outline (to be specified in M1)

A proposal to guide the milestones, not an approved design:

1. **Contract layer (language-neutral):** workspace layout, file identity, PSC metadata, tombstones, conflict copies, version rules, capability list, error categories, sync state machine.
2. **Coordinator:** change journal, checkpoints, retries, conflict routing, status reporting. Runs inside the host app.
3. **Adapters:** folder, WebDAV, Google Drive, GitHub. Each declares its capabilities; provider concepts stay inside.
4. **Platform services, supplied by the host app:** secure credential storage, file access and permissions, background scheduling, network.
5. **Bindings** for the host languages: Swift (macOS, iOS), C#/.NET (Windows), Kotlin/JVM (Android).
6. **Fixture suite:** language-neutral scenario files that every implementation must pass.

**Working assumptions to confirm in M1**
- **Identity:** Markdown notes carry a stable ID in frontmatter (Commonplace already plans this). JSON files carry an ID field. Images are identified by path plus content hash.
- **PSC metadata** lives in a small `.psc/` area (workspace marker, per-device journals, tombstones), never inside users' notes.
- **Conflicts** produce a visible conflict copy next to the original, so nothing is lost and the user can see both. The app may offer a merge view on top.
- **Per-device files** for journals avoid write contention, the pattern Konode uses for its own sync files.

## 4. Milestones

| # | Milestone | Deliverables | Exit gate | Tier | Owner decisions needed |
|---|---|---|---|---|---|
| **M0** | **Prove the routes** | Google E1–E9 results; GitHub App device-flow test; WebDAV capability probe against Nextcloud; folder tests on desktop, Android and iOS. Throwaway code under `prototypes/` | A go/no-go per route, recorded in `DECISIONS.md` | S (code), O (analysis) | Approve a Google test project and test accounts; approve a test GitHub App; provide or approve a test Nextcloud |
| **M1** | **Contract specification** | `docs/specs/CONTRACT.md`: workspace layout, identity, metadata, tombstones, conflict copies, versioning, capabilities, adapter interface (language-neutral), state machine, errors. Worked examples from Commonplace | Owner approval; Opus review done | O | Approve the file contract (a public commitment) |
| **M2** | **Fixture suite** | `fixtures/`: scenario files for every case in `SYNC_SEMANTICS.md` §11 and `RULES.md` §5 (interruptions, duplicates, concurrent edits, deletes, stale devices, mixed versions, mass deletion) | Fixtures reviewed against the spec | S | — |
| **M3** | **Core technology decision** | Spike of the same slice in 2–3 candidates (for example Kotlin Multiplatform, Rust, per-platform native), called from Swift, C# and Kotlin; comparison report; ADR | Owner selects the technology | S (spikes), O (comparison) | Choose the language/runtime |
| **M4** | **Core with the folder adapter** | Coordinator, journal, conflict handling and the folder adapter; passes the fixture suite; first desktop platform | All fixtures pass; desktop folder sync between two machines works | S | Pick the first desktop OS (with Commonplace) |
| **M5** | **First API adapter** | Google Drive if E1/E2 pass; otherwise GitHub first | Phone-to-PC sync of a test workspace; fixture suite passes against the provider in test accounts | S | Model A or B for Google (from M0) |
| **M6** | **Remaining first-release adapters** | GitHub and WebDAV (Nextcloud), whichever was not in M5 | Same as M5, per adapter | S | — |
| **M7** | **Platform bindings** | Desktop OS #2, Android; secure storage and background hooks; iOS later | Per-platform results reported per `AGENTS.md` | S | Platform order |
| **M8** | **Commonplace integration** | Commonplace swaps its mock PSC adapter for the real one; category selection and consent UI on Commonplace's side | Commonplace's own exit: two devices edit offline and converge without silently losing a note | S (PSC side) | Which Commonplace data categories ship first |
| **M9** | **Hardening and release** | Security and privacy review, threat model update, licensing and provenance review, provider terms for a paid app, OAuth verification as needed, release process | No critical data-loss, security or licensing issue open | O (reviews), S (fixes) | License (WP11), clean-room policy, release |

**Commonplace alignment**
- **Commonplace's Phase 1** uses a mock PSC adapter. PSC can unblock it early by publishing the contract and a stub API after M1.
- **Commonplace's Phase 2** (first sync) depends on M4–M5 plus M8.

## 5. Immediate next steps

1. **Owner:** review this plan and the certainty table.
2. **Owner:** approve M0 test resources: a Google test project, a test GitHub App, and a test Nextcloud (a hosted trial or a local instance).
3. **S-tier session:** run M0. Order: Google E1 and E2 first (highest impact), then the GitHub device flow, the WebDAV probe, and the folder tests.
4. **O-tier, in parallel and research-only:** start the M1 contract draft from the working assumptions in §3.

## 6. Top risks

| Risk | Impact | Mitigation |
|---|---|---|
| Google `drive.file` is per client (E1 fails) | Drive cannot sync one app between phone and PC under least privilege | Fall back to GitHub or WebDAV for the first API adapter; reconsider Google only with an owner decision |
| Average users have no workable option besides Google | Friends can't easily sync | Revisit Dropbox and OneDrive after the first release |
| External edits and sync tools on the folder route create conflicts PSC can't see coming | Duplicate or conflicting files | Conflict copies; clear status; recommend API routes on phones |
| Mixed app versions across devices | Corrupted files | Version rules in M1; mixed-version fixtures in M2 |
| GitHub history keeps deleted notes | Privacy surprise | Disclose it; consider a history-pruning option later |
| Licensing of a paid Commonplace | Legal exposure | Interim clean-room rules; license decision before M9 |
| Official provider docs unreadable from cloud sessions | Weaker evidence | Re-read primary pages from a session with network access before M1 is approved |

## Sources added in this round

- [3DSync issue: shared client with drive.file and Picker](https://github.com/vllni/3DSync/issues/67) (community)
- [scopewright issue: shared-folder visibility under drive.file](https://github.com/v1k0d3n/scopewright/issues/23) (community)
- [Nextcloud forum: SAF tree selection and file creation](https://help.nextcloud.com/t/storage-access-framework-cannot-create-file-in-cloud-folder-selected-with-action-open-document-tree/66482) (community)
- [CommonsWare: Scoped Storage Stories, Trees](https://commonsware.com/blog/2019/11/09/scoped-storage-stories-trees.html) (community)
- [Android: Storage Access Framework](https://developer.android.com/guide/topics/providers/document-provider)
- [Apple: Providing access to directories](https://developer.apple.com/documentation/uikit/providing-access-to-directories)
- [Apple forums: folder from a third-party file provider](https://developer.apple.com/forums/thread/691738) and [third-party providers greyed out](https://developer.apple.com/forums/thread/120257) (community)
