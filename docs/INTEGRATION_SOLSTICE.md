# Solstice Integration

**Status:** candidate use case · research required · no implementation approved

Solstice is the first candidate application for Personal Systems Coordinator because the user wants weather recommendation preferences and eligible personalization data to remain consistent across devices.

Reference repository: [INFORMATION89/Solstice](https://github.com/INFORMATION89/Solstice).

## User-visible goal

A person configures Solstice on one device and can choose to carry those recommendation-related preferences to another device without maintaining a separate Solstice cloud account.

The integration should preserve Solstice's local-first behavior. Solstice must continue to work when no provider is connected, when synchronization is paused, or when a provider is unavailable.

## Candidate data categories to investigate

These are candidates, not a final sync schema:

1. **Recommendation preferences**
   - User-adjusted comfort preferences (for example, warmer or cooler).
   - Explicit choices that shape "Best time to be outside", "What to wear" and future recommendations.
   - User-configured recommendation thresholds and related settings, once their meaning and units are stable.

2. **Weather and source preferences**
   - Selected sources and per-place overrides, if the settings are portable and can be mapped safely on another device.
   - App-level display and recommendation settings, distinct from device-specific permissions and capabilities.

3. **Derived personalization state**
   - Compact, versioned state that represents learned preferences or corrections, only if research shows it improves recommendations on another device.
   - Per-place model error history and local forecast corrections from Meridian's learning system are a separate question. Assess whether to keep, recompute, export or synchronize them; do not assume they belong in the first integration.

## Data that must not be silently included

- Precise location or location history.
- Raw station observations and raw forecast logs.
- Device identifiers or advertising identifiers.
- Provider OAuth tokens or credentials.
- Weather data contributions intended to improve Meridian for everyone.
- Any unrelated Solstice data simply because it exists in local storage.

A future design may offer an explicit, inspectable opt-in for selected data categories. Cross-device sync consent must remain separate from Meridian's optional data-contribution consent, which is off by default.

## Ownership boundaries

- **Solstice owns** recommendation semantics, weather preferences, local personalization rules and decisions about which data are portable.
- **Meridian owns** weather-engine semantics and its local forecast-learning behavior.
- **Personal Systems Coordinator owns** generic provider adapters, shared synchronization mechanics, portable envelope/manifest contracts, revision metadata and sync status.
- **The provider owns** its storage and account-specific authorization rules.

PSC must not import Solstice or Meridian code. Solstice must not depend directly on Google Drive, iCloud Drive or another provider API for its domain logic.

## Calendar and cross-app data

This integration does not make Google Calendar or Apple Calendar a synchronization provider for Solstice preferences. External calendar integrations are separate service adapters.

## Integration checkpoint

When the Solstice recommendation settings and personalization model are being designed or implemented:

1. List the data that should be consistent across the user's devices.
2. Separate user preferences from derived learning state and raw forecast history.
3. Define stable IDs, units, schema versions and migration behavior for eligible data.
4. Specify what stays local and why.
5. Define opt-in, provider selection, inspection, pause, disconnect and recovery behavior.
6. Add an adapter boundary so Solstice can later use PSC without importing provider-specific APIs.

Do not block the first recommendation design on an unimplemented coordinator. Design a clean future boundary and integrate PSC only after its research and contracts are approved.

## Acceptance criteria for a future integration

- Solstice works fully without a linked provider.
- Synchronization is explicitly enabled by the user.
- The user can see which Solstice data categories are synchronized and where.
- No telemetry or public weather-data contribution is enabled by linking a provider.
- Two devices converge after reconnecting without silently losing user changes.
- Local recommendation behavior remains available during provider outages.
- The design documents what is not synchronized as clearly as what is.
