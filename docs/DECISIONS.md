# Decision Register

**Last updated:** 2026-11-28

This register separates the direction already agreed in product discussions from technical questions that remain open. A research finding is not automatically a decision.

## Confirmed direction

| Topic | Current position | Status |
|---|---|---|
| Project | Independent shared foundation for the application family | Agreed direction |
| Lead client | Commonplace is the app that needs PSC most; first research and development are oriented towards it. Solstice follows as a simpler second client. | Agreed (2026-11-28) |
| Sync scope | One person's own devices only (for example phone → user's cloud provider → PC). Multi-person sharing and collaboration are not PSC features. | Agreed (2026-11-28) |
| Synced content | Simple files only: Markdown, images and JSON. Any other content type needs an explicit decision. | Agreed (2026-11-28) |
| Role of PSC | The shared foundation that all of the owner's apps plug into for sync. Its code runs on the user's devices; it is never a hosted service. | Agreed (2026-11-28) |
| Workspace layout | A root folder holding PSC's own folder plus one folder per app; each app owns its folder; PSC gives apps shared information (apps, devices, status). Details in ARCHITECTURE.md §3–§4. | Owner direction (2026-11-28) |
| Core language | Owner leaning to Rust; confirm as D1 in ARCHITECTURE.md §1. | Pending owner confirmation |
| Design Freeze | No product code until all decisions for the first viable product are made (IMPLEMENTATION_PLAN.md Phase A). | Agreed (2026-11-28) |
| AI usage | Sonnet codes; Opus only for the named reviews or on request; owner on Claude Pro; no AI-generated art (icons, mockups and suggestions allowed); owner is non-technical, so structural choices come with pros and cons. | Agreed (2026-11-28) |
| Provider registrations | One family-level registration per provider (Google Cloud project, Apple team, Entra app, Dropbox app, GitHub App), owned by the owner and registered as **Personal Systems Coordinator**. Google's shared workspace still depends on experiments E1/E2. | Agreed (2026-11-28) |
| First-release providers | Google Drive, GitHub and self-hosted (WebDAV and the user-selected folder). Dropbox, OneDrive, iCloud and others are deferred, not rejected; the owner judged more options too much for average users. | Agreed (2026-11-28) |
| Minimum providers | Google Drive and GitHub are the accepted minimum, alongside the always-available user-selected folder. Further providers are ordered in research/PROVIDER_CANDIDATES.md for owner review. | Agreed minimum (2026-11-28) |
| Self-hosting | Self-hosted storage (user-selected folder, WebDAV, later self-hosted Git) always remains available; no managed provider is ever the only option. | Agreed (2026-11-28) |
| GitHub | Considered as an optional provider for Commonplace, following Konode's single-private-repository model; a PSC GitHub App is the preferred route to evaluate. | Research direction (2026-11-28) |
| Model attribution | AI-assisted commits, PRs and reports name the tool and model tier (AI_POLICY.md §5). | Agreed (2026-11-28) |
| Clean-room process | Undecided; interim no-copying and provenance rules apply until WP11 decides PSC's license, with Commonplace possibly being paid. | Undecided (2026-11-28) |
| Working rules | Agent instructions, rules, interim clean-room rules, AI and AI-cost policies, agent guides, PR template and PR hygiene check adopted from Meridian-Engine and adapted to PSC. | Adopted at owner request (2026-11-28) |
| Far-future integrations | Clock Pomodoro sync, a Solstice menubar app reading Solstice personalization data, and Calendar ↔ Commonplace mentions are recorded as context in FUTURE_INTEGRATIONS.md. Today's design must not rule them out, but none is scheduled. | Context only (2026-11-28) |
| Quality bar | The apps are expected to be distributed to other people (for example friends), so PSC must meet a public-release standard for data safety and must cope with apps and devices being updated at different times. | Agreed (2026-11-28) |
| Primary purpose | Optional cross-device synchronization of one person's app data; cross-app interoperability is secondary | Agreed direction |
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

- Final public product/feature name. Provider registrations and consent screens use "Personal Systems Coordinator"; whether that is also the consumer-facing brand is open.
- Provider order beyond the agreed minimum (Google Drive, GitHub, user-selected folder).
- Whether Google Drive, iCloud Drive, OneDrive, Dropbox, WebDAV, GitHub or local folders can share one abstraction without unacceptable limitations.
- For Google Drive: whether one family project can share a workspace across apps and platforms (experiments E1/E2).
- Shared folder layout, file formats and manifest format.
- Sync transport, change journal and conflict resolution algorithms.
- Whether any data needs end-to-end encryption and how keys are recovered.
- Data categories eligible for synchronization in each application (within the Markdown/image/JSON limit).
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
