# Provider and Storage Comparison

**Research date:** 2026-11-27  
**Status:** evidence-based comparison; no provider selected.

## Executive findings

There is no single provider abstraction that makes every storage service behave like an ordinary, always-online filesystem on every platform. PSC should model provider capabilities explicitly and preserve a local-first fallback.

The options belong to different categories:

1. **User-selected folders** — PSC reads and writes a directory granted by the operating system. The directory may itself be local, iCloud Drive, Google Drive for desktop, OneDrive, Dropbox, a NAS mount, or another File Provider/DocumentsProvider.
2. **Cloud storage APIs** — PSC talks directly to a provider API using user authorization, change cursors and provider-specific revisions.
3. **External folder synchronization** — another tool synchronizes a folder; PSC only works with its local files and does not operate that service.
4. **Version-control storage** — GitHub provides history and collaboration semantics, but is not a general-purpose low-friction mobile sync engine.

Keep these models distinct in the design and user-facing settings.

## Provider matrix

| Option | Category | Cross-platform fit | Change detection / concurrency | Best role | Main caveat |
|---|---|---|---|---|---|
| User-selected folder | OS file access | Strong conceptual fit; API differs per OS | File scans/watchers and filesystem-specific coordination; no universal revision feed | Universal escape hatch and user-owned storage | Mobile permissions and background execution are constrained |
| Google Drive API | Cloud API | Android, iOS and desktop can use REST/OAuth | changes.list page tokens; revisions/metadata; optional push channel | Early cloud-provider prototype | drive.file is per-file and may complicate one shared folder across multiple apps |
| OneDrive / Microsoft Graph | Cloud API | Strong API coverage across platforms | Delta links, deleted facets, upload sessions, eTags | Candidate managed provider | Graph throttling and Microsoft identity setup |
| Dropbox API | Cloud API | Strong API coverage across platforms | list_folder cursor, file rev, upload sessions | Candidate managed provider | Dropbox account/app scopes and API policy; not a filesystem |
| iCloud Drive | OS File Provider / Apple services | Native Apple and Windows integration; no equivalent public Android Drive API identified | File-provider/document coordination; CloudKit has separate record semantics | Apple-oriented folder option; possible separate Apple adapter | Not a universal cross-platform provider |
| WebDAV | Open protocol | Broad server ecosystem; platform API must be implemented | ETags; optional RFC 6578 sync-collection extension | Advanced/self-hosted/NAS option | Server capability and standards-extension support vary |
| Syncthing-managed folder | External sync tool | Desktop/Linux/Android ecosystem, with platform-specific availability | Folder index, versioning and conflict copies | Let users sync a chosen folder themselves | PSC does not control availability, discovery or timing |
| GitHub repository | Version-control service | APIs and Git clients exist on most platforms | Git commits, branches and merges | Advanced text/document history or manual backup | Git is not designed as a high-frequency app database or mobile sync substrate |

## 1. User-selected local folder

This is the most provider-neutral option. The person chooses a folder through the operating system, and PSC accesses only that granted location.

### Evidence

- Android's Storage Access Framework provides ACTION_OPEN_DOCUMENT_TREE for a user-selected directory and supports persistable URI permissions. Android 11+ excludes certain roots and locations, including internal-storage roots, SD-card roots, Downloads, Android/data and Android/obb from relevant tree/file picker access paths. See [Android: access documents and other files from shared storage](https://developer.android.com/training/data-storage/shared/documents-files).
- iOS/iPadOS can let the person select a directory from available file providers with UIDocumentPickerViewController; the app receives a security-scoped URL and can save a bookmark for later access. See [Apple: providing access to directories](https://developer.apple.com/documentation/uikit/providing-access-to-directories).
- Apple requires coordinated access for files shared with other processes or File Providers. NSFileCoordinator and NSFilePresenter exist to avoid concurrent read/write conflicts and data loss. See [Apple: shared data](https://developer.apple.com/documentation/technologyoverviews/shared-data) and [NSFileCoordinator](https://developer.apple.com/documentation/foundation/nsfilecoordinator).

### Implications

- Ask the user to select the workspace root on each device. Do not assume an absolute path is portable.
- Store a local platform bookmark/URI and separately verify the workspace identity from a small PSC marker file.
- On iOS, use coordinated document/file access and handle security-scoped access correctly.
- On Android, persist the granted tree URI and expect that a provider can be unavailable, slow, partially online or revoked.
- A local folder does not itself synchronize. Users may choose iCloud Drive, OneDrive, Dropbox, Syncthing, a NAS, or no sync at all.
- Do not assume file watchers reliably report every remote File Provider change. Reconcile on app foreground/resume and perform bounded scans when required.
- A folder backend should declare whether it supports atomic replacement, reliable modification time, stable file IDs, notifications, conditional writes or none of these.

### Assessment

A user-selected folder is essential as an open option, but it does not provide equivalent background sync on Android and iOS. It should be treated as a first-class storage mode with opportunistic synchronization, not as a promise of continuous multi-device convergence.

## 2. Google Drive

Google Drive offers a direct REST API with user OAuth, visible folders and files, file metadata, resumable uploads and an incremental change feed.

### Evidence

- changes.list returns pages of changes and a newStartPageToken to store for the next incremental sync. See [Drive API: changes.list](https://developers.google.com/workspace/drive/api/reference/rest/v3/changes/list).
- Google recommends the non-sensitive drive.file scope for most apps. It grants per-file access to files created by the app or opened/shared with the app using Google Picker or an app file picker. Broad drive and drive.readonly scopes are restricted. See [Choose Google Drive API scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).
- appDataFolder is a separate, app-specific and user-invisible storage space; it is not a substitute for a visible folder that users and other apps can manage. See [Drive files and folders overview](https://developers.google.com/workspace/drive/api/guides/about-files).
- Drive's changes.watch notifications only indicate that the change log has new items; the app must still retrieve the actual changes. See [Retrieve changes](https://developers.google.com/workspace/drive/api/guides/manage-changes).
- Native/installed apps are public OAuth clients and Google documents PKCE support for installed applications. See [OAuth 2.0 for native apps](https://developers.google.com/identity/protocols/oauth2/native-app).

### Main architectural question: one folder shared by multiple PSC applications

The desired user experience is one Personal Ecosystem folder with separate app-owned subfolders. However, drive.file is intentionally per-file and per-app. We must not assume that a folder selected by Solstice automatically grants Notes or Clock access to that folder's contents.

A Google Developer forum discussion dated October 2026 describes per-user/per-file access and recommends experimentally testing whether selecting the parent folder grants access to its existing and future descendants. This is not a substitute for official documentation, but it reinforces that the behavior needs a proof of concept: [Google Developer Forum: drive.file scope on shared folders](https://discuss.google.dev/t/google-drive-sheets-api-with-drive-file-scope-on-shared-folder-files/402266).

**Required experiment before selecting Drive for the whole app family:**
1. Register the actual PSC Google Cloud project and the native OAuth clients planned for Android, iOS and desktop.
2. Have app A create a normal visible workspace folder and a file inside it.
3. Have app B select only the parent folder through the supported picker flow.
4. Test listing/reading existing children, reading files created later by app A, writing a new child, and reading that child from app A.
5. Repeat on a second device and after token revocation/re-consent.
6. Determine whether each application must individually select the root or each child; record exact permission behavior.
7. Check current verification requirements for the final scopes and distribution model.

Do not solve the issue by immediately requesting broad access to every Drive file. If the restricted scope is ultimately required, the verification, security and trust implications must be reviewed first.

### Assessment

Strong candidate for an early cloud API prototype, particularly for a single application such as Solstice. The shared-folder/multi-app authorization model is a release-blocking research question for the long-term family experience.

## 3. OneDrive / Microsoft Graph

Microsoft Graph provides useful synchronization primitives:
- driveItem/delta returns pages ending in a delta link; subsequent requests with that link return changes, including deletions. Clients should track items by ID, not path. The feed represents the latest state for each item rather than every intermediate edit. See [driveItem: delta](https://learn.microsoft.com/en-us/graph/api/driveitem-delta?view=graph-rest-1.0).
- Upload sessions support sequential ranged uploads and resume after a dropped connection. If-Match can reject an update when the eTag no longer matches. See [createUploadSession](https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0).
- Microsoft Graph can return 429 Too Many Requests; clients should respect Retry-After, use backoff and avoid continuous polling. See [Graph throttling guidance](https://learn.microsoft.com/en-us/graph/throttling).
- Microsoft supports authorization-code flow with PKCE for desktop and mobile clients. See [Microsoft identity platform authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow).

### Assessment

A strong candidate for a managed-provider adapter. Delta links and eTags provide useful building blocks, but PSC must still own its domain-level conflict policy. Microsoft Graph is not a free unlimited service contract; user storage plans, API quotas, throttling and service conditions still apply.

## 4. Dropbox

Dropbox exposes a file API rather than a mounted filesystem contract:
- list_folder and list_folder/continue provide a cursor-based incremental listing/change process. See [List Folder Continue](https://docs.dropboxapi.com/dropbox-api/api-reference/user-endpoints/files/list-folder-continue).
- File metadata includes a rev identifier that can be used to detect changes and avoid conflicts. See [Upload Session Finish](https://docs.dropboxapi.com/dropbox-api/api-reference/user-endpoints/files/upload-session-finish).
- Upload sessions support multi-request uploads and resume-oriented transfer patterns. See [Upload Session Start](https://docs.dropboxapi.com/dropbox-api/api-reference/user-endpoints/files/upload-session-start).
- Dropbox recommends OAuth authorization code with PKCE for mobile, desktop and other public clients. Refresh tokens can be requested for background access. See [Dropbox OAuth](https://docs.dropboxapi.com/dropbox-api/docs/oauth).

### Assessment

Technically suitable as a future cloud-provider adapter. Do not place Dropbox-specific revision or cursor logic in application domain code. Confirm app review, scopes, user-facing consent and current API conditions before production.

## 5. iCloud Drive and CloudKit

These are related Apple services, but they are not interchangeable.

### iCloud Drive

- On Apple platforms, iCloud Drive appears through native file/document infrastructure and the Files/Finder experience.
- Apple provides a directory picker with security-scoped URLs and file coordination for third-party file providers.
- Apple also documents iCloud Drive on Windows through iCloud for Windows and File Explorer. See [Apple: set up iCloud Drive](https://support.apple.com/en-us/118443) and [iCloud for Windows: view and add files](https://support.apple.com/guide/icloud-windows/icwddbc813bd/icloud).
- This research found no public, general iCloud Drive REST API equivalent to Google Drive API that PSC could use on Android.

### CloudKit

- CloudKit is a structured-data service with per-app containers and private/shared/public databases, not an ordinary user-selected folder. See [CloudKit overview](https://developer.apple.com/documentation/cloudkit).
- Multiple apps from the same developer team can be configured to access a shared CloudKit container using entitlements. See [CKContainer](https://developer.apple.com/documentation/cloudkit/ckcontainer) and [Configuring iCloud services](https://developer.apple.com/documentation/xcode/configuring-icloud-services).
- CloudKit's native model is Apple-specific; it does not by itself solve Android/Windows/Linux parity.

### Assessment

Support iCloud Drive through native folder/File Provider integration where the OS exposes it. Treat CloudKit as a possible Apple-only adapter if the product later justifies a second, platform-specific sync model. Do not describe iCloud as the universal PSC provider.

## 6. WebDAV

WebDAV is an open protocol layered on HTTP. It is attractive for self-hosted storage, NAS systems and services such as Nextcloud.

- RFC 4918 defines WebDAV resources, collections, properties and locking. See [RFC 4918](https://www.rfc-editor.org/rfc/rfc4918.html).
- RFC 6578 defines the sync-collection extension, which allows a client to use synchronization tokens to retrieve changed, added and deleted resources without repeatedly listing an entire collection. See [RFC 6578](https://www.rfc-editor.org/rfc/rfc6578.html).
- HTTP entity tags and conditional requests are important for avoiding silent overwrites. See [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html).

### Assessment

A valuable advanced adapter because it supports user-controlled and self-hosted infrastructure. However, do not assume every WebDAV server implements RFC 6578, locks or ETag behavior correctly. The adapter needs a capability probe and a conservative fallback strategy.

## 7. Syncthing-managed folder

Syncthing is not a cloud-storage API for PSC. It is a separate folder synchronization tool.

- Syncthing tracks local and global file versions and creates conflict copies when two devices modify the same file concurrently rather than silently combining the content. See [Syncthing: understanding synchronization](https://docs.syncthing.net/users/syncing).
- It can use local discovery, global discovery and relay infrastructure. Global discovery exposes device IDs and network-address metadata to discovery operators; its security documentation explains what is announced. See [Syncthing security principles](https://docs.syncthing.net/users/security).
- Optional file versioning can retain replaced or deleted versions according to a configured strategy. See [Syncthing file versioning](https://docs.syncthing.net/users/versioning.html).

### Assessment

Treat Syncthing as an external mechanism the user may point at a PSC folder. PSC should not depend on it, bundle it, or imply that it is a cloud-provider adapter. Document its device availability and discovery/relay trade-offs when users choose it.

## 8. GitHub repositories

GitHub has real strengths for text-oriented data:
- Git provides commit history, branches and diffs.
- GitHub exposes repository contents and Git database APIs.
- Private repositories can keep personal data out of public view when configured correctly.

But it is not a general-purpose sync filesystem:
- Concurrent edits produce Git merge conflicts; non-technical users should not have to resolve these.
- Every change may create repository history and increase clone/pull cost.
- GitHub recommends keeping repository size small; individual Git objects over 100 MiB are blocked, and Git is not designed as a backup tool or large database store. See [GitHub repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits) and [About large files](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).
- REST API secondary limits and content-generation limits apply. See [GitHub REST API rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api).

### Assessment

Keep GitHub as an advanced option for users who deliberately want Git history and understand repositories. Do not use it as the default sync mechanism for Clock sessions, rapidly changing preferences, or ordinary multi-device Notes editing.

## Calendar services are a separate category

Connecting Google Calendar, Apple Calendar, Outlook or CalDAV is a service integration, not a PSC storage provider. These services own events, recurring-calendar semantics and invitations. See [CalDAV RFC 4791](https://www.rfc-editor.org/rfc/rfc4791.html). See CALENDAR_INTEGRATIONS.md for the separate scope.

## Provisional research ordering (not a product commitment)

1. **Folder access prototype:** Android SAF and iOS directory picker, including persistent access, external provider behavior and file coordination.
2. **Google Drive prototype:** one visible folder, one application, drive.file, change cursor and conditional/conflict handling.
3. **Multi-app Google Drive permission experiment:** must pass before claiming a single shared folder works across the whole app family.
4. **OneDrive or Dropbox:** choose one second API provider to prove the adapter boundary.
5. **WebDAV:** capability-probed self-hosted option.
6. **iCloud:** native folder/File Provider route, not a universal REST provider.
7. **GitHub:** optional advanced integration only after the baseline sync protocol is stable.

This ordering is a recommended research sequence, not approval to implement or ship these providers.
