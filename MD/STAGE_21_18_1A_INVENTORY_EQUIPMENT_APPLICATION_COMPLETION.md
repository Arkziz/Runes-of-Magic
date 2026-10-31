# Stage 21.18.1a - Inventory/equipment application completion

`PASS_AUTOMATED`. `rom_v2/domain/inventory.py` is now the single narrow owner of inventory membership, capacity and pure addition planning. `ItemInstance` remains owned by `domain/item.py`; equipment policy remains owned by `domain/equipment.py`; persistence and UoW owners were not duplicated. `InventoryService` delegates its capacity/stack planning to the aggregate. No migration, Telegram UI or production database access was added.

Manual game check: `NOT_REQUIRED`. The Telegram slice is deferred to 21.18.1b.
