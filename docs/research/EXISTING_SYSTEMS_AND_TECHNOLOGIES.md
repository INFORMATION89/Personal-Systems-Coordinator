# Existing Synchronization Systems and Reusable Infrastructure

**Research date:** 2026-11-27  
**Status:** comparative research; no implementation or dependency decision approved

## Purpose

Determine whether Personal Systems Coordinator (PSC) should build a synchronization engine from scratch, adopt an existing system, or compose existing technologies behind a PSC-owned interoperability layer.

The target is broader than syncing files for one application. PSC is intended to support independent applications with separate domain models, user-selected storage, local-first operation, cross-device continuity and carefully controlled cross-app data exchange.

## Executive summary

No reviewed project clearly provides the complete combination of requirements established for PSC. Existing products demonstrate useful patterns, while several libraries and protocols solve narrower technical problems.

The most promising architectural direction to investigate is **a thin PSC coordination and interoperability layer over existing storage providers and selectively reusable synchronization components**, rather than immediately building a complete storage service or adopting one product's full architecture.

Google Drive currently appears to be the most promising first managed-cloud provider to investigate, based on its established API, incremental change tokens, broad user familiarity and the possibility of using a visible user-controlled folder. This is a research preference, not an approved provider decision. The shared-folder authorization model across separate application identities remains a blocking proof-of-concept question.

## 1. Existing applications and products

### Joplin

Joplin is a useful reference for separating application data from synchronization targets. It supports multiple synchronization destinations, including filesystem, WebDAV, Nextcloud, Dropbox, OneDrive and S3-compatible storage, as well as its own service.

**What PSC can learn:**
- Keep synchronization-target-specific code behind adapters.
- Treat the provider as a destination/transport rather than the owner of application semantics.
- Support self-hosted and user-controlled storage alongside managed providers.

**Limitations as a direct PSC foundation:**
- Joplin is a note-taking product with its own data model and synchronization assumptions.
- Its application-level protocol is not automatically a generic cross-application interoperability contract.

References:
- https://joplinapp.org/help/apps/sync/
- https://github.com/laurent22/joplin

### Obsidian

Obsidian stores notes as local Markdown files in a user-selected vault. Users can combine this with operating-system cloud folders or external synchronization tools; Obsidian also offers its own Sync service.

**What PSC can learn:**
- User-visible files and folders make data ownership understandable.
- Local files preserve useful interoperability with external tools.
- The product must clearly warn against running multiple independent synchronization systems over the same files when that can cause conflicts.

**Limitations:**
- A folder-based model alone does not define structured cross-app contracts, portable identities, conflict policies or consent boundaries.
- File synchronization should not be confused with application-level interoperability.

References:
- https://help.obsidian.md/sync
- https://help.obsidian.md/Files+and+folders/How+Obsidian+stores+data

### Anytype / any-sync

Anytype's any-sync project is a more infrastructure-oriented reference. It describes a synchronization protocol and SDK ecosystem for encrypted, replicated application data.

**What PSC can learn:**
- A reusable synchronization protocol and SDK can serve as a foundation for an application ecosystem.
- Data synchronization, local querying and application-facing APIs can be designed as distinct layers.
- End-to-end encryption and peer-oriented synchronization are possible design dimensions.

**Limitations and questions:**
- any-sync has its own architecture, data model and operational requirements, including sync/file nodes. It is compatible with PSC's permanent constraint only if those nodes are user-chosen and user-operated (or otherwise external to PSC); PSC must never run them.
- It is not equivalent to arbitrary BYOS storage over Google Drive, iCloud Drive, Dropbox or a local folder.
- Maturity, licensing, platform support, operational complexity and compatibility with PSC's app-owned domain models require a dedicated technical review before adoption.

References:
- https://sync.any.org/
- https://github.com/anyproto/any-sync

### Notesnook

Notesnook is an example of an application using its own hosted synchronization service with client-side encryption.

**What PSC can learn:**
- Local encryption and explicit synchronization state can be central product properties.
- A managed service can simplify device discovery and synchronization behavior.

**Why it is not the target model by itself:**
- A first-party hosted service is excluded by PSC's permanent constraint: PSC will never operate a backend, relay or account system.

References:
- https://notesnook.com/
- https://github.com/streetwriters/notesnook

### Nextcloud

Nextcloud provides user-operated or hosted file storage and synchronization, with desktop and mobile clients and WebDAV access.

**What PSC can learn:**
- WebDAV and folder-oriented storage can serve self-hosted and user-controlled deployments.
- PSC should consider Nextcloud as a provider/service target, not assume it replaces application-level synchronization semantics.

References:
- https://docs.nextcloud.com/server/stable/user_manual/en/files/access_webdav.html
- https://nextcloud.com/

## 2. Reusable synchronization technologies

These technologies solve different layers and should not be treated as interchangeable provider adapters.

| Technology | Main problem addressed | Potential PSC role | Important limitation |
|---|---|---|---|
| Automerge | Concurrent changes to structured documents, history and merge behavior | Optional data-type-specific conflict engine | Not a storage provider or complete cross-app sync system |
| Yjs | Shared data structures and collaborative editing | Rich-text or real-time collaboration component | Requires transport/persistence integration; not a generic BYOS layer |
| CouchDB / PouchDB | Replication between databases, including offline clients | Pattern reference; possible only against a user-operated CouchDB | Introduces database/document-model assumptions; a replication server would have to be user-chosen and user-operated, never PSC-operated |
| RxDB | Local database with replication plugins | Candidate for structured local-first app data | Not a universal provider abstraction; assess platform/runtime fit |
| PowerSync | Local database synchronization with a backend | Design reference only | Requires a backend service; incompatible with PSC's permanent no-backend constraint |
| any-sync | Encrypted replicated data protocol and SDK | Potential candidate for deeper architecture evaluation | Distinct operational model; BYOS compatibility and maturity need proof |

References:
- https://automerge.org/
- https://docs.yjs.dev/
- https://pouchdb.com/
- https://rxdb.info/
- https://www.powersync.com/
- https://sync.any.org/

## 3. What these systems collectively demonstrate

1. **Provider adapters are viable.** Joplin demonstrates multiple storage destinations behind an application-level sync feature.
2. **User-visible local data is viable.** Obsidian demonstrates the usability and interoperability benefits of ordinary files.
3. **A reusable protocol/SDK is viable in principle.** any-sync demonstrates a more general infrastructure approach, although its fit is unproven.
4. **Conflict resolution is data-type-specific.** Collaborative document engines should not be imposed on preferences, append-only activity records or every other data category.
5. **Storage and interoperability are separate concerns.** A file provider can move bytes but cannot decide which application owns a record, what another app may read, or how a portable cross-app reference behaves.

## 4. Preliminary direction for PSC

Investigate a layered composition:

- **Application domain layer:** each app owns its canonical model and local behavior.
- **Portable data contract:** defines explicitly exportable/synchronizable records, stable IDs, schema versions and cross-app references.
- **PSC coordinator:** manages workspace identity, sync scheduling, checkpoints, retries, consent policies and app/provider boundaries.
- **Provider adapters:** local folders, Google Drive, OneDrive, Dropbox, WebDAV and optional external folder-sync tools.
- **Optional specialized engines:** Automerge or another merge engine only for data categories that demonstrably need concurrent-edit semantics.

This is a hypothesis to evaluate, not a finalized architecture. PSC should not embed a large database or CRDT merely because it exists.

## 5. Google Drive as the leading managed-provider candidate

The project owner currently considers Google Drive the most promising provider to investigate first.

Reasons to prioritize a proof of concept:
- It offers a mature API and incremental change tracking.
- It supports user-visible files and folders.
- It is broadly familiar and can be evaluated without operating PSC's own cloud.
- It can provide a useful test of whether provider-specific APIs can remain behind a portable PSC adapter.

Important unresolved risks:
- The least-privilege `drive.file` authorization model must be tested across separate PSC client applications.
- Do not assume that a folder selected or authorized by Solstice automatically becomes accessible to Notes or Clock.
- Test whether app B can select the same shared folder, list existing and future children, create a file, and have app A observe and read it.
- Repeat across two devices, reauthorization and app reinstall scenarios.
- Assess OAuth verification, consent UX, quotas, change-token recovery, conflict handling and account migration.
- Do not request broader Drive permissions simply to avoid the experiment without a security and policy review.

Relevant official documentation:
- https://developers.google.com/workspace/drive/api/guides/about-changes
- https://developers.google.com/workspace/drive/api/guides/api-specific-auth
- https://developers.google.com/workspace/drive/api/guides/appdata
- https://developers.google.com/workspace/drive/picker/guides/overview

**Conclusion:** Google Drive is the current first candidate for a managed-provider proof of concept, not a selected launch provider and not yet validated as a shared workspace across independent applications.

## 6. Questions for independent Opus review

The review questions from this report have been merged into the single review brief in [Research plan §6](../RESEARCH_PLAN.md#6-independent-review-brief-opus).

## 7. Recommended next experiments

1. Build a small Google Drive multi-app authorization proof of concept before designing a family-wide shared workspace.
2. In parallel, prototype a user-selected folder on Android and iOS to validate the portable workspace-marker and manifest approach.
3. Compare one additional direct API provider (OneDrive or Dropbox) to test whether PSC's adapter contract is genuinely provider-neutral.
4. Evaluate any-sync, Automerge and CouchDB/PouchDB against one concrete PSC data flow rather than comparing them only by feature lists.
5. Ask Opus to review this report together with the existing provider, platform, sync-semantics and security reports.

No implementation dependency, protocol, provider order or public contract is approved by this report.
