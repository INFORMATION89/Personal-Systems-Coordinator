# Calendar Integrations Are Separate From PSC Storage Sync

**Research date:** 2026-11-27  
**Status:** out of PSC scope · handed to the future Calendar app (decision 2026-11-28). Kept as boundary notes only; PSC does no further calendar-service research.

Calendar is a product in the application family, but connecting a calendar account is a different problem from synchronizing our own app-owned data through a storage folder.

## 1. Two independent connections

### PSC data synchronization

Examples:
- Clock publishes Pomodoro sessions.
- Notes owns tasks and documents.
- PSC synchronizes eligible application-owned records through a user-selected provider.
- Calendar reads those records as independent activity/task/note layers.

### External calendar integration

Examples:
- The user connects Google Calendar.
- The user grants Calendar access to Apple calendars on the device.
- The user connects Outlook through Microsoft Graph.
- The user connects a CalDAV account.

These services own events, recurring events, attendee state, invitations and calendar-specific change semantics. Calendar should use their APIs rather than copy events into the PSC file workspace and claim ownership.

## 2. Candidate adapters

### Google Calendar API

Use Google Calendar API for Google accounts. Evaluate event listing with incremental synchronization, event IDs, etags, sync tokens, read-only versus read-write scopes, recurring events and deleted-event behavior.

Official documentation: [Google Calendar API](https://developers.google.com/calendar/api/guides/overview).

### Apple EventKit

On Apple platforms, EventKit provides access to the user's calendars and reminders with system permission. It is an OS-native integration, not an iCloud Drive storage adapter.

Official documentation:
- [EventKit](https://developer.apple.com/documentation/eventkit)
- [Requesting access to event data](https://developer.apple.com/documentation/eventkit/requesting_access_to_events_and_reminders)

### Microsoft Graph / Outlook

Use Microsoft Graph calendar APIs for Microsoft accounts. Review delegated permissions, calendarView/delta where supported, event change keys/ETags, recurring event exceptions and throttling.

Official documentation: [Microsoft Graph calendar API](https://learn.microsoft.com/en-us/graph/api/resources/calendar).

### CalDAV

CalDAV is a standard calendar-access protocol built on WebDAV and iCalendar. It can support user-controlled and self-hosted calendar providers, but server interoperability must be tested.

Standard: [RFC 4791 — Calendaring Extensions to WebDAV](https://www.rfc-editor.org/rfc/rfc4791.html).

## 3. Ownership and cross-app references

- A Google Calendar event remains owned by Google Calendar.
- An Apple calendar event remains owned by the selected calendar account.
- A Pomodoro session remains owned by Clock.
- A Notes task remains owned by Notes.
- Calendar may render all of them in separate visual layers and expose links/actions, but should not turn all source data into generic calendar events.

PSC may synchronize app-owned activity records that Calendar consumes. It does not replace external calendar APIs.

## 4. Required product decisions

- Read-only access or read/write event management for each provider.
- Which calendars and accounts are selected.
- How external event IDs map to local cache records.
- How recurring events, exceptions, deleted events, time zones and all-day events are represented.
- Whether tasks/activities are displayed as overlays, not events.
- How duplicate or linked records are recognized.
- Permissions and consent independently from PSC storage sync.
