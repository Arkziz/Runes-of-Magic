# Stage 21.18.2 — Read-only V1 World/Map/Travel Audit

## Status

`PASS_READ_ONLY` / `GO_TO_21_18_2A_PRE_MUTATION_OWNER_AND_RUNTIME_REVIEW`

## Effective V1 ownership map

- World graph and canonical travel duration: `data/location_graph.py`.
- Human localized location names: `data/locations.py`.
- Travel text/presentation helpers: `data/travel_presentation.py`.
- Persistent location/travel state: `db_modules/location.py` plus `migrations/049_persistent_location_travel.py`.
- Telegram map dispatch: `handlers/map.py`.
- Current-location context: `systems/location_context_system.py`.
- Travel start/status/complete/cancel policy: `systems/travel_system.py`.

The machine report preserves symbols, callbacks, constants, SQL/migration evidence and candidate duplicates with source lines. Duplicate candidates remain `UNCERTAIN` unless effective registration/call-path evidence resolves them.

## Required parity fixtures

The next implementation must cover location resolution, graph destinations, unlocks, start, ETA, completion, cancellation, busy restrictions, restart recovery and stale/replayed actions. User-facing text must use localized human names and the term «розділ»; technical location identifiers are prohibited.

## V2 readiness

V2 already contains a location catalog, travel aggregate, travel service and map-presentation contract. Their presence does not prove the full playable path. Repository/UoW ownership, persistence wiring, injected clock, composition and Telegram dispatch remain gated for a focused pre-mutation review.

## Decision

Proceed to `21.18.2a` only through a pre-mutation owner/runtime review. No production code or database was changed or opened. Manual game check: `NOT_REQUIRED`.
