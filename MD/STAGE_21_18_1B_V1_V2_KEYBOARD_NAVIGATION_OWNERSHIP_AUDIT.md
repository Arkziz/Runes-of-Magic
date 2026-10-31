# Stage 21.18.1b V1/V2 keyboard and navigation ownership audit

## Status

`PASS_READ_ONLY` / `GO_TO_NAVIGATION_OWNER_MIGRATION_REVIEW`

## Evidence-based finding

The audit confirms distributed keyboard markup and duplicate user-facing profile entry points. It does **not** claim multiple authoritative profile or inventory behavior owners. V2 flow behavior remains delegated to its existing flow owners.

## Confirmed defects

- Shell inline `Профіль` duplicates the persistent `👤 Профіль` entry.
- Inventory exposes `За ID`, which maps to internal `inventory_id`; that sort is already the default and is not a useful user action.
- Labels and pure keyboard dictionaries are currently constructed in several presentation/runtime files.

## Recommended owner

Create `rom_v2/presentation/navigation.py` as the single owner of user-visible navigation labels and pure keyboard builders. Flows retain behavior; the bot retains dispatch only. Do not copy the large V1 keyboard module mechanically.

## V1 reference

Keyboard evidence was found in **34** V1 files. The machine report records each file, label, callback and keyboard-construction line.

## Manual check

`NOT_REQUIRED`: audit only.
