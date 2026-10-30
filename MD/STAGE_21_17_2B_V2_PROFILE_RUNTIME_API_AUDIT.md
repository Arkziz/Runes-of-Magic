# Stage 21.17.2b - V2 profile runtime/API audit

- Status: **PASS**
- Conclusion: **GO_TO_21_17_2C_PROFILE_IMPLEMENTATION**
- Mode: **STATIC / READ-ONLY**
- Production SQLite opened: **False**
- Manual game check: **NOT_REQUIRED**

## Runtime composition
- `rom_v2/app/development_bot.py:118` `DevelopmentBotConfig`
- `rom_v2/app/development_bot.py:122` `IndependentDevelopmentBot`
- `rom_v2/app/development_bot.py:50` `self._api.send_message`
- `rom_v2/app/development_bot.py:38` `TelegramBotApi`
- `rom_v2/app/development_bot.py:100` `self._api.get_updates`
- `rom_v2/app/development_bot.py:113` `self.handle_update`
- `rom_v2/app/runtime_launcher.py:34` `TelegramRegistrationFlow`
- `rom_v2/app/runtime_launcher.py:35` `DevelopmentBotConfig`
- `rom_v2/app/runtime_launcher.py:36` `IndependentDevelopmentBot`
- `rom_v2/app/runtime_launcher.py:34` `AccountService`
- `rom_v2/app/runtime_launcher.py:34` `CharacterService`
- `rom_v2/app/runtime_launcher.py:36` `TelegramBotApi`

## Telegram transport capabilities
- **send_message:** True
- **get_updates:** True
- **callback_ack:** False
- **inline_keyboard:** True
- **edit_message:** False

## Lookup and profile-facing APIs
- `rom_v2/presentation/registration_flow.py:28` `TelegramRegistrationFlow._account_id`
- `rom_v2/presentation/registration_flow.py:29` `TelegramRegistrationFlow._character_id`
- `rom_v2/domain/primary_stats.py:49` `AttributePointState.effective_without_equipment`
- `rom_v2/domain/derived_stats.py:68` `derive_stats`
- `rom_v2/domain/full_stat_snapshot.py:116` `base_primary_stats`
- `rom_v2/domain/full_stat_snapshot.py:122` `build_full_stat_snapshot`
- `rom_v2/domain/resource_lifecycle.py:20` `initialize_resources`
- `rom_v2/domain/resource_lifecycle.py:34` `set_current_resources`
- `rom_v2/domain/resource_lifecycle.py:40` `restore_resources`
- `rom_v2/domain/durability.py:35` `clamp_durability`
- `rom_v2/domain/durability.py:56` `damage_durability`
- `rom_v2/domain/durability.py:65` `contributes_stats`
- `rom_v2/application/full_stat_snapshot_service.py:22` `FullStatSnapshotService.for_profile`
- `rom_v2/application/services/rune_lifecycle.py:10` `RuneLifecycleGateway.load_equipment`
- `rom_v2/application/services/rune_lifecycle.py:11` `RuneLifecycleGateway.rune_quantity`
- `rom_v2/application/services/rune_lifecycle.py:64` `RuneLifecycleService._owned_equipment`
- `rom_v2/presentation/development_shell.py:32` `build_status_view`

## Gaps that 21.17.2c may implement
- Extend TelegramBotApi with callback acknowledgement before interactive profile callbacks are connected.
- Use send-message navigation initially or add edit-message support in the Telegram adapter with tests.
- Implement immutable profile view models plus a pure presenter/menu; do not import V1 handlers or copy V1 calculations.

## Decision

Proceed to 21.17.2c only with the owners and adapter capabilities recorded here. New code must be orchestration/presentation only unless this audit proves a capability is absent.
