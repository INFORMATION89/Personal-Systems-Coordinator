# Platform Constraints

**Research date:** 2026-11-27  
**Status:** documented platform constraints; no implementation selected.

PSC aims to serve Windows, macOS, iOS, Android and Linux. A single shared synchronization engine cannot erase the differences in file access, permissions and background execution imposed by these platforms.

## 1. Android

### User-selected folders

Android's Storage Access Framework lets the user choose a directory through ACTION_OPEN_DOCUMENT_TREE. The app receives a URI rather than an ordinary filesystem path.

- Persist access with takePersistableUriPermission when the returned grant permits it.
- Store the tree URI as device-local provider state; do not put it into the shared workspace manifest.
- Handle provider unavailability, permission revocation, renamed/moved folders and storage removal.
- Android 11+ restricts access to certain locations through the tree picker, including internal storage roots, reliable SD-card roots and Downloads. Android/data and Android/obb are also restricted.
- The selected provider may be Google Drive, OneDrive or another DocumentsProvider, not necessarily local disk.

Official source: [Android — Access documents and other files from shared storage](https://developer.android.com/training/data-storage/shared/documents-files).

### Background work

WorkManager is the recommended mechanism for persistent deferrable work. Periodic work has a minimum 15-minute interval, and exact execution depends on constraints, Doze and system scheduling. This is not a guarantee that a sync will run exactly every 15 minutes.

Sources:
- [Android — Define WorkRequests](https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work)
- [Android — PeriodicWorkRequest](https://developer.android.com/reference/androidx/work/PeriodicWorkRequest)

### Consequence

Use immediate foreground sync after a relevant user action where possible, and schedule opportunistic background work. Never promise continuous or exact-time sync on Android.

## 2. iOS and iPadOS

### User-selected folders

From iOS 13, UIDocumentPickerViewController can let the user select a directory from available file providers. The returned security-scoped URL grants access to the selected directory and descendants. A bookmark can preserve access across app launches, subject to reauthorization/renewal and provider state.

Use coordinated file access. Apple recommends NSFileCoordinator, NSFilePresenter, or document abstractions such as UIDocument to avoid concurrent file changes and data loss.

Sources:
- [Apple — Providing access to directories](https://developer.apple.com/documentation/uikit/providing-access-to-directories)
- [Apple — Shared data](https://developer.apple.com/documentation/technologyoverviews/shared-data)
- [Apple — NSFileCoordinator](https://developer.apple.com/documentation/foundation/nsfilecoordinator)

### Background work

BGAppRefreshTask and BGProcessingTask are scheduled by the system. The system decides when eligible work runs; processing tasks can be interrupted and require expiration handling. An earliestBeginDate is not an exact execution promise.

Sources:
- [Apple — Background Tasks](https://developer.apple.com/documentation/backgroundtasks)
- [Apple — Using background tasks to update your app](https://developer.apple.com/documentation/uikit/using-background-tasks-to-update-your-app)
- [Apple — BGProcessingTask](https://developer.apple.com/documentation/backgroundtasks/bgprocessingtask)

### Consequence

Use foreground sync when the app opens or the user requests it, and schedule opportunistic background refresh. Coordinate all external document operations and tolerate suspension at any point.

## 3. macOS

macOS supports native file access, sandboxed user-selected folder permissions and iCloud/third-party File Provider integrations. When operating in a sandbox, the selected directory's security-scoped access and bookmark lifecycle must be respected.

File coordination remains important for files shared with other processes and File Providers. Do not treat a provider-mounted file as a normal local file with guaranteed immediate reads or writes.

Sources:
- [Apple — Shared data](https://developer.apple.com/documentation/technologyoverviews/shared-data)
- [Apple — Improving performance and stability when accessing the file system](https://developer.apple.com/documentation/foundation/improving-performance-and-stability-when-accessing-the-file-system)

## 4. Windows

Windows offers ordinary filesystem paths for directories accessible to the process, but cloud services such as iCloud Drive and OneDrive may expose placeholder/hydrated files and provider-specific availability states. A path being visible does not prove that content is fully local or immediately readable.

Apple documents iCloud Drive through iCloud for Windows and File Explorer. The user must install and configure iCloud for Windows and sign in. This is a user-installed provider integration, not a public iCloud Drive API available to arbitrary PSC clients.

Sources:
- [Apple — Set up iCloud Drive](https://support.apple.com/en-us/118443)
- [Apple — View, add, or remove iCloud Drive files in iCloud for Windows](https://support.apple.com/guide/icloud-windows/icwddbc813bd/icloud)

## 5. Linux

A user-selected folder can be accessed through the ordinary filesystem, subject to permissions, mounts and provider software available on that distribution. There is no single built-in cloud File Provider interface shared by all Linux distributions. WebDAV, mounted cloud folders and Syncthing-managed directories are possible user-managed options.

This requires a platform-specific implementation and test matrix; do not infer complete provider parity from the existence of a filesystem path.

## 6. Cross-platform rules

1. Store absolute paths, security-scoped URLs, SAF tree URIs, access tokens and provider bookmarks locally on the device. They are not portable workspace data.
2. Use a portable workspace identifier in shared metadata. On each device, the person selects or authorizes the corresponding remote root.
3. Treat filesystem notifications as hints, not the sole source of truth. Reconcile on app launch/resume and after a provider signals change.
4. Design all sync jobs to be resumable, idempotent and safe to stop at any instruction boundary.
5. Keep a visible last-sync state: last successful check, outstanding local changes, remote changes pending, provider unavailable, authorization expired, conflicts and errors.
6. Do not claim real-time sync across mobile platforms. Use syncs when possible or a more precise status that reflects platform scheduling.
7. Any provider that hydrates remote content on demand can incur latency and network use during file reads; do not perform this work on the UI thread.
8. Use native OS coordination APIs where the platform requires them; do not assume shared cross-platform code, in any language, can replace them.

## Required prototype checks

- Restart app and device while folder permission is persisted.
- Revoke permission and move/rename the selected folder.
- Test a third-party File Provider/DocumentsProvider, not only local disk.
- Edit the same file in an external editor while PSC is reading/writing.
- Test app suspension and process termination mid-upload.
- Verify behavior when a remote file exists as a placeholder but is not downloaded.
- Verify workspace selection separately on two devices.
