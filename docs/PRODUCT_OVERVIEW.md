# Product Overview

**Status:** exploratory brief · 2026-11-26

## Purpose

Personal Systems Coordinator (PSC) is a shared foundation that may allow independent personal applications to exchange and synchronize user-approved information across devices.

The working vision is:

> A coordination layer that helps a person's applications and devices stay consistent, while allowing the person to choose where their data lives.

The foundation should make it possible for an application to keep its data locally, then synchronize selected data through an existing provider or a user-managed folder when the person chooses to enable it.

## The problem

The application family is expected to include products with different responsibilities:

- **Solstice:** weather, recommendations and locally derived personalization.
- **Notes:** Markdown documents, notes, tasks and structured personal information.
- **Clock:** timers, focus sessions and activity history.
- **Calendar:** external calendar events plus first-party activity layers and references.

Users may want these applications to share selected information across phones and computers. Examples include:

- Solstice recommendation preferences remaining consistent across devices.
- Clock sessions appearing as a distinct activity layer in Calendar.
- Calendar showing links to Notes tasks or documents and opening the owning application.
- Each application remaining useful when another device or provider is unavailable.

## Product model

The candidate model has three separate responsibilities:

1. **Applications own domain data.** Solstice owns weather preferences and weather-derived personalization; Clock owns timer sessions; Notes owns notes and tasks; Calendar owns its calendar-specific data and views.
2. **PSC coordinates portable data exchange and synchronization.** It should provide shared contracts and provider integration boundaries without understanding every application's business logic.
3. **External providers transport or store data.** The user may connect an existing cloud account or choose a local folder that is synchronized by software of their choice.

This separation must survive platform differences and provider limitations.

## Candidate storage and sync destinations

These are candidates to research, not promised integrations:

- a user-selected local folder;
- Google Drive;
- iCloud Drive;
- OneDrive and Dropbox;
- WebDAV-compatible services, including self-hosted storage;
- a GitHub repository as an advanced, version-oriented option;
- Syncthing-managed or otherwise externally synchronized folders.

The same provider will not necessarily support every application, platform or data type equally well. The research must document those gaps.

## Separate external-service integrations

Some services are not storage backends for PSC. For example, connecting Google Calendar, Apple Calendar, Outlook or a CalDAV server is an integration with an existing calendar service.

Calendar-provider integration and synchronization of our own application data must remain separate capabilities with separate authorization, scopes and failure handling.

## What PSC is not

- It is not a mandatory centralized server.
- It is not a new identity provider that every user must register with.
- It is not a replacement for the applications' local databases.
- It is not a universal shared database that every application can freely mutate.
- It is not a promise that every provider supports seamless, real-time, bidirectional synchronization.
- It does not make telemetry, collaborative data contribution or analytics necessary.

## First candidate use case

Solstice is the first integration candidate. Its recommendation preferences and potentially portable personalization state could follow the user between devices. This is a research target, not a decision to synchronize every weather record or learning artifact.

See [Solstice Integration](INTEGRATION_SOLSTICE.md).
