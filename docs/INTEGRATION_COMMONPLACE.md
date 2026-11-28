# Commonplace Integration

**Status:** lead client · research required · no implementation approved · summarized from the Commonplace repository on 2026-11-28, with owner clarifications

Commonplace is the application family's Markdown-first notes app: notes, moodboards, tasks, reminders and shopping lists, with a spatial desktop canvas and a list view. It is the app that needs PSC the most, so PSC's first research and development are oriented towards it (see [DECISIONS.md](DECISIONS.md)).

Reference repository: [INFORMATION89/Commonplace](https://github.com/INFORMATION89/Commonplace), especially `PREPLAN.md` §4 (data model), §6 (storage and sync, including §6.4 on PSC) and `rules.md` §5.

## Owner clarifications (2026-11-28)

Where Commonplace's planning documents are ambiguous, these take precedence:

- **"Sharing" means the app will be distributed to other people** (for example friends), not that content is shared between people. Each person syncs only their own devices. The consequence for PSC is a higher bar for quality, data safety and easy updates, not a collaboration feature.
- **Sync is one person's own devices:** for example phone → the user's cloud provider → PC.
- **PSC as "backend"** means the shared foundation that all of the owner's apps plug into. It runs on the user's devices; it is never a hosted service.
- **Synced content is simple files:** Markdown, images and maybe JSON.

## Why Commonplace leads

Solstice needs to sync a few small preference files. Commonplace needs much more, so it sets the requirements:

- **Plain files are the source of truth.** Notes are ordinary Markdown files with optional YAML frontmatter that external editors can change. So PSC cannot assume every synced item is a PSC-formatted record. It must handle user-visible files that other tools edit, and keep record identity (a stable note ID in the frontmatter) separate from the file path.
- **Frequent edits on two or more devices.** Edits made offline on the phone and the PC must both survive; on conflict, keep both versions. Overwriting by wall-clock timestamp is forbidden.
- **Images and attachments** linked by relative paths.
- **Deletion and mass-deletion protection.** Tombstones, recoverable versions and conflict copies.
- **Native host languages.** The planned native UIs are SwiftUI (macOS, later iOS), WinUI 3 (Windows) and Jetpack Compose (Android). Linux is open and its sync is conditional. Any PSC core must therefore bind cleanly to Swift, C#/.NET and Kotlin/JVM, which is why Kotlin appeared in earlier drafts. It is one binding target, not a chosen PSC implementation language.

## Candidate data categories (from Commonplace's documents)

Commonplace decides which of these are eligible. None is approved yet.

| Category | Contents | File type and notes for PSC |
|---|---|---|
| Notes | **Markdown.** Body plus frontmatter (stable ID, title, tags, aliases, timestamps); unknown keys preserved | File-based; external edits; conflict copies; IDs survive renames and moves |
| Images / attachments | **Images** referenced by relative path | Larger binaries; resumable upload; file identity. Non-image attachments would need an explicit decision |
| Workspace metadata | **JSON.** Canvas coordinates, zoom, viewport, groups, stacks, pins, saved list views, sort orders and filters, workspace preferences | Kept separate from note prose; sidecar files versus local index is still undecided in Commonplace |
| Tasks and reminders | **Markdown** (tasks) and possibly **JSON** (reminder state). Tasks readable in Markdown; date/time reminder state attached to a note or task | Reminder scheduling stays local and native; only the state may sync |
| Shopping lists | **JSON** or Markdown. Structured items, checked state, quantity, store, cost; a personal index of frequently bought items | Structured records with per-field merge candidates |
| Origin metadata | **Frontmatter or JSON.** Device/platform that created or last edited a note; human-readable device label | Device label kept separate from internal sync IDs; inspectable and removable |
| Location | Only if the user explicitly enables location capture | Never synced silently; separate opt-in |

## Sync review: what should travel and what stays on the device

A first pass, for Commonplace to confirm (WP10 in the [Research plan](RESEARCH_PLAN.md)). The rule of thumb: sync what the person created or deliberately arranged. Keep local what can be rebuilt, what is specific to one device, and anything secret.

**Should sync (portable)**

| Item | Format | Conflict handling | Notes |
|---|---|---|---|
| Note content | Markdown + frontmatter | Keep both versions as a conflict copy | The core of Commonplace; external edits must be detected |
| Images and moodboard images | Image files | Keep both | Largest files; content hash for identity; resumable upload |
| Moodboard and canvas arrangement (positions, groups, stacks, pins) | JSON | Per-item rules (a moved card, a new group); keep both if unsure | Shared across devices so the layout follows the person |
| Saved list views, sorts, filters | JSON | Per-view; keep both if unsure | Small, rarely edited |
| Tasks | Markdown (checkboxes in notes) | Same as note content | Stays readable in other editors |
| Reminder definitions (what and when) | Frontmatter or JSON | Per-reminder | Only the definition syncs; see below |
| Shopping lists and frequently-bought index | JSON (or Markdown) | Per-item merge; checked state needs care | An item checked on the phone in the store must not be undone by the PC |
| Tags | Frontmatter | Union of tags, removals tracked | A tag hierarchy, if adopted, also travels |
| Origin device label | Frontmatter | Last edit wins is acceptable here | Human-readable label only; internal sync IDs are separate |
| Deletions | Tombstones | A deletion beats an older edit only if the edit was seen | Protects against notes coming back and against mass deletion |

**Should stay on the device**

| Item | Why |
|---|---|
| Search index and local database | Rebuilt from the synced files |
| Thumbnails and render caches | Rebuilt; would waste storage and bandwidth |
| Viewport, zoom, window size and position | A phone and a PC need different views; syncing them would fight |
| Scheduled notifications for reminders | Each device schedules its own native notifications from the synced reminder definition. The open question is which devices should fire them, so a reminder doesn't ring on every device. |
| Location data | Only with explicit opt-in, and then as its own category |
| Provider credentials, folder permissions, sync cursors | Device-specific and secret |
| AI tag suggestions | Local and optional, not approved content |
| Local backups and undo history | Recovery belongs to each device; the provider's own version history may add a second layer |

**Questions for Commonplace to settle**
1. Is the canvas layout one shared arrangement, or can it differ per device (for example a phone layout)?
2. Which devices fire a reminder?
3. Sidecar JSON next to each note, or one workspace JSON per area? Many small files are easier to merge; a few larger ones are easier to keep consistent.
4. Size limits for images and other attachments, and whether non-image attachments are in scope (today only Markdown, images and JSON are).
5. Later: mentions of calendar events inside notes (see [Future integrations](FUTURE_INTEGRATIONS.md#3-calendar--commonplace-mentions-possibly-in-both-directions)).

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

1. **Plain files plus PSC metadata.** How does PSC track identity, revisions and deletions for files that external editors may change, without cluttering the user's folder or breaking those editors?
2. **Mixed versions.** People will update the app at different times on different devices. An older device must never corrupt files written by a newer version.
3. **Per-workspace providers.** Commonplace notes that users may want different storage for different workspaces.
4. **Encryption versus editability.** End-to-end encryption conflicts with plaintext Markdown that external editors can read.

## Suggested corrections to Commonplace's own documents

These are for the Commonplace repository; they are recorded here because this session cannot change it.

- `PREPLAN.md` §5.6 and the README describe "small-group sharing" and "shared spaces". Per the owner, these should describe distribution to other users, each syncing only their own devices.
- `PREPLAN.md` §6.4 calls PSC a "shared backend". Clarify that this means a shared on-device foundation all apps plug into, not a hosted service.
- `PREPLAN.md` §6.4 lists "explicitly authorized cross-app references" as a PSC responsibility; with the current scope this is secondary.
