# PSC Clean-room Policy

**Status:** decided 2026-11-28 (option B: permissive reuse allowed). PSC is licensed under Apache-2.0. The rules below are the permanent policy; a formal two-step clean-room process is not required.

## Why this matters: Commonplace may be paid

Commonplace, PSC's lead client, may be sold as a paid app (its own planning mentions a paid license, per-platform pricing and a trial). PSC code is embedded in Commonplace, so whatever PSC contains ends up in a paid product. That has consequences:

- **PSC's own license must allow embedding in a paid, closed-source app.** Apache-2.0 (decided) does.
- **Copyleft code inside PSC could force source disclosure.** Copied or closely derived code from a strong-copyleft project (GPL, AGPL), or a copyleft dependency, may oblige Commonplace to publish its source or prevent closed distribution. App-store distribution adds its own compatibility questions for GPL-family licenses.
- **Several reference projects use copyleft or proprietary terms.** Their licenses must be checked from primary sources before anything is reused, and their code must not be copied in the meantime.
- **Provenance protects a paid product.** A record of where every design and code element came from is what lets the owner sell Commonplace without legal doubt.

## Rules

1. **Copying is allowed only from permissively licensed code** (the "Allowed without review" licenses below: MIT, Apache-2.0, BSD and similar). When code is copied or closely adapted:
   - keep the original copyright and license notice, and add an entry to `THIRD_PARTY_NOTICES.md` (project, URL, license, version or commit, what was taken);
   - name the source in the PR's "Sources consulted";
   - mark the copied part with a short comment pointing to the notice entry;
   - make sure it fits PSC's architecture and passes the same tests and lints as PSC's own code.
   **Never copy, translate or closely paraphrase code** under GPL, LGPL, AGPL, SSPL, MPL, "non-commercial", source-available or unclear terms, or with no license at all. Public availability is not permission.
2. **Learning from other projects is allowed** through user documentation, published protocol descriptions and design write-ups (Joplin, Obsidian, Syncthing, rclone, Konode, Anytype/any-sync, Nextcloud, Notesnook and similar). Record what was read.
3. **Primary sources first:** official provider documentation and terms, standards (IETF RFCs), official platform documentation and dependency public API documentation.
4. **Dependencies:** before adding one, even to a prototype, record its license, version, maintenance and platform support. Flag any copyleft, source-available, "non-commercial" or unclear license for owner review; do not add it to anything that could ship.
5. **Prototypes are throwaway.** Prototype code is not carried into production without a provenance and license review.
6. **Sources consulted:** every PR lists the sources and dependencies relied on (PR template). Never claim a source that was not used.
7. **Similarity:** if code looks unusually close to a project whose license is not permissive, stop, record the concern and rewrite from PSC's own specification and permitted sources.
8. **AI-generated code** follows the same rule: if a tool reproduces recognizable code from a non-permissive project, discard it.

## Dependency licenses

Allowed without review: Apache-2.0, MIT, BSD-2-Clause, BSD-3-Clause, ISC, Zlib, Unicode-3.0, CC0-1.0. Allowed with a note in the PR: MPL-2.0 (file-level copyleft; PSC must not modify MPL files without publishing those changes). Not allowed in anything that ships: GPL, LGPL, AGPL, SSPL, "non-commercial" or unclear licenses. `cargo-deny` enforces this list in CI (`docs/ARCHITECTURE.md` §9.3).
