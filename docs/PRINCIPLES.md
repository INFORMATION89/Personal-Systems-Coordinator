# Principles

**Status:** initial product constraints · 2026-11-26

These principles guide research. They do not select a provider or implementation technology.

## 1. Local-first

- Applications remain useful without network access.
- Each application keeps a local copy of the data it needs.
- A provider outage, expired credential or unavailable network must not make local data inaccessible.
- Synchronization is eventual; the system must explain when a device is behind.

## 2. User chooses the storage

- Do not require a first-party cloud account.
- Prefer providers and folders the user already controls.
- A user-selected local folder must be a first-class option, not an export-only escape hatch.
- Users may choose how that folder is synchronized, including third-party tools or no synchronization at all.
- Provider-specific features and limitations must be disclosed.

## 3. Applications retain ownership

- Each application remains the source of truth for its own domain semantics.
- PSC handles transport, shared identity/metadata contracts and synchronization mechanics; it should not absorb weather, notes, timer or calendar business rules.
- Cross-application references must use stable identifiers and explicit contracts, not direct access to another application's private database.
- One application must not silently rewrite another application's records.

## 4. Portable and inspectable data

- Prefer documented, versioned and reasonably open formats.
- Preserve user-readable formats where appropriate (for example, Markdown for notes).
- Data must be exportable without requiring the original application or provider.
- Schema migrations and provider metadata must not destroy the original user content.
- Be explicit where binary, encrypted or provider-specific data cannot be edited by external tools.

## 5. Consent and privacy

- Synchronization is an explicit user choice, separate from core functionality.
- Explain which categories of data are synchronized, to which provider, and from which applications/devices.
- Allow users to inspect, pause and disconnect synchronization.
- Do not silently sync precise location, location history, raw weather observations, forecast logs, provider credentials or unrelated application data.
- Data sharing for improving public weather models, analytics, telemetry and cross-device synchronization are separate purposes with separate consent.
- Revoking access prevents future synchronization but cannot reliably erase copies already downloaded to another device or provider.
- Evaluate encryption at rest, end-to-end encryption, key recovery and external-editor compatibility as explicit trade-offs.

## 6. Reliability and conflict safety

- Offline changes must be retained until they can be synchronized or safely resolved.
- Conflict behavior must be defined by data type; "last write wins" is not a universal policy.
- Deletions require explicit semantics so that removed data is not accidentally resurrected.
- Duplicate delivery must not create duplicate records.
- Provider throttling, partial failures, expired authorization and interrupted writes must be handled safely.
- A successful provider upload must not be confused with successful synchronization to every device.

## 7. Provider-neutral architecture

- Applications should depend on stable PSC contracts, not provider-specific APIs.
- Providers are adapters with declared capabilities and limitations.
- Do not assume that Drive, iCloud Drive, GitHub, WebDAV or a local folder expose equivalent semantics.
- Do not assume a provider API offers a filesystem, transaction, change feed or background execution on every platform.

## 8. No hidden operating cost

- The baseline architecture must not require us to operate a paid synchronization backend.
- API quotas, rate limits, OAuth verification, provider policy changes and operational costs still require research.
- Do not introduce paid APIs, hosted services or recurring costs without explicit approval.

## 9. Platform-native behavior

- Shared data contracts and synchronization policy may be common.
- File access, credential storage, background work, permissions and user experience must respect each platform's native capabilities.
- Do not promise continuous background synchronization where the operating system does not allow it.

## 10. Research before implementation

No provider, cryptographic design, CRDT, database, transport or language is selected by this document. Verify current official provider documentation and run small interoperability experiments before making architectural commitments.
