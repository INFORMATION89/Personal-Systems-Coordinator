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

## 8. Permanent decentralization; no PSC-operated backend

- PSC will never operate a centralized backend, first-party cloud storage, content relay, hosted coordinator, managed storage service, or mandatory account system.
- Coordination and synchronization logic runs on user devices inside consuming applications and/or user-controlled local components, according to the approved architecture.
- Data is stored or transported through folders and providers selected by the user. A provider may be commercial or self-hosted, but it remains external to PSC and under the user's choice/control.
- Do not add a server as a shortcut for synchronization, sharing, notifications, identity, or realtime collaboration.
- Provider APIs may have quotas, rate limits, OAuth verification requirements, policy changes and costs; research and disclose these without turning them into a PSC-operated service.
- A proposal to reverse this constraint is a product-direction change, not a routine technical optimization, and requires explicit owner approval.

## 9. Host-platform integration

- PSC is shared infrastructure for consuming applications, not an end-user application or UI shell. Its scope does not prescribe or provide the consuming apps' screens, visual design system, navigation, or UI framework.
- Each consuming application chooses its own interface and application architecture. Platform-native UI requirements, where applicable, belong to that application; they are not PSC constraints.
- PSC contracts should remain platform-neutral where practical. File access, credential storage, background work, permissions, and other OS capabilities must be implemented through appropriate host-platform APIs or adapters.
- Do not promise continuous background synchronization where the operating system does not allow it.
- Provide documented integration surfaces and bindings appropriate to supported host platforms without requiring a particular UI toolkit.

## 10. Research before implementation

No provider, cryptographic design, CRDT, database, transport or language is selected by this document. Verify current official provider documentation and run small interoperability experiments before making architectural commitments.


## 11. Licensing and resource provenance

- Evaluate whether and how PSC may be monetized, distributed, or supported commercially without violating its permanent decentralized/provider-based constraint. A paid license, SDK, support offering or other model may be researched, but none is selected by this principle.
- Keep PSC's own software license distinct from licenses of dependencies, platform SDKs, sample code, documentation, test fixtures and other bundled materials.
- Maintain a provenance and license inventory for code, APIs, services, datasets, models, fonts, icons, media and generated assets used by PSC or its integration examples.
- Check commercial-use, redistribution, modification, attribution, copyleft/source-disclosure, patent, trademark, quota, fee and data-use conditions using current primary terms.
- Classify resources as allowed, allowed with conditions, or prohibited/unresolved. Unknown or incompatible rights block inclusion or release until resolved.
- Do not infer permission from public availability, no-cost access, open-source status, or AI generation. Retain required notices, attributions, source offers and an SBOM where practical.
- No public license or monetization model is chosen by this principle. Record the decision separately after commercial and legal implications are evaluated.
