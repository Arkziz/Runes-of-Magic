# Stage 21.18.2a V2 Travel Schema Owner Review

## Status

`PASS_READ_ONLY` / `GO_TO_21_18_2A_PERSISTENCE_AND_RUNTIME_COMPLETION_IMPLEMENTATION_WITH_V2_SCHEMA_OWNER`

## Decision

The travel schema is owned by a new append-only V2 migration: `rom_v2/infrastructure/persistence/migrations/v005_world_travel.py`. The canonical expected metadata remains owned by `rom_v2/infrastructure/persistence/schema_contract.py`; registration/application remains owned by `rom_v2/infrastructure/persistence/migrator.py`.

`v001_v2_baseline.py` is immutable for this stage. `migrations/049_persistent_location_travel.py` is a read-only V1 parity reference and must never be imported by V2 runtime. Repository, Unit of Work and launcher code must not execute schema-creation SQL.

## Contract

The new V2 table owns active/terminal travel rows, revision, aware UTC timestamps, one-active-per-user uniqueness, due ordering and user history indexes. Fresh migration, idempotency and live-schema-contract equality must be proven against an isolated temporary database.

## Scope

The implementation allowlist is expanded only by the new V2 migration, schema contract, migrator if registration requires it, and a focused schema migration test. No production code or database was changed or opened. Manual game check: `NOT_REQUIRED`.
