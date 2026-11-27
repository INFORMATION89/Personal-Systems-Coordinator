# Personal Systems Coordinator

A provider-neutral foundation for optional data synchronization and interoperability across a family of personal applications.

**Status: research and architecture planning. Not implementation-ready.**

The project explores how applications such as Solstice, Notes, Clock and Calendar can keep user-controlled data available across the user's devices without requiring us to operate a proprietary cloud or mandatory account system.

The intended model is permanently decentralized, local-first and provider-neutral: applications own their domain data; users choose whether to synchronize it and which existing storage provider or folder to use. PSC will not operate a central backend, first-party cloud, content relay or mandatory account system.

## Start here

- [Product overview](docs/PRODUCT_OVERVIEW.md) — purpose, scope and boundaries.
- [Principles](docs/PRINCIPLES.md) — product and privacy constraints.
- [Research plan](docs/RESEARCH_PLAN.md) — questions to investigate before selecting an architecture.
- [Solstice integration](docs/INTEGRATION_SOLSTICE.md) — the first candidate use case.
- [Decision register](docs/DECISIONS.md) — confirmed direction and unresolved choices.

## Current status

- The repository is a planning and research workspace.
- Solstice is the first candidate application because its recommendation preferences and personalization data could benefit from cross-device continuity.
- Provider APIs, synchronization semantics, data schemas, encryption design and implementation technology have **not** been selected.
- An independent review with Claude Opus is planned before the architecture is treated as ready for implementation.

## Non-goals

This project is not intended to become:
- a mandatory account system for the application family;
- a first-party cloud storage business;
- a replacement for Google Calendar, Apple Calendar or other external services;
- an opaque database that traps the user's data;
- a reason for each application to surrender ownership of its own domain model.

See the documents above before proposing implementation work.
