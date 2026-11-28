# Personal Systems Coordinator

A provider-neutral foundation for optional data synchronization and interoperability across a family of personal applications.

**Status: research and architecture planning. Not implementation-ready.**

The project explores how applications such as Solstice, Commonplace (notes), Clock and Calendar can keep user-controlled data available across the user's devices without requiring us to operate a proprietary cloud or mandatory account system.

The intended model is permanently decentralized, local-first and provider-neutral: applications own their domain data; users choose whether to synchronize it and which existing storage provider or folder to use. PSC itself will never operate a centralized backend, first-party cloud storage, hosted coordinator, content relay, managed storage, or mandatory account system.

## Start here

- [Product overview](docs/PRODUCT_OVERVIEW.md) — purpose, scope and boundaries.
- [Principles](docs/PRINCIPLES.md) — product and privacy constraints.
- [Research plan](docs/RESEARCH_PLAN.md) — goals, research work packages and sequencing before selecting an architecture.
- [Solstice integration](docs/INTEGRATION_SOLSTICE.md) — the first candidate use case (small preference records).
- [Commonplace integration](docs/INTEGRATION_COMMONPLACE.md) — the notes app; the most demanding sync requirements (plain Markdown files, attachments, conflicts).
- [Decision register](docs/DECISIONS.md) — confirmed direction and unresolved choices.
- [Glossary](docs/GLOSSARY.md) — working vocabulary (PSC, Meridian, adapter, workspace, namespace...).

## Research findings

Initial provider and architecture research is documented:
- [Provider comparison](docs/research/PROVIDER_COMPARISON.md)
- [Platform constraints](docs/research/PLATFORM_CONSTRAINTS.md)
- [Sync semantics and architecture options](docs/research/SYNC_SEMANTICS.md)
- [Security, authorization and consent](docs/research/SECURITY_AND_CONSENT.md)
- [Calendar integrations](docs/research/CALENDAR_INTEGRATIONS.md) — boundary notes only; calendar services are the future Calendar app's responsibility
- [Existing synchronization systems and reusable technologies](docs/research/EXISTING_SYSTEMS_AND_TECHNOLOGIES.md)

Key unresolved issues, tracked as work packages in the research plan:
- **Provider authorization (WP1):** who owns each provider registration, and whether Google Drive's least-privilege `drive.file` scope lets separate applications share one workspace. A multi-app proof of concept is required before committing to a shared provider workspace.
- **Data contracts and interoperability (WP3):** the portable record format, cross-app references and how app ownership is respected in a shared folder have not been researched yet.

## Current status

- The repository is a planning and research workspace.
- Solstice is the first candidate application because its recommendation preferences and personalization data could benefit from cross-device continuity.
- Provider APIs, synchronization semantics, data schemas, encryption design and implementation technology have **not** been selected.
- An independent review with Claude Opus is planned before the architecture is treated as ready for implementation.

## Non-goals

This project is not intended to become:
- a mandatory account system for the application family;
- a centralized backend, hosted coordinator, content relay, or managed storage service operated by PSC;
- a first-party cloud storage business;
- a replacement for Google Calendar, Apple Calendar or other external services;
- an opaque database that traps the user's data;
- a reason for each application to surrender ownership of its own domain model;
- a UI framework, design system, or application shell for consuming products. Each app defines its own user interface and architecture.

See the documents above before proposing implementation work.
