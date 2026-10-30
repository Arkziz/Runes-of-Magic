# Stage 21.17.3 - Character restart/reset audit

- Status: **PASS**
- Conclusion: **GO_TO_21_17_3A_RESET_IMPLEMENTATION**
- Mode: **STATIC / READ-ONLY**
- Production SQLite opened: **False**
- Manual game check: **NOT_REQUIRED**

## Reset owners
- `rom_v2/application/character_ports.py:10` `delete`
- `rom_v2/application/character_service.py:31` `reset`
- `rom_v2/application/guild_core_service.py:44` `delete`
- `rom_v2/application/inventory_ports.py:12` `delete_instance`
- `rom_v2/domain/battle_persistence.py:120` `recover_persisted_encounters_after_restart`
- `rom_v2/domain/dev_data_operations.py:52` `reset`
- `rom_v2/domain/simulator_adapters.py:139` `delete`
- `rom_v2/infrastructure/persistence/character_repository.py:21` `delete`
- `rom_v2/infrastructure/persistence/inventory_repository.py:21` `delete_instance`
- `rom_v2/infrastructure/persistence/migrator.py:86` `_delete_v2_database_files`
- `rom_v2/presentation/account_character_contract.py:62` `present_restart`
- `rom_v2/presentation/registration_flow.py:22` `reset_name`
- `tests_v2/test_account_character_parity_contract.py:25` `test_stale_reset_target_is_explicit_not_found`
- `tests_v2/test_account_character_parity_contract.py:28` `test_restart_without_character_returns_registration_state`
- `tests_v2/test_account_character_parity_contract.py:32` `test_restart_with_character_returns_ready_state`
- `tests_v2/test_account_character_persistence.py:15` `test_create_read_repeat_and_restart_are_persistent`
- `tests_v2/test_admin_crystals.py:41` `test_rollback_restart`
- `tests_v2/test_bag_expansion.py:59` `test_restart_replay_and_reset_survival`
- `tests_v2/test_base_equipment_shop.py:65` `test_restart_replay`
- `tests_v2/test_battle_persistence.py:29` `test_expiry_boundary_and_restart_recovery`
- `tests_v2/test_character_lifecycle.py:17` `test_reset_removes_character_and_requires_registration`
- `tests_v2/test_crystal_wallet_ledger.py:57` `test_restart_replay`
- `tests_v2/test_daily_reward.py:65` `test_restart_replay`
- `tests_v2/test_dev_data_operations.py:11` `reset`
- `tests_v2/test_dev_data_operations.py:33` `test_give_reset_set_delegate_and_commit`
- `tests_v2/test_direct_trade.py:18` `test_restart_recovery`
- `tests_v2/test_gold_wallet.py:82` `test_restart_replay_uses_persisted_operation`
- `tests_v2/test_location_catalog.py:16` `test_immutable_and_restart_stable`
- `tests_v2/test_potion_trading.py:62` `test_restart_replay`
- `tests_v2/test_premium_shop.py:59` `test_restart_replay`
- `tests_v2/test_rune_lifecycle.py:31` `test_atomic_insert_extract_and_restart_shape`
- `tests_v2/test_world_graph.py:29` `test_immutable_and_restart_stable`

## Dependency evidence
- Character-reference files: **18**
- Foreign-key declarations mentioning character: **6**
- Discovered tables: **18**

## Required policy
- Reset deletes the character aggregate only; the account remains active.
- Reset requires an explicit confirmation callback and cancel performs no mutation.
- A second/stale confirmation fails closed and must not delete the account.
- After committed reset, /start opens the registration wizard.
- Re-registration reuses the existing account and creates exactly one character.
- All character-owned dependent rows must be deleted by verified repository/UoW behavior or explicit same-transaction cleanup.

## Decision

Proceed to implementation refinement 21.17.3a only with confirmation/cancel routing, account preservation, same-transaction dependent cleanup, temporary SQLite cardinality tests, and manual Telegram acceptance.
