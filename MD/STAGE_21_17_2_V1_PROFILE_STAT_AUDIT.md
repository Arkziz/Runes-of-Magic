# Stage 21.17.2 - Read-only V1 profile/stat audit

- Status: **PASS**
- Conclusion: **GO_TO_PROFILE_PRESENTER**
- Branch: `rewrite/rom-v2`
- HEAD before: `5c8363c8f35393fede94a4d238f7d9926a337253`
- Production mutation: **NONE**
- Production SQLite opened: **False**
- game.db-wal / game.db-shm: **NOT MANIPULATED**
- Manual game check: **NOT_REQUIRED**

## Scope

The audit traces V1 profile presentation, stat/resource calculation inputs, equipment, rune, durability and enhancement effects. V1 is parsed statically and is never imported or executed.

## Inventory

- V1 Python files parsed: 270
- V2 Python files parsed: 162
- Relevant modules: 415
- Profile/presentation entry candidates: 932
- Duplicate relevant symbol groups: 126

## Candidate owners by contract

### profile
- `handlers/combat.py:2125` - `register_combat_handlers`
- `handlers/city.py:496` - `register_city_handlers`
- `systems/simulation/world_progression.py:49` - `run`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `handlers/player_interaction.py:224` - `_register_player_interaction_base_handlers_12_6_8`
- `handlers/dev.py:184` - `register_dev_handlers`
- `handlers/combat.py:2376` - `attack`
- `handlers/profile.py:887` - `register_profile_handlers`
- `handlers/story_quests.py:346` - `register_story_quest_handlers`

### primary_stats
- `handlers/combat.py:2125` - `register_combat_handlers`
- `handlers/city.py:496` - `register_city_handlers`
- `systems/simulation/world_progression.py:49` - `run`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `handlers/player_interaction.py:224` - `_register_player_interaction_base_handlers_12_6_8`
- `handlers/dev.py:184` - `register_dev_handlers`
- `systems/pvp_adaptive_balance_optimizer.py:320` - `run_optimizer`
- `handlers/combat.py:2376` - `attack`
- `handlers/player_interaction.py:960` - `_trade_register_amount_input_12_6_3`

### derived_stats
- `handlers/combat.py:2125` - `register_combat_handlers`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `systems/pvp_adaptive_balance_optimizer.py:320` - `run_optimizer`
- `handlers/combat.py:2376` - `attack`
- `systems/pvp_round_engine.py:224` - `resolve_pvp_round`
- `handlers/combat.py:2177` - `hunt`
- `db_modules/generated_equipment.py:1006` - `create_generated_equipment_item`
- `systems/pvp_policy_metrics_audit.py:226` - `simulate_duel`
- `systems/simulation/excel_reporting.py:30` - `write_consolidated_workbook`

### resources
- `handlers/combat.py:2125` - `register_combat_handlers`
- `systems/simulation/world_progression.py:49` - `run`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `handlers/dev.py:184` - `register_dev_handlers`
- `systems/pvp_adaptive_balance_optimizer.py:320` - `run_optimizer`
- `handlers/combat.py:2376` - `attack`
- `systems/pvp_round_engine.py:224` - `resolve_pvp_round`
- `systems/pvp_combat_log.py:86` - `render_pvp_round_combat_log`
- `db_modules/dev_compat.py:289` - `reset_hero_for_test`

### equipment
- `handlers/combat.py:2125` - `register_combat_handlers`
- `handlers/city.py:496` - `register_city_handlers`
- `systems/simulation/world_progression.py:49` - `run`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `handlers/dev.py:184` - `register_dev_handlers`
- `systems/pvp_adaptive_balance_optimizer.py:320` - `run_optimizer`
- `handlers/combat.py:2376` - `attack`
- `handlers/player_interaction.py:617` - `_register_player_trade_offer_editor_ux_handlers`
- `handlers/auction_house.py:1502` - `_auction_register_sell_inline_handlers_v1`

### runes
- `systems/simulation/world_progression.py:49` - `run`
- `handlers/dev.py:184` - `register_dev_handlers`
- `systems/simulation/progression_economy_reporting.py:39` - `build_economy_equipment_report`
- `db_modules/dev_compat.py:289` - `reset_hero_for_test`
- `systems/simulation/excel_reporting.py:30` - `write_consolidated_workbook`
- `handlers/refine.py:423` - `register_refine_handlers`
- `systems/refine_system.py:112` - `perform_refine_attempt`
- `systems/auction_house_system.py:3080` - `build_auction_sell_item_review_text`
- `handlers/name_rune.py:5` - `register_name_rune_handlers`
- `handlers/runes.py:580` - `register_rune_master_shop_handlers`

### durability
- `handlers/combat.py:2125` - `register_combat_handlers`
- `systems/simulation/world_progression.py:49` - `run`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `handlers/combat.py:2376` - `attack`
- `db_modules/generated_equipment.py:1006` - `create_generated_equipment_item`
- `handlers/combat.py:1964` - `process_victory`
- `handlers/pvp_interaction.py:50` - `register_pvp_interaction_handlers`
- `systems/simulation/excel_reporting.py:30` - `write_consolidated_workbook`
- `systems/auction_house_system.py:3080` - `build_auction_sell_item_review_text`

### enhancement
- `systems/simulation/world_progression.py:49` - `run`
- `systems/pvp_adaptive_balance_optimizer.py:320` - `run_optimizer`
- `systems/simulation/progression_economy_reporting.py:39` - `build_economy_equipment_report`
- `systems/simulation/excel_reporting.py:30` - `write_consolidated_workbook`
- `handlers/refine.py:423` - `register_refine_handlers`
- `systems/refine_system.py:112` - `perform_refine_attempt`
- `systems/auction_house_system.py:3080` - `build_auction_sell_item_review_text`
- `systems/auction_house_system.py:4214` - `build_auction_buy_lot_details_v2`
- `systems/auction_house_system.py:1614` - `create_stack_auction_lot`
- `systems/drop_system.py:1270` - `simulate_central_drops`

### presentation
- `handlers/combat.py:2125` - `register_combat_handlers`
- `handlers/city.py:496` - `register_city_handlers`
- `handlers/combat.py:3184` - `combat_use_skill_callback`
- `handlers/combat.py:2685` - `use_skill_text_button`
- `handlers/player_interaction.py:224` - `_register_player_interaction_base_handlers_12_6_8`
- `handlers/dev.py:184` - `register_dev_handlers`
- `handlers/combat.py:2376` - `attack`
- `handlers/player_interaction.py:960` - `_trade_register_amount_input_12_6_3`
- `handlers/event_ui.py:110` - `register_event_ui_handlers`
- `handlers/pvp_round_ui.py:131` - `register_pvp_round_ui_handlers`

## V2 canonical boundary

The audit maps evidence to existing V2 owners and does not create a second formula or presenter owner.

- `rom_v2/application/base_equipment_shop.py`
- `rom_v2/application/durability_service.py`
- `rom_v2/application/enhancement_service.py`
- `rom_v2/application/equipment_generation_ports.py`
- `rom_v2/application/equipment_generation_service.py`
- `rom_v2/application/equipment_ports.py`
- `rom_v2/application/equipment_service.py`
- `rom_v2/application/full_stat_snapshot_service.py`
- `rom_v2/application/primary_stat_ports.py`
- `rom_v2/application/primary_stat_service.py`
- `rom_v2/application/resource_ports.py`
- `rom_v2/application/resource_service.py`
- `rom_v2/application/services/rune_lifecycle.py`
- `rom_v2/domain/combat_resources.py`
- `rom_v2/domain/derived_stats.py`
- `rom_v2/domain/durability.py`
- `rom_v2/domain/enhancement.py`
- `rom_v2/domain/equipment.py`
- `rom_v2/domain/equipment_generation.py`
- `rom_v2/domain/full_stat_snapshot.py`
- `rom_v2/domain/primary_stats.py`
- `rom_v2/domain/resource_lifecycle.py`
- `rom_v2/domain/runes.py`
- `rom_v2/infrastructure/persistence/equipment_repository.py`
- `rom_v2/infrastructure/persistence/equipment_unit_of_work.py`
- `rom_v2/infrastructure/persistence/migrations/v002_primary_stats_parity.py`
- `rom_v2/infrastructure/persistence/migrations/v004_equipment_slots_parity.py`
- `rom_v2/infrastructure/persistence/primary_stat_repository.py`
- `rom_v2/infrastructure/persistence/primary_stat_unit_of_work.py`
- `rom_v2/infrastructure/persistence/resource_repository.py`
- `rom_v2/infrastructure/persistence/resource_unit_of_work.py`

## Parity fixtures

- `v1_primary_stats_owner_fixture`: 3 source owner(s)
- `v1_derived_stats_owner_fixture`: 3 source owner(s)
- `v1_resources_owner_fixture`: 3 source owner(s)
- `v1_equipment_owner_fixture`: 3 source owner(s)
- `v1_runes_owner_fixture`: 3 source owner(s)
- `v1_durability_owner_fixture`: 3 source owner(s)
- `v1_enhancement_owner_fixture`: 3 source owner(s)

## Result

Unresolved required categories: `[]`.
Next canonical stage: `21.17.2a - V2 profile presenter and menu` only after this audit is reviewed and accepted.
