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
- OAuth for native applications and PKCE; secure token storage on each platform.
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

## F. Native application architecture and desktop-first sequence

The application family will use native UI frameworks rather than Electron or web UI wrappers. Evaluate a shared, platform-neutral domain/core layer separately from platform UI and system adapters.

- Windows UI target: WinUI 3.
- macOS UI target: SwiftUI.
- Android UI target: Jetpack Compose with Motion UI and Material You/Material 3.
- iOS future target: SwiftUI is the candidate native direction.
- Linux: native toolkit/framework remains open; evaluate GTK 4/libadwaita and alternatives if Linux remains in scope.

Desktop is the first development target, but the first desktop OS is deliberately undecided. Compare Windows and macOS based on development environment, native API access, file-provider behavior, background execution, distribution, accessibility, testing, and the ability to validate the shared-core boundary. Do not select an OS by assumption.

Prototype architecture options for shared domain logic and data contracts while preserving native UI. Candidate approaches may include Kotlin Multiplatform, Rust with stable platform bindings, or platform-specific domain implementations around shared versioned contracts. Evaluate actual integration costs for SwiftUI, WinUI 3, Compose/Motion UI, debugging, packaging, testing, and maintenance. Do not choose a technology based on language preference alone, and do not attempt to share UI components across these native frameworks.

## G. Prototype sequence

1. Compare a user-selected folder with one managed cloud provider.
2. Prove two devices can exchange a small versioned manifest and a sample document.
3. Test interrupted writes, duplicate delivery, concurrent edits, deletion and provider outage.
4. Verify local usability while offline and after authorization is revoked.
5. Prototype one provider-specific adapter without leaking its API into app domain code.
6. Add a second provider only after the interface proves it is genuinely provider-neutral.

## H. Opus review brief

Ask Opus for an independent architecture and security review of:
- the product boundary and local-first model;
- provider comparison, especially Google Drive versus iCloud Drive and local folders;
- whether a single shared provider folder can safely serve multiple apps;
- sync protocol and conflict semantics;
- data formats and metadata;
- consent, encryption and token handling;
- platform limitations;
- API quotas, costs and long-term maintenance;
- a minimal proof-of-concept plan.

Request cited official documentation, separate facts from assumptions, identify design risks, and recommend experiments. Do not ask Opus to implement the system or silently turn its recommendations into decisions.
