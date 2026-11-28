# Glossary

**Status:** working vocabulary · 2026-11-28

| Term | Meaning in this repository |
|---|---|
| **PSC** | Personal Systems Coordinator: shared, provider-neutral infrastructure that consuming apps embed for optional sync and interoperability. Project identifier, not a final consumer brand. |
| **Consuming app** | An application that integrates PSC (currently Solstice, Commonplace, Clock, Calendar). It owns its domain model, UI and local storage. |
| **Meridian** | Solstice's weather engine, including its local forecast-learning behavior and its separate, opt-in weather-data contribution. Not part of PSC. |
| **Provider** | External storage or transport the user chooses: a local folder, Google Drive, iCloud Drive, OneDrive, Dropbox, WebDAV, etc. Always external to PSC. |
| **Adapter** | PSC component that translates PSC operations to one provider and declares that provider's capabilities. |
| **Capability** | A provider property an adapter declares (conditional write, change feed, resumable upload, deletion feed, file identity, version history...). The coordinator chooses strategies based on capabilities. |
| **Coordinator** | The PSC component, running on the user's device inside a consuming app, that manages pending changes, cursors, retries, conflicts and sync status. |
| **Workspace** | The user-selected root (folder or provider location) holding portable PSC data, identified by a workspace marker with a stable ID and format version. |
| **Namespace** | The part of a workspace owned by one app. Only the owning app defines and changes its records. |
| **Record / envelope** | A unit of portable data plus PSC metadata (stable ID, owner, schema version, revision context). |
| **Cross-app reference** | A stable pointer from one app's record to another app's record that resolves without access to the other app's private database. |
| **Cursor / checkpoint** | Device-local, provider-specific position in a change feed. Never portable workspace data. |
| **Tombstone** | A replicated record stating that something was deleted, so stale devices do not resurrect it. |
| **Conflict copy** | Preserved alternative version produced when concurrent edits cannot be merged safely. |
| **Provider registration** | The OAuth client/app registration (e.g. a Google Cloud project) used to request user authorization. Who owns it is an open question (see Research plan WP1). Not a PSC-operated backend. |
| **Calendar service integration** | A connection to an external calendar (Google Calendar, EventKit, Graph, CalDAV). Separate from PSC storage sync. |
