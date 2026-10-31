# Stage 21.18.1b - Telegram inventory/equipment slice audit

## Status

`PASS_READ_ONLY` / `GO_TO_21_18_1B_IMPLEMENTATION`

## Ownership

The Telegram slice must reuse the accepted inventory aggregate, item identity, equipment policy, application services, repositories and UoW. New presentation ownership is limited to `inventory_flow.py`; a separate `equipment_flow.py` is permitted only when it delegates to the same application services and does not duplicate item details, labels or policy. Current-character lookup must reuse `ProfileQueryService`.

## Callback contract

Namespaces are `v2:inventory:*` and `v2:equipment:*`. Item callbacks carry exact `inventory_id`; unequip callbacks carry canonical `slot_key`. Localized names are never identities. Stale, foreign and replayed callbacks fail closed.

## Presentation rules

Page size, default sort and allowed sort keys each have one canonical definition in the inventory presentation owner. Sorting, pagination, details and comparison are read-only. Telegram code performs no SQL and no compatibility calculations.

## Evidence

- V2 targets present: **7**
- V1 reference targets present: **3**
- existing V2 callback evidence rows: **0**
- callback conflicts: **0**

The machine report contains source hashes, definitions, imports, calls, literals, gaps, owner matrix, callback contract, exact candidate allowlist and formal acceptance matrix.

## Manual game check

`NOT_REQUIRED`: this patch is read-only. Implementation will require manual Telegram acceptance.
