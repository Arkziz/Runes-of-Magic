# Stage 21.18.2a Pre-mutation Owner and Runtime Review

## Status

`PASS_READ_ONLY` / `GO_TO_21_18_2A_PERSISTENCE_AND_RUNTIME_COMPLETION_IMPLEMENTATION`

## Approved owners

- World graph: `rom_v2/content/world_graph.py`.
- Localized location catalog: `rom_v2/content/location_catalog.py`.
- Domain transitions: `rom_v2/domain/travel_aggregate.py`.
- Application orchestration: `rom_v2/application/travel_service.py`.
- Pure map DTO/callback contract: `rom_v2/application/map_presentation.py`.
- Navigation labels/markup: `rom_v2/presentation/navigation.py`.
- Runtime composition: `rom_v2/app/runtime_launcher.py`.
- Dispatch only: `rom_v2/app/development_bot.py`.

## Boundaries

Persistence must own travel records, due queries, one-active uniqueness, revision/CAS, transactions and rollback. A Telegram map/travel flow may render and delegate, but must not own SQL or travel policy. Completion remains server-authoritative. Clock and busy state are injected application boundaries.

## Presentation

User text uses the term «розділ», resolves names through the canonical localized catalog, and never exposes technical location/node IDs.

## Scope

The machine report contains the evidence inventory, exact candidate implementation allowlist, callback namespace and mandatory restart/stale/idempotency tests. No production code or database was changed or opened. Manual game check: `NOT_REQUIRED`.
