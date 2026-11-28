# Personal Systems Coordinator — Rules

**Status:** working rules baseline · 2026-11-28 · adapted from INFORMATION89/Meridian-Engine `RULES.md`

These rules govern research, design, prototyping and (later) implementation of PSC. They take priority over speed and convenience. Product principles live in `docs/PRINCIPLES.md` and agreed decisions in `docs/DECISIONS.md`; these rules do not repeat them. Changes to these rules need owner approval and an entry in `docs/DECISIONS.md`.

## 1. Read before every session

1. Read `AGENTS.md`, this file and `CLEAN_ROOM.md`. Every AI-assisted task follows `AI_POLICY.md` and `AI_COST_POLICY.md`; read the relevant sections, not the whole set every time.
2. Read the active work package in `docs/RESEARCH_PLAN.md` and the decisions in `docs/DECISIONS.md`. A research finding is not an approved requirement.
3. Inspect the actual repository before relying on a summary. Start with targeted searches.
4. Report contradictions, missing decisions and outdated documents before relying on them.

## 2. PSC's purpose and boundaries

1. PSC is shared sync infrastructure that the owner's apps embed. It runs on the user's devices. It never operates a server, relay, managed storage or account system.
2. Sync covers one person's own devices. Sharing content with other people is not a PSC feature.
3. Synced content is Markdown, images and JSON. Any other content type needs an explicit decision.
4. PSC has no user interface and prescribes none.
5. Apps depend on PSC; PSC never depends on an app. PSC must build and pass its own tests without Commonplace, Solstice or any other consumer.
6. Each app owns its data's meaning and its conflict rules for that data. PSC owns generic sync mechanics.
7. PSC does not decide when apps sync. The host app schedules sync through the platform's facilities; PSC respects background limits.

## 3. Approval boundaries and technical autonomy

1. **Owner review is required** before changing product scope or principles; privacy or consent commitments; licensing; anything with paid or recurring cost; creating provider registrations (cloud projects, OAuth clients); selecting a provider, file format, implementation language or license; public contract or file-format compatibility; data retention; releases; and destructive or external actions.
2. **Technical autonomy is expected** inside an approved work package: research method, report structure, experiment design, test fixtures and throwaway prototype code.
3. Before asking for owner review, present the problem, evidence, a bounded proposal, alternatives, trade-offs, maintenance cost and privacy/licensing implications. Do not ask the owner to choose between unexplained options.
4. Do not interrupt the owner for routine choices.

## 3a. Maintainable products, not vibe coding

1. `docs/ARCHITECTURE.md` is the design. Build what it says; do not add systems it doesn't describe.
2. Prefer established libraries (`docs/ARCHITECTURE.md` §9.1) and platform standards over home-made code.
3. Research before building anything new; propose it to the owner; then code.
4. No hard-coded limits, intervals, names, file types or user-facing text. Use the configuration module and error codes.
5. Follow each platform's guidelines (sign-in in the system browser, platform schedulers, platform pickers).
6. Code must pass the guardrails in `docs/ARCHITECTURE.md` §9.3 before review.

## 4. Architecture boundaries (for design and prototypes)

1. Provider-specific concepts (Drive file IDs, page tokens, Graph delta links, SAF URIs, security-scoped bookmarks) stay inside that provider's adapter. They must never leak into the portable contract or app-facing API.
2. Adapters declare capabilities; the coordinator chooses strategies from them. Do not pretend providers are equivalent.
3. Access storage, network, time and platform services through explicit interfaces, so core logic is testable without a real provider, filesystem, device or clock.
4. Keep the portable contract language-neutral. Do not commit to interfaces in a specific language before the contract and fixtures exist (`docs/RESEARCH_PLAN.md` WP7).
5. Device-local state (tokens, cursors, paths, URIs, bookmarks) never goes into the shared workspace.

## 5. Data integrity rules for sync

1. Never lose user data. On doubt, keep both versions.
2. Never overwrite based on wall-clock time alone. Device clocks drift.
3. A missing file in a listing is not a deletion. Deletions are explicit tombstones.
4. Conditional writes: if the remote changed since it was read, re-read and apply the content type's conflict rule. Never retry by overwriting.
5. Advance a sync checkpoint only after the related changes are durably applied.
6. Repeated delivery must not create duplicates.
7. An older app version must never corrupt files written by a newer one. Preserve unknown fields and frontmatter keys.
8. Protect against mass deletion: large or unexpected delete sets need a safeguard and must be recoverable.
9. A successful upload is not proof that every device synced. Report status honestly.

## 6. Research evidence

1. Use official provider documentation, standards (RFCs) and official platform documentation as primary sources. Record the URL and the date checked.
2. Label every claim: **[Official]**, **[Community]**, **[Inference]** or **[Untested]**. Community posts and blogs are never treated as official.
3. If a primary source could not be read in full (for example a blocked host), say so.
4. Separate documented behaviour from tested behaviour. Only an experiment run with recorded results counts as tested.
5. Re-check provider terms, scopes and quotas when they matter for a decision; they change.

## 7. Providers and external services

1. Request the least-privilege scope that does the job. Do not request broad scopes to avoid an experiment.
2. Use official APIs and operating-system file interfaces. Do not scrape consumer interfaces or bypass provider restrictions.
3. Respect rate limits, quotas, backoff guidance and terms. A test must never bypass them.
4. Experiments use dedicated test accounts and test projects. Never use the owner's personal account data, and never commit client IDs paired with secrets, tokens or refresh tokens.
5. Credentials stay in the platform's secure storage or the developer's local, untracked configuration. Never in source control, fixtures, logs or reports.

## 8. Privacy

1. Sync is explicit and per category. Never sync location, credentials or data outside the approved categories.
2. Sync consent, Meridian data contribution, telemetry and external AI access are separate purposes.
3. Do not add telemetry, analytics or remote logging.
4. Never log tokens, authorization codes, file contents or personal paths.

## 9. Clean-room development and licensing

Whether PSC adopts a formal clean-room process is undecided; until then follow the interim rules in `CLEAN_ROOM.md`. Commonplace may be a paid app, so nothing that could ship may carry copyleft or unclear licensing without owner review. Review every dependency's license, maintenance, platform support and size before adding it, and record it. PSC's own license is not yet chosen (`docs/RESEARCH_PLAN.md` WP11); do not add a LICENSE file or license headers without owner approval.

## 10. Testing and verification

Follow `AI_COST_POLICY.md` §7 for choosing checks.

1. Sync logic must be tested with deterministic, offline fixtures: workspace states, operations and expected outcomes.
2. Fixtures cover interruption, duplicates, concurrent edits, deletions, stale devices, lost cursors, revoked access and provider errors (429, 5xx, out of storage).
3. Live provider checks are manual or explicitly marked, minimal and within provider terms. They supplement fixtures and never replace them.
4. Report platform and provider results per target. "It compiled" or "it worked once" is not support.

## 11. Documentation and decisions

1. One source of truth per topic. `docs/DECISIONS.md` holds agreed decisions; `docs/RESEARCH_PLAN.md` holds the plan and task routing; research reports hold findings.
2. When a decision changes, update `docs/DECISIONS.md` with the date.
3. Mark ideas, findings and proposals as such until approved.
4. Fix contradictions in the authoritative document; do not leave two versions looking valid.

## 12. Git and pull requests

1. Work on a feature branch; merge through a pull request.
2. Keep commits focused, and few (normally 1–3 per PR). Do not combine unrelated changes.
3. Never commit credentials, tokens, personal data, local configuration, IDE state, build output or machine-specific paths.
4. Never put a CI-skip marker on a commit that changes anything other than documentation.
5. Use `.github/pull_request_template.md` and fill every section.
6. CI must pass before merge.

## 13. Done means verified

A change is complete only when:

1. it follows the active work package and these rules;
2. claims are sourced and labelled, and experiments report what actually ran;
3. relevant checks pass;
4. `docs/DECISIONS.md`, the research plan and affected reports reflect the result;
5. the PR states what was and was not verified.
