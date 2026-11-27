# Decision Register

**Last updated:** 2026-11-27

This register separates the direction already agreed in product discussions from technical questions that remain open. A research finding is not automatically a decision.

## Confirmed direction

| Topic | Current position | Status |
|---|---|---|
| Project | Independent shared foundation for the application family | Agreed direction |
| First candidate client | Solstice | Agreed |
| Primary purpose | Optional cross-device synchronization and cross-app interoperability | Agreed direction |
| Storage model | User chooses an existing provider or a folder they control | Agreed direction |
| First-party cloud | PSC will never operate a first-party cloud, centralized backend, hosted relay or mandatory account | Permanent product constraint |
| Native application UI | Platform-native UI; no Electron or web-wrapper desktop apps | Agreed constraint |
| Development order | Desktop first; first desktop OS remains undecided | Agreed direction |
| Application ownership | Each app retains its domain model and local functionality | Agreed constraint |
| User consent | Sync is explicit and separate from telemetry or weather-data contribution | Agreed constraint |
| Current phase | Documentation and research before implementation | Agreed |

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
- First desktop operating system (Windows or macOS); choose only after native architecture and feasibility prototypes.
- Linux native UI framework and final supported platform matrix.
- Shared domain/core implementation technology and its native binding strategy.
- Whether and how PSC should be monetized or commercially distributed, including costs and compatibility with permanent decentralization.
- The license for PSC's own code, distinct from dependency and asset licenses, and the resulting contribution, redistribution, copyleft, patent and commercial obligations.
- The permitted-resource policy and inventory process for dependencies, APIs, datasets, models, fonts, icons, media, sample code and other third-party materials.

## Constraints on future decisions

- Verify current official provider documentation before selecting a provider.
- Record the date and sources for provider capability claims.
- Do not treat a successful upload as proof that all devices have synchronized.
- Do not silently sync sensitive or location-derived data.
- Do not turn an Opus review into an accepted decision without reviewing it with the project owner.
- Update this register when a decision is explicitly approved.
