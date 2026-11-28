# Planned Future Integrations

**Status:** context only · far future · nothing here is approved, scheduled or researched in depth · 2026-11-28

These integrations are recorded so that today's PSC design does not rule them out. They are not deliverables. Current work stays focused on [Commonplace](INTEGRATION_COMMONPLACE.md) syncing one person's own devices with Markdown, images and JSON (see [DECISIONS.md](DECISIONS.md)).

Two kinds of integration appear below, and they place different demands on PSC:

- **Same app, across devices:** one app syncs its own files between a person's devices. This is PSC's core job.
- **Across apps:** one app reads, or links to, another app's data. This needs namespaces, read permissions and a reference format. It is the secondary goal G2 in the [Research plan](RESEARCH_PLAN.md).

## 1. Clock: Pomodoro sync across devices

**Kind:** same app, across devices.

The future Clock app syncs Pomodoro data between a person's devices. "Pomodoro versions" is read here as Pomodoro configurations (presets or variants, such as work/break lengths and cycles), with session history as a possible addition. This should be confirmed when Clock is planned.

What it implies:
- **Presets:** small JSON files, rarely edited. If two devices edit the same preset at once, keep both versions or use simple per-field rules. Deleted presets need tombstones, so they don't come back.
- **Session history (if included):** append-only JSON records with unique IDs. They never conflict; duplicates are removed by ID. Store many sessions per file (for example one file per day or month) so the folder doesn't fill up with tiny files.
- **A running timer** is live device state, not sync data. PSC sync is opportunistic, not real-time, so a timer started on the phone appearing live on the PC is not a promise PSC can make.
- **Nothing new needed:** this fits within the Markdown/image/JSON scope.

## 2. Solstice → Solstice menubar app: sharing personalization data

**Kind:** across apps (both apps belong to the Solstice product).

A future Solstice menubar app (macOS) would use the recommendation-engine data that Solstice has learned about the person, so it can show the same personalized recommendations.

What it implies:
- **Read-only consumer.** The menubar app reads Solstice's namespace and never writes to it. Solstice stays the owner of the data.
- **Same device is often enough.** If both apps are on the same Mac, Apple's shared app-group storage may do the job without PSC at all. PSC is needed only when the data has to come from another device (for example, learned on the phone, shown on the Mac).
- **Cross-app permission.** This is the first real case of one app reading another's namespace. The contract needs a way for the owning app to publish data to named readers, and the person must be able to see and approve that.
- **Privacy.** Personalization data is data about the person. The current Solstice limits still apply: no precise location, raw observations or forecast logs. Only a compact, versioned profile, and only if Solstice decides it is portable.
- **Format.** A versioned JSON profile that both apps understand. A menubar app on an older version must handle a newer profile safely.

## 3. Calendar ↔ Commonplace: mentions, possibly in both directions

**Kind:** across apps.

The future Calendar app lets a person mention a Commonplace note from a calendar item. Possibly the reverse too: a Commonplace note mentions a calendar event.

What it implies:

**Stable identity on both sides**
- Commonplace notes need IDs that survive renames and moves. Commonplace already plans this (an ID in the frontmatter).
- Calendar events usually belong to an external calendar service (Google, Apple, Outlook). Their IDs are that service's IDs, not PSC IDs. A reference to an event must therefore say which service, account and calendar it came from. It will only resolve on devices where that calendar is connected in the Calendar app.

**Where each mention is stored**
- Each app stores the mentions it makes in its own files. Calendar → note mentions live in Calendar's own JSON. PSC must not write into external calendar events. Note → event mentions live in the Commonplace note, for example as a link in the Markdown or a frontmatter field.
- **Mutual** does not have to mean both sides store the link. One side can store it, and the other side shows it as a backlink by reading an index. That avoids keeping two copies in step, but needs cross-app reading (below).

**What each app can see**
- To show a mention, Calendar needs at least the note's title and whether it still exists. That means a narrow, approved read of Commonplace data. The options are a small published index of note IDs and titles, or Calendar opening the note only through Commonplace (a deep link).
- The person must approve this. Calendar seeing note titles is a separate permission from syncing.

**Broken links**
- Notes get deleted, events get cancelled, and calendars get disconnected. A mention must show a clear "missing" state, never crash, and never resurrect deleted data.

**Portability**
- A link like `psc://commonplace/note/<id>` inside Markdown should stay readable in other editors, even though it won't work there.
- Opening a mention should launch the owning app (URL schemes, intents, deep links) on each platform.

**Scope boundary**
- Connecting to Google Calendar and the like remains the Calendar app's job. PSC only syncs the app-owned files that hold mentions and indexes.

## What today's design must keep possible

These are design constraints for the current work (WP3 in the [Research plan](RESEARCH_PLAN.md)), not extra deliverables:

1. Stable IDs for every synced file, independent of its path.
2. Per-app namespaces in the workspace, with a later option for an owner app to publish read-only data to named apps.
3. A reference format that can point to PSC-synced files and to external IDs (such as calendar events), with an explicit "unresolved" state.
4. JSON formats that tolerate older and newer app versions.
5. Append-only, ID-deduplicated JSON as a supported pattern (Clock sessions).
