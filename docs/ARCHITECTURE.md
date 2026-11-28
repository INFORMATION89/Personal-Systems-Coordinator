# PSC Architecture and Design Decisions

**Status:** design draft · owner decisions D1–D7 answered 2026-11-28 · becomes binding at **Design Freeze** (see `IMPLEMENTATION_PLAN.md`)
**Prepared with:** Claude Code, tier O (design only; no code). Owner review pending.
**Scope:** the first viable product: PSC syncing **Commonplace** between one person's devices.

This document decides how PSC is built. Technical choices are made here, with reasons, so that coding sessions follow them instead of improvising. Choices that change the whole structure of the project are listed in §1 for the owner, each with pros and cons and a recommendation. Nothing here is coded until Design Freeze.

**How to read it:** §1 asks for the owner's decisions. §2–§4 describe what PSC is and how the workspace looks. §5–§9 are the technical design. §10–§11 cover quality and what is deliberately left out.

---

## 1. Decisions for the owner

Each of these affects the whole project. **All seven were answered on 2026-11-28:**

| Decision | Owner's answer |
|---|---|
| D1 Core language | **Rust** |
| D2 First desktop OS | **macOS** (also Commonplace's first desktop OS) |
| D3 First phone | **Android** |
| D4 Encryption in v1 | **Plain files** |
| D5 If Drive fails E1 | **GitHub first**: GitHub is the first online route; Drive follows if E1 passes |
| D6 License | **Apache-2.0**; interim clean-room rules become the permanent policy |
| D7 Repository | **Open source (public)**, so users can see how their data is processed |

The options and their trade-offs are kept below as the record of why.

### D1. Core language: Rust

The owner is leaning towards Rust.

| | Rust (recommended) | Kotlin Multiplatform (Meridian's choice) | Separate native code per platform |
|---|---|---|---|
| **Pros** | One core for every platform, including C# on Windows. Strong safety guarantees for file and sync code. Excellent libraries for HTTP, JSON, SQLite, OAuth and hashing. Small native libraries with no runtime. Well suited to AI-assisted coding, because the compiler and linter catch many mistakes before a human sees them. | Same toolchain as Meridian. Very good on Android and the JVM. | Each platform uses its natural language. |
| **Cons** | Bindings must be generated for Swift, Kotlin and C#; C# relies on a younger third-party generator. Longer compile times. | Weak fit for C#/WinUI 3 on Windows, which Commonplace plans. Kotlin/Native on Apple platforms is heavier. | Three implementations of the same sync logic: three times the bugs and maintenance. Contradicts "maintainable". |

**Affects:** §6, §8, and all build tasks.

### D2. First desktop operating system (shared with Commonplace)

| | Windows first | macOS first |
|---|---|---|
| **Pros** | Matches "my PC", if the owner's computer runs Windows. Cheaper CI (Windows runners cost less than macOS). Windows Credential Manager is simple. | Apple's file coordination and Keychain are mature. iOS later shares the Swift binding. |
| **Cons** | Depends on the C# generator, which is the riskiest binding. | Needs a Mac for builds and testing. CI runners are about 10 times the Linux cost on private repositories. |

**Recommendation:** the operating system the owner uses every day, because the owner is the first tester. **Affects:** build order (§8.4).

### D3. Phone platform for the first release

The goal "my phone syncs to the cloud, then to my PC" needs a phone in the first release.

| | Android (recommended if the owner's phone is Android) | iPhone |
|---|---|---|
| **Pros** | Commonplace already plans Android (Jetpack Compose). Can be tested on an emulator in CI. | Large audience. |
| **Cons** | — | Commonplace schedules iOS later. Needs a Mac, an Apple developer account (annual fee) and a device. |

**Affects:** §8.4 and the build order.

### D4. Encryption in the first release

| | Plain files (recommended for v1) | End-to-end encryption |
|---|---|---|
| **Pros** | Notes stay readable Markdown in Drive, GitHub or any editor, which is Commonplace's core promise. Simple recovery: no keys to lose. Much less code. | The provider cannot read the content. |
| **Cons** | Google, GitHub or the WebDAV host can technically read the files. | Files are unreadable outside the app. Losing the key means losing the data. Key sharing between devices with no server is complex. |

**Recommendation:** plain files in v1, stated clearly in each app's onboarding. The design keeps room for optional per-app encryption later (§10). **Affects:** §3 and §7.

### D5. What happens if Google Drive fails experiment E1

Experiment E1 (`IMPLEMENTATION_PLAN.md`, step A1) tests whether two sign-in clients in one Google project can see the same files. If they can't, Commonplace on a phone and on a PC cannot share files through Drive under the least-privilege permission.

| Option | Pros | Cons |
|---|---|---|
| **a. Ship v1 with GitHub, WebDAV and folder; add Drive later** (recommended) | No compromise on privacy or cost | No average-user provider in v1 |
| b. Request broad Drive access | Drive works | Google's restricted-scope review, a paid yearly security assessment (about US$540 a year in one community report), and access to the user's whole Drive |
| c. Add Dropbox or OneDrive as the average-user provider | Both have app folders that very likely work | One more provider to build and maintain; previously deferred |

Decide now, so the experiment's result leads straight to a plan.

### D6. PSC's license and clean-room policy

Commonplace may be a paid app, and it embeds PSC.

| | Apache-2.0 (recommended) | Proprietary (private) | MPL-2.0 |
|---|---|---|---|
| **Pros** | Allows use in a paid, closed app. Includes a patent grant. Same license as Meridian. Easy to accept dependencies. | Full control; nobody else can use PSC. | Changes to PSC's own files must stay open, while apps can stay closed. |
| **Cons** | Others may reuse PSC, including commercially. | Others can't contribute or audit it. Harder to accept outside help. | More obligations to track. |

**Recommendation:** Apache-2.0, with the interim clean-room rules (no copying, provenance records) adopted as the permanent policy. A formal two-step clean-room process is not needed for this project. **Affects:** `CLEAN_ROOM.md`, the LICENSE file and the dependency policy (§9.3).

### D7. Repository visibility and CI budget

| | Public repository | Private repository |
|---|---|---|
| **Pros** | Free CI minutes, including macOS and Windows | Code stays private |
| **Cons** | Code is visible to everyone | macOS and Windows CI minutes count against the plan, at higher rates than Linux |

**Recommendation:** private while building, if the budget allows Windows CI; public at release if D6 is Apache-2.0.

---

## 2. What PSC is

- **A Rust library** embedded in each app. No server, no account, no UI.
- **It syncs one person's app folders** between their devices through storage they choose: Google Drive, GitHub, a WebDAV server or a local folder.
- **It syncs files, not app data structures.** PSC never parses notes. It treats files as bytes with a type, size and hash. Commonplace's note IDs, frontmatter and layout JSON are Commonplace's business.
- **It gives apps shared information:** which devices and apps belong to the workspace, sync status, and (later) data an app chooses to publish for other apps.

## 3. The workspace (decided by the owner: PSC folder plus one folder per app)

What the user sees in Google Drive, the GitHub repository, the WebDAV server or the chosen folder:

```
Personal Systems Coordinator/
├── PSC/                              ← PSC's own folder; managed by PSC
│   ├── README.txt                    ← "Managed by Personal Systems Coordinator. Do not edit."
│   ├── workspace.json                ← workspace ID, format version, creation date
│   ├── apps/
│   │   └── commonplace.json          ← app registry entry: name, folder, format version, what it publishes
│   ├── devices/
│   │   └── <device-id>/
│   │       └── commonplace.json      ← device label, platform, app and PSC versions, last sync
│   └── tombstones/
│       └── commonplace/
│           └── <device-id>.jsonl     ← deletions made by that device
├── Commonplace/                      ← Commonplace's folder; only Commonplace's own files
│   ├── <notes>.md
│   ├── <images>
│   └── <layout and view files>.json
└── Solstice/                         ← later
```

**Rules**
1. **Single writer per file in `PSC/`.** Every file in `PSC/` is written by exactly one device and app (or once, at creation, for `workspace.json`). So PSC's own metadata never conflicts.
2. **Each app writes only in its own folder** and its own entries in `PSC/`. PSC enforces this for everything it writes. It cannot stop other tools from writing, so it tolerates and reports unexpected files.
3. **The `PSC` folder is visible, not hidden.** Some file pickers and providers hide or reject dot-folders.
4. **Folder names:** the root is always `Personal Systems Coordinator`. Each app's folder name is set by the app at registration and recorded in its registry entry. PSC refuses a name already registered by another app.
5. **Allowed content in app folders:** Markdown (`.md`), JSON (`.json`) and images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.heic`, `.svg`). The list is configuration, not code (§9.2). Other files are ignored and reported in the status.
6. **Ignored names:** operating-system and editor clutter (`.DS_Store`, `Thumbs.db`, `desktop.ini`, `~$*`, `*.tmp`, `.~lock.*`). Also configuration.
7. **Where the root lives, per route:**

| Route | Location |
|---|---|
| Google Drive | PSC creates `Personal Systems Coordinator` in My Drive (created by the app, so it is visible under `drive.file`) |
| GitHub | The root of a private repository the user chooses (PSC refuses public repositories) |
| WebDAV | A folder the user chooses on the server; PSC creates the root inside it |
| Local folder | A folder the user chooses; PSC creates the root inside it |

### JSON formats (v1)

All PSC JSON files carry `"format": <integer>` and `"min_reader_format": <integer>`. Timestamps are UTC in RFC 3339. Unknown fields are always preserved when rewriting.

`PSC/workspace.json`:
```json
{ "format": 1, "min_reader_format": 1, "workspace_id": "<uuid>", "created_at": "<rfc3339>", "created_by_app": "commonplace" }
```

`PSC/apps/<app-id>.json`:
```json
{ "format": 1, "min_reader_format": 1, "app_id": "commonplace", "display_name": "Commonplace",
  "folder": "Commonplace", "app_format": 1, "published": [] }
```

`PSC/devices/<device-id>/<app-id>.json`:
```json
{ "format": 1, "min_reader_format": 1, "device_id": "<uuid>", "label": "My Mac", "platform": "macos",
  "app_version": "1.0.0", "psc_version": "1.0.0", "last_sync_at": "<rfc3339>" }
```

`PSC/tombstones/<app-id>/<device-id>.jsonl`, one JSON object per line:
```json
{ "path": "notes/old.md", "content_hash": "sha256:<hex>", "deleted_at": "<rfc3339>" }
```

The exact JSON Schemas are written as files under `spec/` in step A7 and are part of Design Freeze.

## 4. Cross-app information

What "PSC can give the information needed to other apps" means in v1:
- `list_apps()` reads the registry: which apps use the workspace, their folders and versions.
- `list_devices()` reads the device files: which devices sync, and when each last synced.
- `status()` reports this app's sync state.

**Publishing data to other apps** (for example a note index that Calendar can read) is designed but not built in v1: an app lists files in `published` in its registry entry, together with the app IDs allowed to read them. PSC would offer `read_published(app_id, name)`, refusing apps not listed. This is a cooperative rule between the owner's own apps, not a security boundary, because anyone with the storage account can read every file.

## 5. How sync works

### 5.1 Model

- **Each app's local folder is the source of truth on that device.** Commonplace keeps reading and writing ordinary files in its own local folder (for example its notes vault). PSC keeps that folder in step with the app's folder in the workspace.
- **State-based, three-way comparison per file.** For each file path PSC stores, on the device, the **base**: the content hash and provider revision at the last successful sync. Each cycle compares base, local and remote:

| Local vs base | Remote vs base | Action |
|---|---|---|
| Same | Same | Nothing |
| Changed | Same | Upload, only if the remote is still at the base revision (conditional write) |
| Same | Changed | Download to a temporary file, check its hash, replace atomically |
| Changed | Changed, same content | Record the new base; nothing to transfer |
| Changed | Changed, different content | **Conflict** (§5.3) |
| Deleted | Same | Delete remotely, write a tombstone |
| Same | Deleted (confirmed) | Delete locally |
| Deleted | Changed | **Keep the remote version.** An edit beats a deletion, so nothing is lost |
| Changed | Deleted | **Keep and re-upload the local version** |

- **Hashes are SHA-256** of the file's bytes, written as `sha256:<hex>`.
- **No CRDTs and no last-write-wins.** Wall-clock time is never used to decide which version survives.
- **No device-to-device messages.** Devices only see each other's changes through the storage.

### 5.2 Sync cycle

1. Take the device-local sync lock for this app and workspace (only one sync at a time).
2. Scan the local folder: compare size and modification time with the local index, and hash anything that changed.
3. Ask the adapter for remote changes since the stored checkpoint (a change feed where available; otherwise a listing).
4. Read new tombstones from other devices.
5. Classify every changed path using the table above.
6. Apply downloads and local deletions. Each download goes to a temporary file, is hash-checked, then atomically renamed into place.
7. Apply uploads and remote deletions with conditional writes. If a conditional write fails because the remote moved on, re-read that file and classify it again; never overwrite.
8. Write this device's tombstones and device file.
9. **Advance the base and checkpoint only after everything above is durably done.** A crash at any point leaves a state the next cycle can safely resume from.
10. Release the lock and publish a sync report (counts, conflicts, errors, next suggested sync time).

The host app decides **when** to sync: on app start, after edits (debounced), on a timer while open, and when the operating system allows background work. PSC accepts a time budget and a cancellation token.

### 5.3 Conflicts

When both sides changed the same file differently:
- The version **already in the workspace keeps the original name.**
- The local version is saved next to it as **`<name> (conflict <device label> <YYYY-MM-DD HHmm>).<ext>`** and uploaded like any other new file.
- Both devices end up with both files. The app can show them to the user; deleting the unwanted copy is an ordinary delete.
- The pattern is fixed by the format, so it is the same on every device and language. The device label comes from the host app.

### 5.4 Deletions and safety guards

- **Confirmed deletes only.** A file missing from a remote listing counts as deleted only if the listing is complete (an adapter capability) or a tombstone confirms it. A partial or failed listing never deletes anything.
- **Tombstones** are kept for **90 days** (configuration). A device offline for longer does a safe full reconcile: it re-uploads what it has instead of applying deletions it can no longer verify. Resurrecting a file is preferred over losing one.
- **Mass-deletion guard:** if a cycle would delete more than **25% of an app's files, or more than 50 files** (configuration), PSC pauses and reports `confirmation_required`. The app asks the user before continuing.
- **Newer formats:** if `workspace.json` or a registry or device file has a `min_reader_format` higher than this PSC version supports, PSC stops syncing that workspace and reports `update_required`. It never writes to a newer format it doesn't understand.

### 5.5 Renames

v1 treats a rename as a delete plus an add. When the local scan sees a file disappear and one with the same hash appear in one cycle, PSC uses the provider's server-side move where available, to avoid re-uploading.

### 5.6 Mixed routes

A workspace is bound to one route. All devices must reach it the same way (for example, all through the Drive API, never the Drive API on one device and the Drive for desktop folder on another). PSC records the route in its device-local state and refuses to combine routes, reporting `route_mismatch`.

## 6. Code structure (Rust)

A Cargo workspace:

| Crate | Responsibility | Depends on |
|---|---|---|
| `psc-core` | Domain types, sync engine (§5), conflict and deletion rules, format handling. **No network or provider code.** | `psc-state`, adapter trait |
| `psc-state` | Device-local state in SQLite: index, bases, checkpoints, lock, route, device ID | `rusqlite` |
| `psc-adapter` | The `StorageAdapter` trait and capability flags; a fault-injecting in-memory adapter for tests | — |
| `psc-folder` | Local folder adapter | `psc-adapter` |
| `psc-webdav` | WebDAV adapter (thin client: PROPFIND, GET, PUT, DELETE, MKCOL, MOVE) | `psc-transport` |
| `psc-gdrive` | Google Drive adapter (thin REST client for the endpoints used) | `psc-transport` |
| `psc-github` | GitHub adapter (Git data API for batched commits; contents and trees for reading) | `psc-transport` |
| `psc-transport` | HTTP client, retries and backoff, OAuth flows, credential handling | `reqwest`, `oauth2` |
| `psc-ffi` | The public API exported through UniFFI (§8) | all of the above |
| `psc-cli` | Developer and sample command-line tool; also the standalone sample consumer | `psc-ffi` API |
| `psc-testkit` | Fixture runner, fake clock, fake adapter, test helpers | — |

**Adapter capabilities** (each adapter declares which it has; the engine chooses a strategy from them):

| Capability | Folder | WebDAV | Google Drive | GitHub |
|---|---|---|---|---|
| Conditional write | Local only (temp file and atomic rename) | `If-Match` / `If-None-Match` | Revision check before update (behaviour confirmed in step A5) | Commit on top of the expected parent; the ref update fails if it moved |
| Change feed | No (scan) | No (folder ETag walk) | Yes (`changes.list`) | Yes (compare commits) |
| Complete listing | Yes | Yes, when the walk succeeds | Yes, through a paged listing | Yes (tree) |
| Server-side move | Yes | `MOVE` | Yes (change the parent) | Within a commit |
| Content hash from provider | Computed locally | No (ETag only) | Possibly (`sha256Checksum` to be confirmed in A5; otherwise download and hash) | Git blob hash, computed locally to compare |
| Batch commit | n/a | No | No | Yes: one commit per cycle |

## 7. Providers and sign-in

| Route | Sign-in | Where credentials live |
|---|---|---|
| Google Drive | OAuth with PKCE, `drive.file` only, through the system browser. Desktop uses a loopback redirect (RFC 8252); phones use the platform's browser session and return the redirect to PSC | The host's secure storage (§8.3) |
| GitHub | GitHub App "Personal Systems Coordinator", device flow: PSC shows a code, the user approves it in the browser. Contents read/write on the selected repository only. A fine-grained personal access token is the fallback for advanced users | Same |
| WebDAV | Server address, user name and an app password (never the main password where the server offers app passwords). HTTPS only, except `localhost` | Same |
| Local folder | No sign-in. Folder access through the operating system's picker | Platform bookmark or permission, stored device-locally |

- **Client IDs are configuration** supplied by the host app, never hard-coded in PSC.
- **No client secrets** are shipped as if they were secret. Native apps are public clients.
- **Tokens are never logged.** Logs pass through a redaction layer, and a test checks it.

## 8. Public API and bindings

### 8.1 API surface (v1)

Exported through UniFFI as one object, `Psc`:

| Group | Calls |
|---|---|
| Setup | `Psc::new(config, platform_services)` where `config` holds the app ID, app folder name, local folder, data directory, provider client IDs, limits, allowed types and ignore list |
| Connect | `begin_connect(route) -> ConnectStep` (an authorization URL, a device code to show, or a folder request); `complete_connect(response)`; `disconnect(keep_local_files: bool)` |
| Workspace | `open_or_create_workspace() -> WorkspaceInfo`; `list_apps()`; `list_devices()` |
| Sync | `sync_now(budget, cancel) -> SyncReport`; `status() -> SyncStatus`; `subscribe(listener)` for status events; `confirm_pending_deletions()` |
| Conflicts | `list_conflicts()` (paths of conflict copies and their originals) |

**Errors are codes, not sentences.** For example `offline`, `auth_expired`, `rate_limited { retry_after }`, `quota_exceeded`, `route_mismatch`, `update_required`, `confirmation_required`, `permission_denied`, `provider_error { http_status }`, `cancelled`. Host apps translate them into their own words and languages. PSC contains no user-facing text.

### 8.2 Bindings

| Language | Tool | Status |
|---|---|---|
| Swift (macOS first, iOS later) | UniFFI (Mozilla, official) | Supported, including async and callbacks [Official] |
| Kotlin (Android) | UniFFI (official) | Supported, including async and callbacks [Official] |
| C# (Windows) | `uniffi-bindgen-cs` (NordSecurity, third-party, version 0.x) | **Risk:** young, versions tied to UniFFI releases. Checked in step A2; fallback is a thin C ABI with `csbindgen` |

Generated bindings are build output. They are never edited by hand and never committed. CI generates them and packages them.

### 8.3 What the host app provides (`platform_services`)

- **Credential store:** save, load, delete. Bindings include defaults: Keychain (Apple), Credential Manager (Windows), Keystore-backed storage (Android).
- **Browser hand-off:** open a URL in the system browser or the platform's authentication session, and return the redirect.
- **Log sink:** where PSC's redacted logs go.
- **Network state** (optional): hints for "offline" and "metered".

### 8.4 Packaging

| Platform | Package |
|---|---|
| Windows | NuGet package with the native DLL and C# bindings |
| macOS (and iOS later) | Swift package with an XCFramework |
| Android | AAR with native libraries for arm64-v8a and x86_64 (for the emulator), built with `cargo-ndk` |
| Linux | Only if the WP8 feasibility check passes |

## 9. Engineering standards

### 9.1 Libraries (use established libraries; no home-made versions)

| Need | Library |
|---|---|
| Async runtime | `tokio` |
| HTTP | `reqwest` with `rustls` and platform certificate verification |
| OAuth (PKCE, device flow) | `oauth2` |
| JSON | `serde`, `serde_json` |
| Device-local database | `rusqlite` (bundled SQLite) with migrations (`rusqlite_migration`) |
| Hashing | `sha2` |
| XML (WebDAV) | `quick-xml` |
| File watching (desktop hint only) | `notify` |
| IDs | `uuid` |
| Time | `time` |
| Errors | `thiserror` |
| Logging | `tracing` |
| Retries and backoff | `backon` |
| Bindings | `uniffi`; `uniffi-bindgen-cs` for C# |
| Property tests | `proptest` |
| HTTP test doubles | `wiremock` |

Thin provider clients are written in-house only where no maintained library covers the few endpoints PSC uses with the control it needs (conditional writes, change feeds). They stay small and are tested against recorded responses. Before any new dependency: check license, maintenance, platform support and size (`RULES.md` §9).

### 9.2 No hard-coded values

Every limit, interval, threshold, file type and name pattern is a named configuration value, with a default, a unit and a reason, documented in one place (`psc-core` configuration module and `spec/CONFIG.md`). Defaults in this document: tombstone retention 90 days; mass-deletion guard 25% or 50 files; maximum file size 50 MB (revised after provider tests); allowed types and ignore list as in §3.

### 9.3 Guardrails (enforced in CI)

| Check | Rule |
|---|---|
| Formatting | `cargo fmt --check` |
| Lints | `cargo clippy -- -D warnings`, plus `unwrap_used`, `expect_used`, `panic`, `todo` and `dbg_macro` denied outside tests |
| Unsafe code | `#![forbid(unsafe_code)]` in every crate except `psc-ffi` |
| Tests | Unit tests, property tests for the sync engine, the fixture suite, recorded-response adapter tests |
| WebDAV integration | Against Nextcloud in Docker on every adapter change |
| Dependencies | `cargo-deny`: license allowlist (per D6), security advisories, banned crates, trusted sources only |
| Toolchain | `rust-toolchain.toml` pins the Rust version; `Cargo.lock` committed |
| PR hygiene | Existing `ci/pr_hygiene.py` |
| Docs | Public API items documented (`missing_docs` warns) |

### 9.4 Platform guidelines

PSC has no UI, but its behaviour must let apps follow each platform's rules:
- **Sign-in in the system browser,** never an embedded web view (Apple authentication session, Android Custom Tabs, the default browser on desktop).
- **Background work through the platform scheduler** (Android WorkManager; Apple background tasks; on Windows, while the app runs), with PSC respecting time budgets.
- **File access through the platform's pickers and permissions.**
- **Everything user-facing is the app's job,** in the app's design language.

## 10. Deliberately not in v1

- Encryption (D4); the design keeps room for per-app encrypted folders later.
- Publishing data to other apps (§4); the registry has the field.
- Dropbox, OneDrive, iCloud, Gitea/Forgejo, other WebDAV presets (deferred by the owner).
- iOS and Linux bindings.
- Real-time sync or push notifications.
- Multi-person sharing (never: one person's devices only).
- Rename tracking beyond hash-matched moves within one cycle.

## 11. How certain the routes are (before Phase A experiments)

| Route | Technical certainty | Average-user fit | Settled by |
|---|---|---|---|
| Google Drive | Medium: sharing between sign-in clients unknown | High | A1 |
| GitHub | High | Low | A4 confirms |
| WebDAV (Nextcloud) | Medium-high | Low-medium | A3 |
| Local folder, desktop | High | Medium | — |
| Local folder, phones | Low; phones use an API route instead | Low | — |
| C# binding | Medium: young generator | n/a | A2 |
