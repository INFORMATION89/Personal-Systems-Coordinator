# PSC Clean-room Policy

**Status:** undecided · 2026-11-28. Whether PSC adopts a formal clean-room process, and how strict it is, will be decided together with PSC's license and distribution model (`docs/RESEARCH_PLAN.md` WP11). Until then, the interim rules below apply. They are chosen to keep every licensing option open.

## Why this matters: Commonplace may be paid

Commonplace, PSC's lead client, may be sold as a paid app (its own planning mentions a paid license, per-platform pricing and a trial). PSC code is embedded in Commonplace, so whatever PSC contains ends up in a paid product. That has consequences:

- **PSC's own license must allow embedding in a paid, closed-source app.** That points to a permissive license, a proprietary license, or dual licensing. Undecided.
- **Copyleft code inside PSC could force source disclosure.** Copied or closely derived code from a strong-copyleft project (GPL, AGPL), or a copyleft dependency, may oblige Commonplace to publish its source or prevent closed distribution. App-store distribution adds its own compatibility questions for GPL-family licenses.
- **Several reference projects use copyleft or proprietary terms.** Their licenses must be checked from primary sources before anything is reused, and their code must not be copied in the meantime.
- **Provenance protects a paid product.** A record of where every design and code element came from is what lets the owner sell Commonplace without legal doubt.

## Interim rules (until a policy is decided)

1. **No copying.** Do not copy, translate or closely paraphrase source code from other projects into PSC, whatever their license.
2. **Learning from other projects is allowed** through user documentation, published protocol descriptions and design write-ups (Joplin, Obsidian, Syncthing, rclone, Konode, Anytype/any-sync, Nextcloud, Notesnook and similar). Record what was read.
3. **Primary sources first:** official provider documentation and terms, standards (IETF RFCs), official platform documentation and dependency public API documentation.
4. **Dependencies:** before adding one, even to a prototype, record its license, version, maintenance and platform support. Flag any copyleft, source-available, "non-commercial" or unclear license for owner review; do not add it to anything that could ship.
5. **Prototypes are throwaway.** Prototype code is not carried into production without a provenance and license review.
6. **Sources consulted:** every PR lists the sources and dependencies relied on (PR template). Never claim a source that was not used.
7. **Similarity:** if code looks unusually close to another project's, stop, record the concern and rewrite from PSC's own specification and permitted sources.

## To decide (WP11)

- PSC's license and distribution model, with Commonplace being paid as an explicit input.
- Whether a formal clean-room process is needed (separate specification and implementation steps, as Meridian-Engine uses) or whether the interim rules plus provenance records suffice.
- A dependency license allowlist and denylist for anything that ships inside a paid app.
- How notices and attribution are carried into consuming apps.
