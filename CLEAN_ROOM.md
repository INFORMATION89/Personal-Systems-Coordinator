# PSC Clean-room Policy

Adapted from INFORMATION89/Meridian-Engine on 2026-11-28. This applies to all design and implementation work in Personal Systems Coordinator. It reduces copying risk but cannot guarantee that an AI model has never encountered similar public code.

**Permitted sources:** official provider API documentation and terms (Google Drive, Microsoft Graph, Dropbox, Apple), standards (IETF RFCs such as WebDAV, HTTP and OAuth for native apps), official platform documentation (Android, Apple, Windows, Linux), dependency public API documentation, published papers, and PSC's own approved specifications. Record the sources actually consulted.

**Other sync projects** (Joplin, Obsidian, Syncthing, rclone, Konode, Anytype/any-sync, Nextcloud, Notesnook and similar) may be studied through their user documentation, published protocol descriptions and public design write-ups, to learn patterns and failure modes. Their source code is not an implementation reference. Do not copy, translate, closely paraphrase or imitate their internal implementation. Public availability is not permission.

**Before implementing a substantive feature,** write an independently worded specification covering behaviour, file contracts, edge cases, failures and acceptance criteria, and have it reviewed. Implement from that specification without inspecting third-party implementation code for the same feature. Dependency public APIs may be used to integrate the dependency, not its internals as a template.

**Every implementation or prototype pull request** lists the PSC specification, standards, provider and platform documentation, and dependencies relied upon, with versions and licenses. Never claim to have consulted a source that was not used.

**If code looks unusually similar to another project,** stop, identify the concern, revisit the design from the specification and permitted sources, rewrite independently where needed, and record the resolution.

**Licenses:** review direct and transitive dependency licenses, maintenance and platform support, and preserve required notices. PSC's own license is not yet chosen; see `docs/RESEARCH_PLAN.md` WP11.
