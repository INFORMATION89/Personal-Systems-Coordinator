# Provider Authorization (WP1)

**Research date:** 2026-11-28
**Status:** desk research complete for Google Drive, Apple, Microsoft and Dropbox (2026-11-28). No experiment has run yet. No registration model is approved.
**Prepared with:** Claude Code, tier O (research only); not yet reviewed by the owner.
**Scope:** §1–§8 Google Drive; §9 Apple; §10 Microsoft OneDrive; §11 Dropbox; §12 the cross-provider registration recommendation (WP1 questions 1–6).

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
- Apple, Microsoft and Dropbox findings are in §9–§11; each has its own items to verify.
- Whether `drive.appdata` (hidden, deleted if the user removes the app) is useful for PSC metadata. It is not suitable for user-visible notes.

## 9. Apple: iCloud Drive and CloudKit (WP1 question 5)

**Findings**
- **Containers can be shared within one developer team.** Each value in an app's iCloud container entitlement must be that app's bundle identifier, or that of another app submitted under the same team identifier. Wildcards are not allowed. [Official, Apple's archived entitlement reference; current key names should be re-checked, because sources name both `com.apple.developer.ubiquity-container-identifiers` and `com.apple.developer.icloud-container-identifiers`]
- **CloudKit containers can likewise be shared across a team's apps** through entitlements. [Official, from the earlier provider comparison]
- **The container stays with the app.** If an app moves to another developer team, its container goes with it. [Community]
- **No API outside Apple platforms.** On Windows, iCloud Drive is only reachable as a folder through iCloud for Windows. There is no public iCloud Drive API for Android. [Official, from the platform constraints report]

**What it means**
- On Apple devices, all of the owner's apps under one Apple developer team can share one iCloud container. That is the Apple counterpart of Google model A, and it works by configuration, not by experiment. [Inference]
- iCloud cannot be the phone-to-PC route for an Android phone. For an iPhone with a Windows PC, the PC would use iCloud for Windows as a plain folder. [Inference]
- **No restricted-scope reviews, quotas or consent screens** comparable to Google's. The user's iCloud storage plan is the limit. [Inference]

**To verify:** current entitlement key names in Xcode; whether a shared container can be exposed as a user-visible folder in iCloud Drive (so files are inspectable); behaviour under iCloud for Windows.

## 10. Microsoft OneDrive (Graph) (WP1 question 6)

**Findings**
- **App folder scope:** `Files.ReadWrite.AppFolder` limits an app to its own folder, usually `/Apps/{Application Name}` in the user's OneDrive, reached through `special/approot`. It is created on first use. [Official]
- **The folder is visible to the user,** who keeps full control and can add or remove files in it. [Official] So files the user adds through OneDrive should be visible to the app, unlike Google's `drive.file`. [Inference; confirm]
- **Not for large files.** Microsoft positions the app folder for configuration, temporary storage and drafts, and suggests `Files.ReadWrite` when users need to choose save locations. [Official]
- **Work and school accounts:** feedback reports that `Files.ReadWrite.AppFolder` alone is not usable on business accounts. [Community] PSC's audience is personal accounts, so this is likely a minor issue. [Inference]
- **Registration:** an Entra app registration can accept personal Microsoft accounts, alone or alongside work and school accounts. [Official] One registration can carry several platform configurations (mobile and desktop redirect URIs). [Inference from standard Entra practice; confirm]
- **Publisher verification** is free and needs no license. It adds a verified badge to the consent prompt and avoids admin-consent blocks in organizations. It requires a Microsoft Partner Center account. [Official]

**What it means**
- The app folder belongs to the registration. If every family app uses one Entra registration, they share `/Apps/{name}`. With one registration per app, each app gets its own folder. [Inference; confirm with a test]
- **Good fit for Commonplace's user-visible files.** Files sit in a visible folder that the user can browse, and user-added files are probably visible to the app. The "large files" caution matters for images. [Inference]

**To verify:** that user-added files appear through `approot` and the delta feed; size behaviour for images; one registration serving several apps and platforms.

## 11. Dropbox (WP1 question 6)

**Findings**
- **Two access types:** App folder (read and write to one dedicated folder for the app) and Full Dropbox. Dropbox recommends App folder when the app only needs files it created, and asks apps to use the least privilege that works. [Official]
- **App folders cannot be shared with other users.** Irrelevant here, since PSC syncs one person's devices. [Official]
- **Development status:** a new app works like a production app but can link at most 500 Dropbox users. Once it has linked 50 users, it has two weeks to apply for and receive production approval, or linking new users is frozen. [Official] Approval is per app, not per access type. [Community]
- **OAuth with PKCE** for mobile and desktop, with refresh tokens for background access. [Official, from the earlier security report]

**What it means**
- As with Microsoft, the app folder belongs to the Dropbox app (app key). A shared family app key gives a shared folder; separate app keys give separate folders. [Inference; confirm]
- **Distributing to friends** stays well under 500 users, but crossing 50 linked users starts the two-week production-approval clock. Plan approval before a wider release. [Inference]

**To verify:** whether user-added files in the app folder are visible to the app (likely, since it is a normal folder); whether one app key can serve several separately distributed apps under Dropbox's terms.

## 12. Registration recommendation across providers (WP1 question 1)

**The pattern.** For every provider, the least-privilege option is an area tied to the registration: Google `drive.file` (files the app created), Microsoft's app folder, Dropbox's app folder, Apple's team container. **Whoever owns the registration decides which apps share data.** [Inference from §2–§11]

**Recommendation for owner review:** one family-level registration per provider, owned by the owner (model A), with PSC accepting client configuration from each host app rather than embedding any.

| Provider | Family-level registration | Sharing across the owner's apps | Main open risk |
|---|---|---|---|
| Google Drive | One Cloud project, one OAuth client per app and platform | Only if `drive.file` access is per project | E1/E2 not yet run; external files invisible |
| Apple | One developer team, shared container entitlement | Yes, by configuration | Apple devices only |
| Microsoft | One Entra registration with multiple platform configurations | Probably, through one app folder | Confirm one registration can serve several apps |
| Dropbox | One Dropbox app key | Probably, through one app folder | Terms for one key across several apps; production approval at 50 users |

**Why family-level**
- It keeps the future integrations possible (Solstice menubar app, Calendar ↔ Commonplace).
- One consent screen, one verification and one privacy policy per provider instead of one per app.
- The user connects their storage once per provider and app family, which suits "my phone syncs to my cloud, my PC syncs from it".

**Costs and risks**
- **Consent screens show the family name,** not "Commonplace". The family needs a brand name (still undecided).
- **Revoking access** in the provider's account settings probably disconnects all of the owner's apps at once. Disconnecting inside one app should only remove that app's local token. [Inference]
- **Shared quota** across all apps and users. Unlikely to bind at this scale, if sync avoids polling. [Inference]
- **One misbehaving app affects the whole registration's standing** with the provider. [Inference]
- **Paid Commonplace:** commercial distribution may change verification expectations and terms review for each provider. Check each provider's developer terms for commercial use before release. [Inference]

**Fallback:** per-app registrations (model B), if family-level sharing is impossible (Google E1/E2 fail) or terms forbid one registration across several apps. Each app then syncs only its own data, and cross-app features need another mechanism.

**Next steps (owner decisions first)**
1. Approve creating one Google test project and test accounts, so an S-tier session can run E1–E9. Tier O does no code for now.
2. Decide the family brand name for consent screens (it can be provisional for testing).
3. After E1/E2, choose model A or B for Google; then confirm the Microsoft and Dropbox inferences with small tests.

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

Apple, Microsoft and Dropbox (via search extracts; official unless marked):
- [Apple: Enabling iCloud Storage (entitlement reference, archived)](https://developer.apple.com/library/content/documentation/Miscellaneous/Reference/EntitlementKeyReference/Chapters/EnablingiCloud.html)
- [objc.io: Mastering the iCloud Document Store](https://www.objc.io/issues/10-syncing-data/icloud-document-store/) (community)
- [Microsoft Graph: App folder](https://learn.microsoft.com/en-us/graph/onedrive-sharepoint-appfolder) and [OneDrive special folders: approot](https://learn.microsoft.com/en-us/onedrive/developer/rest-api/concepts/special-folders-appfolder)
- [Microsoft Tech Community: AppFolder access for business accounts](https://techcommunity.microsoft.com/idea/microsoft365developerplatform/appfolder-api-access-for-business-accounts/3966638) (community)
- [Microsoft Entra: Publisher verification](https://learn.microsoft.com/en-ca/entra/identity-platform/publisher-verification-overview) and [Microsoft account identity provider](https://learn.microsoft.com/entra/external-id/microsoft-account)
- [Dropbox: DBX Platform developer guide](https://www.dropbox.com/developers/reference/developer-guide) and [Dropbox developer support](https://www.dropbox.com/en_GB/developers/support)
- [Dropbox forum: development user limit](https://www.dropboxforum.com/discussions/101000014/does-a-dropbox-app-have-a-limit-on-development-users/846671) (community)
