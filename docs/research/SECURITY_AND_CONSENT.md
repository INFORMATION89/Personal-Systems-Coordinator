# Security, Authorization and Consent Research

**Research date:** 2026-11-27  
**Status:** requirements and trade-offs; no encryption architecture approved.

## 1. Threat model

PSC should assume:
- devices can be lost, stolen, rooted, jailbroken or compromised;
- provider accounts can be compromised independently of PSC;
- OAuth tokens can expire or be revoked;
- providers can be temporarily unavailable or return incomplete/error responses;
- shared folders can be edited or deleted by the user outside PSC;
- multiple devices can edit offline and reconnect in any order;
- a user may intentionally inspect, edit, copy or delete portable files outside our applications.

The design must prioritize data integrity, least-privilege access, transparent consent and recovery.

## 2. Native application OAuth

Mobile and desktop apps are public clients: an embedded static client secret cannot be treated as confidential.

Research supports Authorization Code with PKCE using the system browser/authentication session:
- Google supports PKCE for installed apps and documents platform-specific installed-app OAuth clients: [Google OAuth for native apps](https://developers.google.com/identity/protocols/oauth2/native-app).
- Dropbox recommends PKCE for client-side/mobile/desktop apps and supports refresh tokens for background access: [Dropbox OAuth](https://docs.dropboxapi.com/dropbox-api/docs/oauth).
- Microsoft supports authorization-code flow with PKCE for mobile and desktop apps: [Microsoft identity platform authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow).
- General native-app guidance is standardized in [RFC 8252](https://www.rfc-editor.org/rfc/rfc8252.html).

### Requirements

- Use Authorization Code + PKCE for public native clients when supported.
- Use the system browser/authentication session, not an embedded credential-collecting WebView.
- Never ship a provider client secret and claim it is secure.
- Request the smallest scopes required for the exact feature.
- Keep provider access/refresh tokens in OS-protected credential storage.
- Never store credentials in Markdown, JSON workspace files, Git repositories or the shared sync folder.
- Never copy one device's OAuth refresh token to another device. Each device authorizes with its own OS credential store.
- Handle access revocation, invalid grants, account switching and disconnect.
- Avoid logging tokens, authorization codes, picker URLs containing sensitive state or remote file contents.

## 3. Provider authorization is not automatically shared across applications

The desired family experience is one Personal Ecosystem folder used by Solstice, Notes, Clock and Calendar. Provider APIs may scope authorization to an app, user and selected file.

Google's drive.file scope is intentionally limited to files created by the app or opened/shared with the app through its picker/file-selection flow. Google recommends it over broad Drive access where possible. See [Google Drive scopes](https://developers.google.com/workspace/drive/api/guides/api-specific-auth).

This creates an important design question: does each application need to select or authorize the shared root separately, and does selecting the root grant access to all existing and future children? Do not assume one app's OAuth consent authorizes the others.

A single shared OAuth identity, per-app client IDs in one cloud project, repeated Picker grants or a broader scope are possible design avenues, but none is approved. Validate the actual behavior and provider policy before choosing.

## 4. Consent must be per purpose and inspectable

Separate these purposes:
1. cross-device synchronization of the user's own data;
2. interoperability between the user's own apps;
3. optional contribution of weather error data to Meridian;
4. telemetry/analytics;
5. sharing data with external AI assistants or providers.

Enabling one must not enable another.

The user should be able to inspect:
- which application owns each data category;
- which categories are enabled for synchronization;
- which provider/workspace receives them;
- which devices currently participate;
- when each device last synchronized;
- whether content is plaintext or encrypted;
- how to pause, disconnect, export and restore.

Do not use a single generic "sync everything" consent without an inventory of included categories.

## 5. Encryption options

### Option A: provider-managed storage / plaintext files

The provider stores readable Markdown/JSON files. This enables:
- ordinary external Markdown editors;
- search and preview in the storage service;
- user inspection and manual repair;
- straightforward exports and migration.

Trade-off: the provider can technically read file contents and metadata, subject to its policies and security controls.

### Option B: end-to-end encrypted payloads

PSC encrypts content before it reaches the provider; only authorized devices hold the keys.

Potential benefits:
- storage provider cannot normally interpret the encrypted content;
- a compromised provider account exposes ciphertext rather than plaintext (assuming keys remain safe).

Costs:
- external editors and provider previews cannot read the payload;
- filename/folder/timestamp/size/access metadata may still leak unless separately minimized;
- key backup and recovery become critical;
- new-device enrollment requires a secure way to transfer or recover keys;
- provider-side content search and many convenience features no longer work;
- losing every authorized device and recovery key may mean permanent data loss.

### Option C: per-category encryption

A possible compromise:
- user-authored Markdown remains plaintext if the user chooses external editability;
- sensitive profile/preferences are encrypted;
- attachments can have a separate policy.

This is more flexible but increases complexity and must be visible to the user.

**No default encryption mode is selected.** The choice must be made at product level with a clear explanation of the trade-offs.

## 6. Identity and device authorization

Do not rely on hardware serial numbers, advertising identifiers or platform IDs as cross-device identity.

If a stable device identity is necessary for conflict provenance or device management:
- generate a random PSC-specific identifier locally;
- keep it in OS-protected local storage;
- let the user see and revoke the device;
- do not expose it outside the synchronization workspace unless necessary;
- rotate/re-enroll after compromise.

Revoking a device prevents future access only after credentials/keys are rotated or revoked. It cannot reliably erase data that device already downloaded.

## 7. Data minimization for Solstice

The first Solstice integration should consider only explicit recommendation preferences and any separately approved compact personalization state.

Do not silently include:
- precise coordinates or location history;
- raw forecast requests or response archives;
- raw station observations;
- Meridian's entire learning log;
- device identifiers unrelated to sync;
- provider tokens;
- anonymous weather-data contributions intended for model improvement.

The fact that a record exists in a local database is not sufficient reason to sync it.

## 8. Disconnect, deletion and recovery

Disconnect should:
- stop future sync attempts;
- revoke/delete local provider tokens where possible;
- show whether the user's remote files are retained or deleted (default should not unexpectedly delete the user's only copy);
- explain that disconnected devices may retain downloaded copies;
- allow the user to choose whether to keep or remove the local workspace;
- provide an explicit re-link/recovery path.

Deletion propagation requires tombstones and stale-device behavior; see SYNC_SEMANTICS.md.

## 9. Review checklist before production

- Threat model and misuse cases reviewed.
- OAuth redirect/deep-link handling tested against interception.
- PKCE and state/nonce validation verified.
- Tokens stored in platform secure storage and excluded from backups/export where appropriate.
- Minimum scopes documented and provider verification status known.
- Logs and crash reports inspected for credential/content leakage.
- Consent copy names providers, data categories and purposes.
- Disconnect and revocation tested.
- Lost-device and key-loss recovery tested.
- Plaintext and encrypted export behaviors documented.
- Applicable privacy law reviewed before any server or data collection is introduced.
