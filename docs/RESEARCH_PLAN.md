# Research Plan

**Status:** open research agenda · independent Opus review recommended

The goal is to establish a feasible, secure and maintainable architecture before implementation. Research must distinguish documented provider capabilities from assumptions and test results.

## A. Provider and folder capabilities

Evaluate at least:

| Candidate | Questions |
|---|---|
| User-selected local folder | Folder access on Android, iOS, Windows, macOS and Linux; security-scoped access; bookmarks/permissions; file watching; background restrictions |
| Google Drive | OAuth scopes, shared folder ownership, file IDs, change tracking, upload semantics, conflict behavior, quotas and verification requirements |
| iCloud Drive | iCloud Drive file-provider behavior versus CloudKit; platform support; Windows access; app-container limitations; cross-app sharing model |
| OneDrive | Graph API permissions, delta/change tracking, upload sessions, throttling and platform support |
| Dropbox | OAuth scopes, file revisions, delta cursors, conflict and rate-limit behavior |
| WebDAV | Interoperability across servers, locking/ETag support, partial failures, discovery and self-hosted options |
| GitHub | Private repository access, API limits, Git semantics, merge conflicts, binary-file limitations and whether it is suitable only for advanced/version-oriented users |
| Syncthing | Whether PSC should integrate with it directly, or simply respect a folder that Syncthing manages |

For each provider, record:
- supported platforms;
- required account and consent;
- least-privilege authorization scopes;
- whether the user can see and edit the stored data;
- change detection and incremental sync model;
- concurrency and conflict behavior;
- deletion semantics;
- limits, quotas, pricing and policy constraints;
- revocation and account migration behavior;
- official documentation URLs and date checked.

## B. Architecture and synchronization semantics

Investigate:
- Provider-neutral interfaces and capability discovery.
- Local-first data ownership and the boundary between app storage and shared portable data.
- Change journals, manifests, revisions, file IDs and stable record IDs.
- Incremental sync, checkpoints, retries, idempotency and duplicate suppression.
- Concurrent edits and per-domain conflict strategies.
- Tombstones and deletion propagation.
- Multi-device first-run, re-linking and device revocation.
- Partial synchronization and provider outages.
- Large documents, attachments and binary files.
- Schema versioning, migrations and forward/backward compatibility.
- Export, import, restore and provider migration.

Do not select a CRDT or "last write wins" as a default without showing that the data type needs it.

## C. Privacy and security

Research:
- OAuth authorization flows for installed desktop/mobile clients, including PKCE where applicable; secure token storage through each host platform's supported facilities.
- Permission minimization and whether each app needs separate provider authorization.
- Shared provider folder access across applications owned by the same user.
- Encryption at rest and end-to-end encryption options.
- Key generation, backup, recovery and revocation.
- Threat model for lost devices, compromised provider accounts and stale local copies.
- External editing of plaintext Markdown versus encrypted application payloads.
- Metadata leakage (file names, timestamps, sizes, folder structure, access patterns).
- How to explain exactly what syncs and where it goes.

The privacy review must distinguish:
1. user-controlled cross-device synchronization;
2. optional contribution of weather data to improve Meridian;
3. telemetry or analytics;
4. external AI integrations.

These must not share consent or be implicitly enabled together.

## D. Calendar integrations are a separate track

Compare direct service integrations separately from storage providers:
- Google Calendar API;
- Apple EventKit and any relevant iCloud calendar behavior;
- Microsoft Graph / Outlook;
- CalDAV.

Assess read-only and read-write scopes, event ownership, recurring events, incremental updates, deletion, offline behavior and conflict semantics.

PSC's storage provider interface must not be assumed to replace these calendar APIs.

## E. First application integration: Solstice

Evaluate what should travel between Solstice devices:
- explicit recommendation preferences and user-tuned comfort settings;
- recommendation configuration that the user expects to remain consistent;
- derived personalization state that is portable and safe to synchronize;
- weather-source preferences, if appropriate;
- local forecast-error history and per-place corrections (Meridian learning), only if there is a demonstrated need and a clear privacy model.

Do not assume that raw location history, exact coordinates, raw observations, forecast archives or provider credentials should be synchronized.

Algorithm and application code versions are shipped through normal application releases; they are not synchronization data.

## F. PSC integration architecture and host-platform adapters

PSC is shared infrastructure consumed by applications; it is not itself a consumer application and does not define the UI of its clients. This repository must not impose a UI framework, design system, navigation model, or native-versus-web interface rule on applications that integrate PSC. Each consuming project defines those choices independently. Commonplace's own native-app requirements, for example, belong in the Commonplace repository.

Research and prototype the PSC integration surface:
- Platform-neutral, versioned contracts for synchronization, identity/namespaces, provider capabilities, metadata, events and error handling.
- Runtime/library/SDK packaging options and stable bindings for the languages used by consuming apps.
- Host-platform adapters only where OS-specific capabilities are required, including file/document access, secure credential storage, background execution, notifications and permission handling.
- Clear separation between PSC's generic coordination responsibilities and each app's domain logic, UI, local database and user experience.
- Supported host-platform matrix and the level of adapter support each platform needs. Do not assume every platform supports identical background execution or provider features.

Compare implementation approaches such as Kotlin Multiplatform, Rust with stable platform bindings, or platform-specific adapters around shared versioned contracts. Evaluate integration costs for representative client languages and runtimes (for example Swift, Kotlin, C# and others) without treating their UI frameworks as PSC implementation requirements. Consider debugging, packaging, ABI/API stability, testing, security boundaries and maintenance. Do not choose a technology based on language preference alone.

## G. Prototype sequence

1. Compare a user-selected folder with one managed cloud provider.
2. Prove two devices can exchange a small versioned manifest and a sample document.
3. Test interrupted writes, duplicate delivery, concurrent edits, deletion and provider outage.
4. Verify local usability while offline and after authorization is revoked.
5. Prototype one provider-specific adapter without leaking its API into app domain code.
6. Add a second provider only after the interface proves it is genuinely provider-neutral.

## H. Existing systems and reusable technology

Compare existing products and infrastructure before designing a new engine. The initial comparative report is [Existing synchronization systems and reusable technologies](research/EXISTING_SYSTEMS_AND_TECHNOLOGIES.md). It covers Joplin, Obsidian, Anytype/any-sync, Notesnook, Nextcloud, Automerge, Yjs, CouchDB/PouchDB, RxDB and PowerSync.

The current product-owner preference is to investigate Google Drive first as the leading managed-provider candidate. This is a research priority only: it is not a launch-provider decision. The cross-application authorization behavior of a shared Drive workspace is a required proof of concept.

## I. Monetization, licensing, and resource due diligence

Evaluate whether PSC should be monetized or commercially distributed, without assuming that it must be paid or free and without adding a centralized service. Compare suitable possibilities such as permissive or copyleft open-source release, paid/proprietary licensing, dual licensing, paid SDK/distribution, support, or other models only where they fit the product and contribution strategy. Record benefits, disadvantages, obligations, and conflicts with permanent decentralization.

Estimate one-time and recurring costs: maintenance, security response, compatibility testing, documentation, distribution, legal/accounting work, support, provider/API dependencies, optional model usage, and third-party fees. Explicitly distinguish external provider costs from PSC-operated infrastructure; PSC must not acquire a first-party hosted backend or relay to create a revenue stream.

Create a license and provenance review for PSC itself and for every shipped or recommended resource: runtime/build dependencies, platform SDKs, sample code, API integrations, test fixtures, documentation, datasets, models, fonts, icons, media and generated assets. Check exact versions and current primary-source terms. Record commercial-use rights, redistribution and modification rights, attribution, copyleft/source disclosure, patent and trademark clauses, data rights, quotas, and fees. Classify each resource as allowed, allowed with conditions, or prohibited/unresolved. Maintain license notices and an SBOM where practical. Do not select a license for PSC's own code or promise a distribution model until the implications are reviewed.

## J. Opus review brief

Ask Opus for an independent architecture and security review of:
- the product boundary and local-first model;
- whether and how PSC could be monetized without contradicting permanent decentralization;
- the license for PSC's own code, separate from dependency and asset licenses;
- dependency, API, dataset, model, font, icon, media and sample-code provenance, including commercial-use and redistribution obligations;
- provider comparison, especially Google Drive versus iCloud Drive and local folders;
- whether a single shared provider folder can safely serve multiple apps;
- sync protocol and conflict semantics;
- data formats and metadata;
- consent, encryption and token handling;
- platform limitations;
- API quotas, costs and long-term maintenance;
- a minimal proof-of-concept plan.

Request cited official documentation, separate facts from assumptions, identify design risks, and recommend experiments. Do not ask Opus to implement the system or silently turn its recommendations into decisions.

## Initial findings (2026-11-27)

The first provider/platform comparison is recorded in:
- [Provider comparison](research/PROVIDER_COMPARISON.md)
- [Platform constraints](research/PLATFORM_CONSTRAINTS.md)
- [Sync semantics and architecture options](research/SYNC_SEMANTICS.md)
- [Security, authorization and consent](research/SECURITY_AND_CONSENT.md)
- [Calendar integrations](research/CALENDAR_INTEGRATIONS.md)

### Findings that affect the architecture

1. **A provider-neutral folder option is possible, but not equivalent across platforms.** Android SAF and iOS document pickers provide user-granted directory access; mobile background execution is opportunistic, not continuous.
2. **Cloud APIs provide better incremental-change metadata than a plain folder**, but each has distinct cursors, revisions, limits and conflict semantics. The provider interface must expose capabilities rather than flatten these differences.
3. **Google Drive is a promising single-app prototype, not yet proven as one shared multi-app workspace.** The recommended drive.file scope is least-privilege and per-file. Test parent-folder selection, descendants, new files and access from separate application OAuth clients before committing to the family-wide folder model.
4. **iCloud Drive is not a universal Android-compatible API.** It can be used through native File Provider/document access where available, including Windows with iCloud for Windows. CloudKit is a separate Apple-specific structured-data service.
5. **OneDrive delta and Dropbox cursors are suitable incremental-sync primitives.** They do not replace PSC conflict, deletion and recovery semantics.
6. **WebDAV is valuable for self-hosted users**, but RFC 6578 sync-collection and conditional-write capabilities must be probed per server.
7. **GitHub should remain an advanced version-control option**, not the default sync engine.
8. **Calendar integrations are separate from app-data storage synchronization.** Use Google Calendar, EventKit, Microsoft Graph and CalDAV adapters for events; PSC synchronizes Clock/Notes-owned data that Calendar may display as overlays.
9. **CRDTs are not a universal solution.** Evaluate Automerge for genuinely concurrent rich-text/structured editing, not simple preferences or append-only sessions.
10. **Sync consent, Meridian data contribution and telemetry remain separate purposes.**

### Recommended next research sequence

1. Prototype directory access on Android and iOS, including persistent permissions and an external File Provider/DocumentsProvider.
2. Prototype Google Drive for a single app with drive.file and a visible folder.
3. Complete the separate-app shared-folder authorization experiment before assuming the application family can share one Drive folder transparently.
4. Prototype one additional cloud API provider (OneDrive or Dropbox) to test the adapter boundary.
5. Test WebDAV capability detection against at least two independent server implementations.
6. Only then freeze portable contracts, manifest format, conflict policy and a first release scope.

These are research recommendations, not approved implementation work. See the individual reports for official source links and test requirements.

