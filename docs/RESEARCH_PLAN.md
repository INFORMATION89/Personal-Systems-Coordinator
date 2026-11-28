# Research Plan

**Status:** open research agenda · refreshed 2026-11-28 · independent Opus review planned before any architecture decision

This plan starts from what Personal Systems Coordinator (PSC) is trying to achieve, derives the questions that must be answered before implementation, and organizes them into work packages with deliverables, dependencies and exit criteria. Research must distinguish documented provider capabilities, test results and assumptions. Nothing in this plan selects a provider, protocol, language or license.

## 1. What PSC is trying to achieve

Derived from the [Product overview](PRODUCT_OVERVIEW.md), [Principles](PRINCIPLES.md) and [Decision register](DECISIONS.md):

| Goal | Meaning | Hard constraint attached |
|---|---|---|
| **G1 Cross-device continuity** | A person's user-approved app data (starting with Solstice preferences) follows them between their devices. | Through storage the user already controls; PSC never operates a backend, relay, managed storage or account system. |
| **G2 Cross-app interoperability** | Independent apps (Solstice, Notes, Clock, Calendar) can reference and display each other's data through explicit contracts. | Each app keeps ownership of its domain model; no app silently rewrites another's records. |
| **G3 Local-first** | Every app is fully useful offline, without a connected provider and during provider failures. | Sync is eventual and opportunistic; status must be honest. |
| **G4 Trust and control** | The person can see, choose, pause, export and disconnect what syncs, where and why. | Per-purpose consent; least privilege; no silent sync of location, raw weather data or credentials. |
| **G5 Provider neutrality** | Apps depend on PSC contracts, not on Drive/iCloud/OneDrive APIs; a plain folder is first-class. | Capability differences are declared and disclosed, not hidden. |
| **G6 Sustainable shared infrastructure** | PSC can be consumed by apps written in different languages on different platforms, maintained over time and distributed lawfully. | PSC prescribes no UI or app architecture; no implementation language is preferred in advance. |

A research question belongs in this plan only if answering it advances one of these goals or tests one of these constraints.

## 2. Where the current research stands

| Report | Goals served | Covers well | Known gaps |
|---|---|---|---|
| [Provider comparison](research/PROVIDER_COMPARISON.md) | G1, G5 | Categories of storage, change feeds, OAuth flows, Drive multi-app risk | Per-provider quotas, pricing, deletion semantics, revocation, account migration; who owns the OAuth app registration; native `drive.file` folder selection; iCloud Drive container sharing |
| [Platform constraints](research/PLATFORM_CONSTRAINTS.md) | G3, G5 | Folder access and background limits on Android/iOS/macOS/Windows | Whether cloud DocumentsProviders/File Providers support directory selection; dot-folder visibility; Linux feasibility criteria |
| [Sync semantics](research/SYNC_SEMANTICS.md) | G1, G3 | Layering, conflict policy by data class, tombstones, lifecycle | No portable data contract or workspace format yet; no fixtures |
| [Security and consent](research/SECURITY_AND_CONSENT.md) | G4 | OAuth for native apps, consent purposes, encryption trade-offs | Shared-folder files as untrusted input; record authenticity; cross-ecosystem key transfer |
| [Calendar integrations](research/CALENDAR_INTEGRATIONS.md) | G2 | Boundary between calendar services and PSC sync | Current permission models and sync-token expiry details |
| [Existing systems](research/EXISTING_SYSTEMS_AND_TECHNOLOGIES.md) | G1, G6 | Patterns from Joplin, Obsidian, any-sync, CRDT libraries | Licenses and maintenance activity; evaluation against a concrete PSC data flow |
| *(none yet)* | G2 | — | Cross-app references, namespaces, ownership enforcement |
| *(none yet)* | G6 | — | Shared-core technology and bindings; licensing and monetization |

## 3. Work packages

Each work package (WP) lists the question, the goals it serves, the deliverable and what "done" means. Proposed deliverable paths are under `docs/research/`.

### WP1 — Provider registration and authorization ownership *(blocking)*

**Goals:** G1, G2, G5 · **Deliverable:** `research/PROVIDER_AUTHORIZATION.md` plus a proof-of-concept report

PSC is a library, not an app. Someone must own each provider registration (Google Cloud project and OAuth clients, Microsoft Entra app, Dropbox app). That choice decides verification burden, quota sharing, user caps for unverified apps, consent-screen branding and whether separate apps can share one workspace.

Questions:
1. Who owns provider registrations: PSC's maintainers, each consuming app, or a family-level registration? What are the operational and legal implications of each, given that a registration is not a PSC-operated backend but does carry obligations?
2. How does a native Android, iOS or desktop app obtain `drive.file` access to an existing folder? Which picker flows are officially supported outside the web?
3. Under `drive.file`, does granting a parent folder grant access to its existing and future children? Does it work across separate OAuth clients in the same project, and across separate projects?
4. Are Drive quotas per project, per user or both, and what do they mean for a family of apps sharing one registration?
5. Apple: how do iCloud Drive ubiquity containers and CloudKit containers behave across apps from the same team? Can separate apps share one iCloud Drive folder?
6. Microsoft Graph and Dropbox: what scopes give least-privilege access to one app folder or user-selected folder, and can several apps share it?

Done when: the multi-app Drive experiment (steps in [Provider comparison §2](research/PROVIDER_COMPARISON.md#2-google-drive)) has run on at least Android plus one desktop OS, and the report recommends one or more registration models with their trade-offs for owner review.

### WP2 — User-selected folder baseline

**Goals:** G1, G3, G5 · **Deliverable:** prototype report appended to `research/PLATFORM_CONSTRAINTS.md`

Questions:
1. Do Google Drive, OneDrive, Dropbox and iCloud expose directory (tree) selection through Android's Storage Access Framework and iOS document pickers, or only single files?
2. How do persisted permissions survive restart, reinstall, folder rename/move and revocation?
3. How do placeholder/unhydrated files behave on Windows, macOS and iOS File Providers?
4. Are dot-folders such as `.psc/` hidden, filtered or rejected by any picker or provider?
5. Which atomic-replace, modification-time and file-identity guarantees does each platform/provider pair actually give?

Done when: the "Required prototype checks" in [Platform constraints](research/PLATFORM_CONSTRAINTS.md#required-prototype-checks) have been run on Android and iOS with at least one cloud-backed provider, and the results are recorded as a capability table.

### WP3 — Portable data contract, workspace format and cross-app interoperability

**Goals:** G2, G4, G5 · **Deliverable:** `research/DATA_CONTRACTS_AND_INTEROP.md`

This is the core of G2 and has no research yet.

Questions:
1. Record envelope: stable record ID, owning app/namespace, schema ID and version, revision context, timestamps, tombstone form.
2. Schema description language and compatibility rules (additive changes, unknown-field preservation, migrations, forward/backward reading).
3. Workspace layout and identity: workspace marker, format version, per-app namespaces, file granularity (avoid hot monolithic manifests).
4. Cross-app references: a stable reference format (for example a URI form `psc://<app>/<type>/<id>`), how a reference resolves, what happens when the target is missing or deleted, and how a reference opens the owning app on each platform (deep links, intents, URL schemes).
5. Read and write permissions between apps: which app may read which namespace. In a plaintext shared folder ownership cannot be enforced by the storage itself. Evaluate convention plus validation, per-app signing of records, per-namespace encryption or other models, and say honestly what each can and cannot guarantee.
6. Human inspectability: which records stay readable (Markdown, JSON) and which may be opaque.

Done when: a draft contract exists with worked examples for one Solstice preference record, one Clock session and one Calendar → Notes reference, and the ownership-enforcement options are compared.

### WP4 — Synchronization protocol semantics and test fixtures

**Goals:** G1, G3 · **Depends on:** WP3 draft · **Deliverable:** update `research/SYNC_SEMANTICS.md` plus a fixture set

Questions: change journal versus state scanning; per-adapter cursors and safe rescans; conditional writes; tombstone retention; per-data-class conflict policy (append-only, field-level, conflict copies, CRDT only where justified); restartable lifecycle; device identity.

Done when: the [proof-of-concept test matrix](research/SYNC_SEMANTICS.md#11-proof-of-concept-test-matrix) is expressed as repeatable, language-neutral fixtures (input workspace states, operations, expected outcomes) that any implementation can be tested against.

### WP5 — Provider capability model and second provider

**Goals:** G5 · **Depends on:** WP1, WP2 · **Deliverable:** capability matrix in `research/PROVIDER_COMPARISON.md`

Questions:
1. The minimum common adapter contract and a capability list (conditional write, change feed, resumable upload, deletion feed, file identity, version history).
2. Whether one second API provider (OneDrive or Dropbox) fits the contract without leaking provider concepts.
3. WebDAV capability probing (RFC 6578 sync-collection, ETags, locking) against at least two independent server implementations.

For every provider, record: supported platforms; required account and consent; least-privilege scopes; whether the user can see and edit stored data; change detection model; concurrency and conflict behavior; deletion semantics; limits, quotas, pricing and policy constraints; revocation and account migration behavior; official documentation URLs and date checked.

Done when: every provider candidate has a complete record, and the second-provider spike confirms or revises the contract.

### WP6 — Security, encryption and consent

**Goals:** G4 · **Deliverable:** update `research/SECURITY_AND_CONSENT.md`

Questions:
1. Shared-folder content as untrusted input: malformed or hostile files, path traversal, Unicode and case collisions, size limits, schema validation before parsing.
2. Record authenticity: can an app or device tell that a record came from its claimed owner?
3. Encryption decision inputs: plaintext versus end-to-end versus per-category; metadata leakage.
4. Key enrollment and recovery across ecosystems (Apple, Google, Windows, Linux) without a PSC server; recovery-key UX; loss scenarios.
5. Consent inventory and UX requirements per app, keeping these separate: (1) cross-device sync, (2) cross-app interoperability, (3) Meridian weather-data contribution, (4) telemetry/analytics, (5) external AI integrations.

Done when: the threat model covers these cases and the encryption options are written up as a decision memo for the owner.

### WP7 — Shared-core technology and host-language bindings

**Goals:** G6 · **Depends on:** WP3 and WP4 drafts (the contract must exist before the technology is chosen) · **Deliverable:** `research/CORE_TECHNOLOGY.md`

The contract is defined language-neutrally first. Only then are implementation options compared, with no option preferred in advance. Candidates include, but are not limited to: a Rust core with generated bindings; Kotlin Multiplatform; a C or C++ core with a stable C ABI; per-platform native implementations validated against the shared fixtures from WP4; and a hybrid with a shared core for the protocol and native adapters for OS capabilities.

Criteria: binding quality and cost for representative consumers (Swift, Kotlin/Java, C#/.NET, TypeScript/JavaScript and others the app family uses); ABI/API stability; binary size; debugging and crash diagnostics; secure-storage and file-coordination interop; testability against the WP4 fixtures; build and distribution; maintenance and contributor pool; license of the toolchain and runtime.

Done when: a short spike implements the same small slice (read workspace marker, apply one fixture) in two or three candidates, is called from at least two host languages, and the comparison is written up. No technology is selected without owner approval.

### WP8 — Host-platform matrix and Linux feasibility

**Goals:** G3, G6 · **Deliverable:** platform matrix in `research/PLATFORM_CONSTRAINTS.md`

Linux synchronization is a conditional target. Before the Linux spike, write measurable go/no-go criteria for owner approval, for example: which WP2/WP4 fixtures must pass on which distributions and providers; an acceptable ongoing maintenance budget; and whether any Linux-only workaround would weaken the portable protocol (which disqualifies it). If Linux sync fails these criteria, drop it from the supported sync matrix; whether a local-only Linux app is still worthwhile is a separate product decision.

### WP9 — Calendar service integrations (separate track)

**Goals:** G2 · **Deliverable:** update `research/CALENDAR_INTEGRATIONS.md`

Compare Google Calendar API, Apple EventKit (including its current permission levels), Microsoft Graph and CalDAV: read-only versus read-write scopes, event ownership, recurrence and exceptions, incremental sync and token expiry, deletion, offline behavior. Define how Calendar shows PSC-synced Clock and Notes records as overlays. Calendar service authorization stays separate from PSC storage authorization.

### WP10 — Solstice first-integration data inventory

**Goals:** G1, G4 · **Depends on:** WP3 draft · **Deliverable:** update `INTEGRATION_SOLSTICE.md`

List candidate Solstice records with units, ranges, schema versions, conflict policy and privacy classification; separate explicit preferences from derived personalization and Meridian learning state; state what stays local and why. Algorithm and app code versions ship through app releases and are never sync data.

### WP11 — Licensing, provenance and monetization

**Goals:** G6 · **Deliverable:** `research/LICENSING_AND_DISTRIBUTION.md`

Compare license options for PSC's own code (permissive, copyleft, dual, proprietary SDK) and distribution or support models, without adding any PSC-operated service. Estimate one-time and recurring costs. Start a provenance inventory and classify dependencies, SDKs, sample code, datasets, fonts, icons and media as allowed, allowed with conditions, or prohibited/unresolved, using current primary-source terms. Check the licenses of any project whose code or protocol PSC might reuse (see [Existing systems](research/EXISTING_SYSTEMS_AND_TECHNOLOGIES.md)) before borrowing anything.

### WP12 — Independent review

**Goals:** all · **Depends on:** WP1–WP6 at least in draft · **Deliverable:** review brief and recorded review outcome

See §6.

## 4. Sequencing

| Phase | Work | Why this order |
|---|---|---|
| **1. Unblock** | WP1 desk research, WP2 prototype, WP3 draft | WP1 can invalidate the shared-workspace model; WP3 defines what everything else moves; WP2 establishes the universal baseline. |
| **2. Prove** | WP1 multi-app experiment, WP4 fixtures, WP5 second provider, WP6, WP10 | Test the contract against real providers and failure cases. |
| **3. Choose how to build** | WP7, WP8, WP11 | Technology, platform matrix and license are chosen for a contract that already exists, not the other way round. |
| **4. Review and decide** | WP12, then owner decisions recorded in [DECISIONS.md](DECISIONS.md) | Findings become decisions only through explicit owner approval. |

WP9 (Calendar) can run in parallel at any phase.

## 5. Rules for all research

- Cite current official documentation with the date checked; label forum posts and blog posts as such.
- Separate facts, test results and assumptions.
- Do not select a CRDT or "last write wins" as a default without showing that the data type needs it.
- Do not request broad provider scopes to avoid an experiment.
- Do not propose any PSC-operated server, relay or account as a shortcut (see [Principles §8](PRINCIPLES.md#8-permanent-decentralization-no-psc-operated-backend)).
- Prototypes are throwaway research code, not approved implementation.

## 6. Independent review brief (Opus)

Ask for an independent architecture and security review of:
- the product boundary and local-first model;
- whether PSC should build a thin coordinator, adopt something like any-sync (only with user-operated nodes), or compose existing storage and merge components;
- the provider registration and authorization model from WP1, including whether Google Drive can serve one shared workspace across separate apps under least privilege;
- whether the folder model should be the universal baseline with direct APIs as optional enhancements;
- the data contract, cross-app references and ownership enforcement from WP3;
- sync protocol and per-data-class conflict semantics, and which categories (if any) need a merge engine;
- consent, encryption, key recovery and token handling;
- platform limitations and the Linux criteria;
- shared-core technology options from WP7;
- licensing, provenance and monetization options that preserve permanent decentralization;
- API quotas, costs and long-term maintenance;
- the smallest experiment that could falsify the proposed layered architecture.

Request cited official documentation, separation of facts from assumptions, identified risks and recommended experiments. Do not ask the reviewer to implement the system, and do not turn its recommendations into decisions without owner review.

## Appendix: initial findings (2026-11-27)

1. **A provider-neutral folder option is possible, but not equivalent across platforms.** Android SAF and iOS document pickers provide user-granted directory access; mobile background execution is opportunistic, not continuous.
2. **Cloud APIs provide better incremental-change metadata than a plain folder**, but each has distinct cursors, revisions, limits and conflict semantics. The provider interface must expose capabilities rather than flatten these differences.
3. **Google Drive is a promising single-app prototype, not yet proven as one shared multi-app workspace.** The least-privilege `drive.file` scope is per-file and per-app.
4. **iCloud Drive is not a universal Android-compatible API.** CloudKit is a separate Apple-specific structured-data service.
5. **OneDrive delta and Dropbox cursors are suitable incremental-sync primitives**; they do not replace PSC conflict, deletion and recovery semantics.
6. **WebDAV is valuable for self-hosted users**, but sync-collection and conditional-write support must be probed per server.
7. **GitHub should remain an advanced version-control option**, not the default sync engine.
8. **Calendar integrations are separate from app-data storage synchronization.**
9. **CRDTs are not a universal solution.** Evaluate Automerge only for genuinely concurrent rich-text or structured editing.
10. **Sync consent, Meridian data contribution and telemetry remain separate purposes.**

The current owner preference is to investigate Google Drive first as the leading managed-provider candidate. This is a research priority only, not a launch-provider decision.
