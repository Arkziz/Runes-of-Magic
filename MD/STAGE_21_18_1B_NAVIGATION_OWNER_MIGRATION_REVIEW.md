# Stage 21.18.1b Navigation Owner Migration Review

## Status

`PASS_READ_ONLY` / `GO_TO_NAVIGATION_OWNER_MIGRATION_IMPLEMENTATION`

## Approved ownership

`rom_v2/presentation/navigation.py` becomes the single owner of user-visible navigation labels, presentation callback constants, and pure reply/inline keyboard builders. Existing flows remain the authoritative behavior owners.

## User decision incorporated

The public `Скинути персонажа` button and its public navigation entry are removed. The underlying reset capability is preserved but is not exposed to players. A future developer reset command is outside this migration and requires separate assigned work.

## Approved removals

- shell inline `Профіль`;
- inventory `За ID`;
- public `Скинути персонажа`;
- redundant profile inline `Назад` where persistent `🔙 Назад` is available.

## Approved retained actions

- shell inline `Стан V2`;
- persistent `👤 Профіль`;
- persistent `🎒 Інвентар` and `🔙 Назад` in the profile/inventory section;
- inline `Екіпірування`, item details, pagination, equip/unequip and `До інвентарю`;
- registration controls.

## Scope

The machine report contains the exact implementation allowlist, owner matrix, callback policy, tests, rollback requirements, and manual Telegram acceptance contract.

Manual game check: `NOT_REQUIRED_FOR_REVIEW`.
