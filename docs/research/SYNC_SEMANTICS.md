# Synchronization Semantics and Architecture Options

**Research date:** 2026-11-27  
**Status:** architecture analysis; no wire protocol or implementation chosen.

> **Scope update (2026-11-28):** PSC syncs one person's own devices and only simple files (Markdown, images, JSON); Commonplace is the lead client. Rows below about calendar events, CRDTs and multi-user editing are background, not current scope. See [DECISIONS.md](../DECISIONS.md).

## 1. Separate the layers

PSC should not be a single "sync everything" database. Separate four responsibilities:

1. **Application domain model** — Solstice, Notes, Clock and Calendar own the meaning and validation of their records.
2. **Portable data contract** — each app defines which records may leave the device, their stable identity, schema version and migration rules.
3. **Synchronization coordinator** — manages pending changes, per-provider cursors, retries, conflicts, deletion state and sync status.
4. **Storage adapter** — translates PSC operations into a folder, Google Drive, Microsoft Graph, Dropbox, WebDAV or another provider's API.

A provider adapter must not decide the meaning of a weather preference, note, Pomodoro session or calendar activity.

## 2. Distinguish file-first data from structured records

Potential classes of synchronized data:

| Data class | Examples | Likely semantics |
|---|---|---|
| Portable documents | Markdown notes and attachments | File/object revisions; preserve original bytes; conflicts retained for review |
| User preferences | Comfort preference, display settings | Small versioned records; field-specific conflict policy |
| Append-only activity | Pomodoro sessions, completed activity history | Immutable records with stable UUIDs; deduplicate by record ID |
| Mutable tasks | Title, status, due date, tags | Structured record with field-level changes and explicit deletion semantics |
| Calendar events | External provider events | Owned by calendar service; use that provider's API rather than copying into PSC as if PSC owns them |
| Derived personalization | A compact learned preference profile | Only sync if the app can explain, version and safely merge it |
| Raw learning history | Forecast logs, observations | Keep local by default; evaluate separately before any portability |

Do not force Markdown, tasks, events and preference settings into one data representation.

## 3. Workspace structure: illustrative only

A user-visible folder may be useful for portability and inspection. This is an example for research, not an approved schema:

    Personal Ecosystem/
      .psc/
        workspace.json
        schemas/
      apps/
        solstice/
          preferences/
        notes/
          notes/
          attachments/
        clock/
          sessions/
        calendar/
          references/

Important constraints:

- The shared folder root has a stable workspace ID and format version.
- Device-local paths, URIs, tokens and OAuth state never go in this folder.
- Every app owns its namespace and record semantics.
- Avoid one monolithic frequently rewritten manifest; it would become a contention hotspot and a single point of failure.
- Do not make a shared folder a database without defining write atomicity, revisions, repair and recovery.

## 4. Incremental synchronization

Each provider exposes different change mechanisms:

- Google Drive uses change-list page tokens.
- OneDrive uses delta links.
- Dropbox uses list-folder cursors.
- WebDAV may support the RFC 6578 sync-collection extension; servers without it may require conservative PROPFIND listings.
- Plain folders may have file watchers, but those notifications can be lost, coalesced or unavailable for remote providers.

PSC should store a provider cursor/checkpoint locally for each combination of account, workspace and adapter. Cursors are provider state, not portable application data. Expired or invalid cursors must trigger a safe rescan rather than data deletion.

Change feeds may report latest item state rather than every intermediate edit. Domain-level audit history must not rely on a provider change feed to preserve every edit.

## 5. Conditional writes and lost-update protection

Where the provider offers revisions, ETags or conditional writes, use them to detect when a remote object changed since it was read.

- Microsoft Graph documents If-Match on upload sessions; an ETag mismatch can return 412 Precondition Failed.
- WebDAV/HTTP provides entity tags and conditional request semantics.
- Dropbox exposes a rev value.
- Google Drive has file metadata and revisions, but the exact update semantics for the chosen API calls must be tested.

When a conditional write fails, re-read the remote version and route the result to the data-type conflict policy. Do not automatically retry by overwriting the new version.

## 6. Conflict policy must be data-specific

| Data type | Candidate behavior | Why |
|---|---|---|
| Immutable activity records | Append and deduplicate by UUID | Independent sessions do not need field merging |
| Simple preferences | Merge independent fields; if the same field changed concurrently, preserve both candidates or use an explicitly approved deterministic rule | A global last-write-wins rule can erase a deliberate setting |
| Markdown document | Conditional update; if the base revision changed, preserve a conflict copy or offer a merge/review UI | External editors and arbitrary Markdown make semantic merge difficult |
| Structured note document | Evaluate CRDT/operation-based model only if concurrent editing is a real requirement | Adds document model, history, migration and interoperability complexity |
| Tasks | Per-field/operation merge with explicit status and delete rules | Task fields can change independently, but completion/deletion may be semantically important |
| Calendar events | Use service event IDs, etags/change keys and the owning calendar API's semantics | Calendar providers already own recurring event and attendee behavior |

Do not use wall-clock timestamps alone as a trustworthy total ordering across devices. Device clocks can drift. A simple deterministic tie-breaker may be acceptable for low-risk fields only after its trade-offs are explicit.

## 7. Deletes and tombstones

A delete is a replicated operation, not merely the absence of a file.

Research and specify:
- stable record identity independent of file path;
- a tombstone with schema version, deletion identifier and causal/revision context;
- how long tombstones remain;
- how stale devices learn that a record was deleted;
- what happens when a user restores an old backup;
- how a provider's remote deletion differs from a local file being temporarily unavailable;
- explicit recovery and undo behavior.

A missing file during a partial folder listing must never be interpreted immediately as a confirmed delete.

## 8. CRDT evaluation: Automerge as a candidate, not a decision

Automerge provides a CRDT document model, a transport-agnostic sync protocol and pluggable networking/storage in its JavaScript ecosystem. Its Swift implementation also exposes document synchronization. Concurrent changes to many independent fields and text/list insertions can be merged, but concurrent writes to the same object property still require a defined winner/conflict representation.

References:
- [Automerge concepts](https://automerge.org/docs/reference/concepts/)
- [Automerge conflicts](https://automerge.org/docs/reference/documents/conflicts/)
- [Automerge glossary](https://automerge.org/docs/reference/glossary/)
- [Automerge Swift synchronization](https://automerge.org/automerge-swift/documentation/automerge/sync/)

### Why not adopt it everywhere immediately?

- Simple settings and immutable Pomodoro sessions do not need a general CRDT document engine.
- A CRDT document may not remain an ordinary editable Markdown file.
- Integration with whichever shared-core technology PSC eventually selects, native storage, compaction, binary format, schema evolution and external editing behavior need an experiment.
- Conflict-free convergence does not decide product semantics for all fields. For example, two different values for one comfort preference still need a meaningful policy.

Prototype Automerge only for a use case that actually needs concurrent rich-text or structured document editing.

## 9. Synchronization lifecycle

A portable implementation should make these states explicit:

1. Local change saved successfully.
2. Change queued for synchronization.
3. Provider authorization and workspace access checked.
4. Remote cursor/change set retrieved.
5. Local and remote revisions compared.
6. Safe updates applied or conflicts preserved.
7. Local changes uploaded conditionally.
8. Uploaded changes verified/reconciled.
9. Cursor checkpoint advanced only after the related work is durably applied.
10. Per-device status updated.

Every stage must be restartable. Avoid moving a cursor forward before downloaded changes are durably applied; otherwise a crash can permanently skip remote records.

## 10. Proposed architecture boundary

A useful future SPI would describe capabilities rather than pretend all providers are identical. Candidate capabilities:

- choose or reconnect a workspace root;
- list/read/write/delete an object;
- retrieve an object revision/ETag;
- conditional write or compare-and-swap;
- incremental change feed;
- resumable upload;
- server-side rename/move;
- reliable deletion feed;
- external file coordination;
- provider-side version history.

An adapter declares which capabilities it has. The coordinator selects a safe strategy based on them.

No concrete interfaces, in any language, should be committed until the provider experiments establish the minimum common contract. The contract should first be described language-neutrally (operations, capabilities, error classes, state machine) and only then bound to implementation languages.

## 11. Proof-of-concept test matrix

For each provider, test:
- initial workspace creation and re-selection on a second device;
- new, changed, renamed and deleted files;
- two devices editing the same object offline;
- external editor changes;
- duplicated events and repeated uploads;
- app termination after download but before cursor commit;
- app termination halfway through upload;
- revoked credentials and re-authorization;
- lost/expired provider cursors;
- network interruption, 429, 5xx and insufficient storage;
- case-sensitive versus case-insensitive filename collisions;
- stale device returning after weeks offline;
- restore from an older backup.

The proof should produce repeatable fixtures and a report, not just a happy-path demonstration.
