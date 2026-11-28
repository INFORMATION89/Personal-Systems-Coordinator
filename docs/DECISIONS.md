# Decision Register

**Last updated:** 2026-11-28

This register separates the direction already agreed in product discussions from technical questions that remain open. A research finding is not automatically a decision.

## Confirmed direction

| Topic | Current position | Status |
|---|---|---|
| Project | Independent shared foundation for the application family | Agreed direction |
| First candidate client | Solstice | Agreed |
| Primary purpose | Optional cross-device synchronization and cross-app interoperability | Agreed direction |
| Storage model | User chooses an existing provider or a folder they control | Agreed direction |
| First-party cloud | PSC will never operate a centralized backend, first-party cloud storage, hosted coordinator, content relay, managed storage or mandatory account | Permanent product constraint |
| Consuming-app UI | Each application chooses its own UI framework and architecture; PSC does not prescribe or provide a UI | Outside PSC scope |
| Host-platform integration | OS-specific APIs/adapters are used where necessary; background execution limits must be respected | Research requirement |
| Linux synchronization | Linux is a conditional sync target. If reliable, maintainable sync proves disproportionately difficult or costly, drop Linux from the supported sync matrix rather than compromising other platforms. A local-only Linux app remains a separate product decision. | Agreed scope constraint |
| Calendar service integrations | Connecting Google Calendar, EventKit, Microsoft Graph or CalDAV belongs to the future Calendar app, not PSC. PSC focuses on synchronization of app-owned data. | Agreed scope (2026-11-28) |
| Application ownership | Each app retains its domain model and local functionality | Agreed constraint |
| User consent | Sync is explicit and separate from telemetry or weather-data contribution | Agreed constraint |
| Current phase | Documentation and research before implementation | Agreed |

## Current research preference (not an approved technical decision)

- Google Drive is currently the leading managed-provider candidate to investigate first. This reflects the project owner's present preference and comparative research, not a commitment to ship it as the first or only provider. A multi-app, least-privilege shared-folder proof of concept and independent Opus review are required before deciding.

## Not decided

- Final public product/feature name. The repository is named Personal-Systems-Coordinator; treat that as the project identifier, not a settled consumer-facing brand.
- Provider order or launch provider.
- Whether Google Drive, iCloud Drive, OneDrive, Dropbox, WebDAV, GitHub or local folders can share one abstraction without unacceptable limitations.
- Whether provider connections are authorized once per app, per platform, or through another safe model.
- Shared folder layout, file formats and manifest format.
- Sync transport, change journal and conflict resolution algorithms.
- Whether any data needs end-to-end encryption and how keys are recovered.
- Data categories eligible for synchronization in each application.
- Background-sync expectations on each platform.
- Implementation language, libraries and minimum platform versions.
- Final host-platform matrix, including whether any Linux-only local application remains worthwhile if Linux synchronization is dropped.
- Shared domain/core implementation technology, SDK packaging, and its binding strategy for consuming applications.
- Whether and how PSC should be monetized or commercially distributed, including cost, legal and operational implications while preserving permanent decentralization.
- The license and distribution model for PSC's own code, separate from licenses governing dependencies and assets.
- The permitted-resource policy and inventory process for dependencies, SDKs, APIs, datasets, models, fonts, icons, media, sample code and other third-party materials.

## Constraints on future decisions

- Verify current official provider documentation before selecting a provider.
- Record the date and sources for provider capability claims.
- Do not treat a successful upload as proof that all devices have synchronized.
- Do not silently sync sensitive or location-derived data.
- Do not turn an Opus review into an accepted decision without reviewing it with the project owner.
- Update this register when a decision is explicitly approved.
