# Commonplace Integration

**Status:** candidate use case · research required · no implementation approved · summarized from the Commonplace repository on 2026-11-28

Commonplace is the application family's Markdown-first notes app: notes, moodboards, tasks, reminders and shopping lists, with a spatial desktop canvas and a list view. It plans to use PSC for cross-device synchronization and family interoperability.

Reference repository: [INFORMATION89/Commonplace](https://github.com/INFORMATION89/Commonplace), especially `PREPLAN.md` §4 (data model), §6 (storage and sync, including §6.4 on PSC) and `rules.md` §5.

## Why Commonplace matters for PSC research

Solstice needs to sync a few small preference records. Commonplace needs much more, and it sets the hardest requirements:

- **Plain files are the source of truth.** Notes are ordinary Markdown files with optional YAML frontmatter that external editors can change. So PSC cannot assume every synced item is a PSC-formatted record. It must handle user-visible files that other tools edit, and keep record identity (a stable note ID in the frontmatter) separate from the file path.
- **Frequent human edits and real conflicts.** Concurrent edits must be detected and both versions kept. Overwriting by wall-clock timestamp is forbidden.
- **Attachments and assets** of arbitrary size, linked by relative paths.
- **Deletion and mass-deletion protection.** Tombstones, recoverable versions and conflict copies.
- **Native host languages.** The planned native UIs are SwiftUI (macOS, later iOS), WinUI 3 (Windows) and Jetpack Compose (Android). Linux is open and its sync is conditional. Any PSC core must therefore bind cleanly to Swift, C#/.NET and Kotlin/JVM, which is why Kotlin appeared in earlier drafts. It is one binding target, not a chosen PSC implementation language.

## Candidate data categories (from Commonplace's documents)

Commonplace decides which of these are eligible. None is approved yet.

| Category | Contents | Notes for PSC |
|---|---|---|
| Notes | Markdown body plus frontmatter (stable ID, title, tags, aliases, timestamps); unknown keys preserved | File-based; external edits; conflict copies; IDs survive renames and moves |
| Attachments / assets | Images and files referenced by relative path | Large binaries; resumable upload; file identity |
| Workspace metadata | Canvas coordinates, zoom, viewport, groups, stacks, pins, saved list views, sort orders and filters, workspace preferences | Kept separate from note prose; sidecar files versus local index is still undecided in Commonplace |
| Tasks and reminders | Tasks readable in Markdown; date/time reminder state attached to a note or task | Reminder scheduling stays local and native; only the state may sync |
| Shopping lists | Structured items, checked state, quantity, store, cost; a personal index of frequently bought items | Structured records with per-field merge candidates |
| Origin metadata | Device/platform that created or last edited a note; human-readable device label | Device label kept separate from internal sync IDs; inspectable and removable |
| Location | Only if the user explicitly enables location capture | Never synced silently; separate opt-in |

Commonplace explicitly requires that no note, attachment, location, credential or private-space content is shared with another app merely because both apps use PSC.

## What Commonplace expects from PSC

From `PREPLAN.md` §6.4:

- **PSC owns:** portable envelopes and manifests, versioned interoperability metadata, provider-adapter boundaries and capability descriptions, generic sync mechanics (checkpoints, revisions, idempotent delivery, retries, sync status), and explicitly authorized cross-app references.
- **Commonplace owns:** note content, identity and semantics, workspace layout, task and reminder behavior, sharing rules, per-data-type conflict policy, and which categories are eligible to sync.
- **Isolation:** every app and data category gets its own namespace and authorization scope. Linking PSC in one app grants nothing to another. Cross-app exchange needs a separate, user-approved purpose.
- **Credentials** stay in platform secure storage. PSC is not an identity provider, token vault or single-sign-on service.
- **Before Commonplace depends on PSC,** PSC must publish an accepted integration contract and a tested proof of concept for the required provider and platform path.
- **Commonplace's phase plan:** a no-op/mock PSC adapter in its local MVP; the first sync through PSC in its private alpha (exit criterion: two devices edit offline and converge without silently losing a note); coexistence with Solstice without namespace collisions or leakage by public beta.

## Open questions this raises for PSC

1. **Plain files plus PSC metadata.** How does PSC track revisions and tombstones for files it does not fully control, without cluttering the user's folder or breaking external editors?
2. **Shared spaces.** Commonplace plans small-group sharing with other people. PSC so far covers one person's own devices. Is multi-person sharing in PSC scope, Commonplace's own concern, or provider-native sharing only? Undecided.
3. **Per-workspace providers.** Commonplace notes that one provider per sync group may not suit users who want different storage for different workspaces.
4. **Encryption versus editability.** End-to-end encryption conflicts with plaintext Markdown that external editors can read.
5. **Wording.** Commonplace's `PREPLAN.md` §6.4 calls PSC a "shared backend/coordination foundation". "Backend" should be read as coordination code running on the user's devices, never a hosted service.
