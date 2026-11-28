# Provider Authorization: Google Drive (WP1, part 1)

**Research date:** 2026-11-28
**Status:** desk research, first pass. No experiment has run yet. No registration model is approved.
**Prepared with:** Claude Code, tier O (research only); not yet reviewed by the owner.
**Scope:** Google Drive only. iCloud, Microsoft Graph and Dropbox (WP1 questions 5–6) are still to do.

## How to read this report

Every claim is labelled by the strength of its evidence:

- **[Official]** Google documentation or help pages, seen through search-engine extracts. This session could not open developers.google.com or support.google.com directly: the hosts were blocked and still failed after being added to the environment's allowed hosts. Official claims should be re-read in full before any decision.
- **[Community]** Developer forums, open-source projects, issue trackers and blogs.
- **[Inference]** Reasoning from the evidence above. Not stated by any source.
- **[Untested]** Needs the experiment in §6.

## 1. Summary

1. **`drive.file` is the only realistic scope.** It is non-sensitive, so there is no restricted-scope verification, no annual security assessment and no 100-user cap. The broader scopes are restricted, which means verification plus a paid annual assessment, and Google's eligibility rules for them are narrow. [Official, §4]
2. **Native apps can now use the Google Picker.** Desktop and mobile apps open it in the system browser by adding `trigger_onepick=true` to the OAuth request. It returns the selected file IDs through a redirect URI or a custom URL scheme. [Official, §3]
3. **Picking a folder probably does not grant access to its contents.** Two independent hands-on reports say that under `drive.file`, a picked folder lists as empty. No official statement says otherwise. [Community, §3] So the original idea of "each app picks the shared root folder" is unlikely to work.
4. **What the app creates, the app can see.** That remains the reliable path. The open question is what "the app" means: one OAuth client, or the whole Cloud project? Community sources say access is tied to the OAuth client ID, but they mostly compare clients from different projects. Nothing found settles the same-project case. [Community/Untested, §5]
5. **That question decides the architecture.**
   - **If access is per project,** one family-level Cloud project, with separate OAuth clients for each app and platform, could give every app access to everything any of them created. A shared workspace works.
   - **If access is per client,** even one app's Android and desktop clients could not see each other's files. That would rule out Drive API sync across a phone and a PC.

   This is now the first experiment to run.
6. **Mixing access routes is a trap.** A PC using the "Google Drive for desktop" folder writes files as the user, not as the app. Under `drive.file`, the phone app would not see them. [Inference from 4; Untested] All devices in one workspace must reach Drive the same way.
7. **New files created outside the app are invisible.** A Markdown note created in the Drive web UI or by another tool is not visible to a `drive.file` app unless the user picks it. Edits to files the app created should stay visible, because the file ID doesn't change. [Inference; Untested] This matters for Commonplace's goal of editing outside the app.

## 2. Who owns the registration (WP1 question 1)

PSC is a library, so it must not embed credentials. The host app supplies its client IDs. The real question is how the owner organizes Cloud projects for the app family.

| Model | How it works | Shared workspace | Costs and obligations |
|---|---|---|---|
| **A. One family project** (recommended to test first) | One Google Cloud project owned by the developer, with one OAuth client per app and platform: Android (package name + signing-certificate fingerprint), iOS (bundle ID), desktop. | Possible only if `drive.file` access is per project. [Untested] | One consent screen and brand for all apps. One verification. Quota shared by every app and every user. One privacy policy and homepage. |
| **B. One project per app** | Each app has its own project and clients. | No. Each app sees only its own files. Future cross-app features would need the user to pick files one by one. | Separate consent screens and verification. Quotas isolated per app. |
| **C. Restricted scope** (`drive`) | Any model above, with full Drive access. | Yes, regardless of project. | Restricted-scope verification, annual third-party security assessment (CASA), Google's narrow eligibility rules, and much larger user-trust and security exposure. Against PSC's least-privilege principle. [Official, §4] |
| **D. Third-party apps using PSC** | Their own project and clients. | Never with the owner's apps. | Their responsibility. PSC only needs to accept client configuration from the host app. |

**A registration is not a PSC backend.** A Cloud project is a set of credentials and policy obligations, not a server. Nothing runs and no data passes through it. It does carry obligations: consent-screen branding, a privacy policy, a support contact, quota monitoring, and keeping the project in good standing. [Inference]

## 3. Picker on native apps and folder access (WP1 question 2–3)

**Native Picker flow** [Official]
- Desktop and mobile apps trigger the Google Picker by adding `trigger_onepick=true` to the OAuth request. Authentication and file picking happen in a single system-browser flow.
- Results come back through a redirect URI or a custom URL scheme, and include file metadata such as IDs and URLs.
- Users cannot move or copy files between folders in the Picker.

**Scope with the native Picker**
- For Android, Google's guide says to request `drive.file` and set `setOptOutIncludingGrantedScopes(true)`, so the token covers only `drive.file`. [Official]
- A secondary source says desktop and mobile Picker flows allow only `drive.file`, which cannot be combined with other scopes. [Community; re-check against the official page]

**Folders**
- A personal-storage project's spike (2026-11) found that listing the children of a Picker-selected folder under `drive.file` returns an empty list. Under `drive.readonly` it returned all files. [Community]
- An Uppy pull request reaches the same conclusion, and notes that an empty listing is indistinguishable from having no access. [Community]
- Other sources claim the opposite but describe untested proposals. [Community]
- **Conclusion:** assume picking a folder grants access to the folder object only, not its contents. The experiment must confirm whether that holds for the native Picker too.

**Android folder route.** Android's directory picker (`ACTION_OPEN_DOCUMENT_TREE`) shows only providers that support directory selection. [Official] A 2021 community answer says Google Drive's Android provider allows single files only, not folders. [Community, may be outdated] If that still holds, an Android phone cannot use "pick a Drive folder" through the operating system. It must use the Drive API.

## 4. Scope classification and verification

- **Non-sensitive and recommended:** `drive.file` ("only the specific Google Drive files you use with this app") and `drive.appdata` (the hidden app-data folder). [Official]
- **Restricted:** `drive`, `drive.readonly` and `drive.metadata.readonly`. [Official; translated pages disagree on `drive.metadata.readonly`, so the English page is authoritative]
- **Eligibility:** for Drive, only platform-specific and web apps that provide local sync or automatic backup of users' Drive files may use restricted scopes. [Official] Commonplace syncing its own workspace probably does not qualify. [Inference]
- **Unverified-app cap:** an unverified app requesting sensitive or restricted scopes shows an "unverified app" screen and is capped at 100 new users over the project's lifetime. The cap cannot be reset. [Official] Non-sensitive scopes are not subject to it. [Inference from the wording; confirm]
- **Security assessment:** apps using restricted scopes need an annual assessment by a Google-approved third party. [Official] Whether a client-only app with no server is exempt is disputed. [Community] A 2024 community report gave about US$540 a year for the lowest tier. [Community, possibly outdated]

**Consequence for model C:** for a small app family distributed to friends, the restricted route costs money every year, is uncertain on eligibility, and contradicts least privilege. Use it only if every `drive.file` design fails.

## 5. Quotas (WP1 question 4)

- The Drive API has quotas per project and per user per project. Exceeding them returns 403 or 429, and Google recommends exponential backoff. [Official]
- Current figures could not be confirmed. Google appears to be moving from query counts (an older page says 12,000 queries per 60 seconds) to weighted quota units (for example, `files.list` costs more than `files.get`), and the extracted figures were inconsistent. [Official, unclear] The project's Cloud console shows the limits that actually apply.
- **Implication for model A:** all apps and all users share one project quota. For a family of personal apps used by friends, this is very unlikely to bind, but sync must avoid polling. Use the Drive change feed with backoff, and only list folders when needed. [Inference]

## 6. Experiment plan (replaces the earlier draft in the provider comparison)

Run these in order. Stop and report as soon as a step fails, because later steps depend on it.

**Setup:** one test Cloud project, consent screen in testing mode with test users, and `drive.file` only.

| # | Test | Decides |
|---|---|---|
| E1 | Android client creates a folder and a file. A desktop client in the **same project** lists and reads them. | Per-project or per-client access. The key result for model A. |
| E2 | Same as E1, but with a second **app** (different package name) in the same project. | Whether separate family apps can share a workspace. |
| E3 | Same as E1, with a client from a **different project**. | Confirms that model B isolates apps. Expected to fail. |
| E4 | Native Picker (`trigger_onepick=true`): pick a folder, then list its existing children and files added later by another client. | Whether folder picking helps at all. Expected to fail. |
| E5 | Native Picker: pick individual files created elsewhere (for example in the Drive web UI), then read and update them. | The recovery path for files the app didn't create. |
| E6 | Edit an app-created Markdown file in the Drive web UI or with Drive for desktop. Check the app still sees it with the same ID and picks up the change. | External editing of existing notes. |
| E7 | Create a new file in the workspace folder through Drive for desktop. Check whether the app can see it. | Confirms the mixed-route trap. Expected to fail. |
| E8 | Revoke access in Google account settings, re-authorize and reinstall. Check that previously created files are visible again. | Recovery after disconnect or a new device. |
| E9 | Same as E1 on iOS. | Platform parity. |

**Decision rule**
- **E1 and E2 pass:** go ahead with model A. The family shares one workspace, and all devices use the Drive API.
- **Only E1 passes:** one Cloud project per app. Each app syncs only its own data, and future cross-app features need another mechanism.
- **E1 fails:** the Drive API cannot sync one app between a phone and a PC under `drive.file`. Fall back to the folder route on desktop plus a different phone strategy, or another provider. Model C is a last resort that needs the owner's decision.

## 7. What this means for Commonplace

- **Every Commonplace device should use the Drive API.** Mixing the Drive API on the phone with the Drive for desktop folder on the PC would break visibility (E7). [Inference]
- **Users should create notes inside Commonplace.** Notes created in Drive directly won't sync unless the user imports them through the Picker (E5). The app should explain this.
- **Editing existing notes elsewhere should work** (E6). If E6 holds, conflict detection relies on Drive revisions.
- **The folder route remains available** for other storage. A user can still point Commonplace at a local folder synced by any tool. Drive via the API is a separate storage option with its own rules.

## 8. Still open

- Re-read the official pages in full, especially the native Picker guide, the scopes page, the app-data guide and the unverified-apps page, once those hosts are reachable from this environment.
- iCloud Drive and CloudKit container sharing between apps from the same team (WP1 question 5).
- Microsoft Graph and Dropbox scopes for an app folder versus a user-selected folder (WP1 question 6).
- Whether `drive.appdata` (hidden, deleted if the user removes the app) is useful for PSC metadata. It is not suitable for user-visible notes.

## Sources

Official (via search extracts):
- [Integrate the Google Picker into desktop and mobile apps](https://developers.google.com/workspace/drive/picker/guides/desktop-mobile-picker)
- [Overview of desktop and mobile apps (Picker)](https://developers.google.com/workspace/drive/picker/guides/overview-desktop)
- [Choose Google Drive API scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth)
- [Store application-specific data](https://developers.google.com/workspace/drive/api/guides/appdata)
- [Drive API usage limits](https://developers.google.com/workspace/drive/api/guides/limits)
- [Unverified apps](https://support.google.com/cloud/answer/7454865) and [OAuth verification FAQ](https://support.google.com/cloud/answer/13463817)
- [Restricted scope verification](https://developers.google.com/identity/protocols/oauth2/production-readiness/restricted-scope-verification) and [Security assessment](https://support.google.com/cloud/answer/13465431)
- [Google Workspace user data and developer policy](https://developers.google.com/drive/api/policy)
- [Android: Open files using the Storage Access Framework](https://developer.android.com/guide/topics/providers/document-provider)

Community:
- [personal-storage: drive.file folder access spike](https://github.com/hualinh1012/personal-storage/issues/2)
- [Uppy PR: selectFolders option and drive.file folder access](https://github.com/transloadit/uppy/pull/6385)
- [rclone Google Drive documentation](https://rclone.org/drive/) and [rclone PR #10266: drive.file tied to client_id](https://github.com/rclone/rclone/pull/10266)
- [rclone forum: changing client_id with drive.file](https://forum.rclone.org/t/google-drive-changing-client-id-and-scope-drive-file-write-access/6693)
- [Google Developer forum: drive.file on shared folders](https://discuss.google.dev/t/google-drive-sheets-api-with-drive-file-scope-on-shared-folder-files/402266)
- [Google Developer forum: CASA for a client-only Android app](https://discuss.google.dev/t/does-a-client-only-android-app-with-no-server-need-the-casa-security-assessment-for-drive-readonly/393638)
- [Apps Script community: CASA verification cost](https://groups.google.com/g/google-apps-script-community/c/XgsHT2Fr7u8)
