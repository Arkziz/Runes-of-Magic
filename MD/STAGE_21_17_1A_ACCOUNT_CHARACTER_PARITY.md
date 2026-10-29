# Stage 21.17.1a - Account/character parity refinement

- Status: **PASS**
- Conclusion: **CONTRACT_PARITY_ACCEPTED**
- Parent HEAD: `a5394e967a7cb391f89618414620d5433739dbcb`
- Manual game check: **NOT_REQUIRED**

## Scope
Typed presentation contract for account registration, character creation/reset and restart state. Covers happy, rejection, repeat, stale and restart cases.

## Boundaries
Telegram wiring and runtime registration remain intentionally absent. Production persistence and SQLite were not changed. V1 was not imported or executed.

## Authoritative owners
- `rom_v2/application/account_service.py`
- `rom_v2/application/character_service.py`
- `rom_v2/presentation/account_character_contract.py`

## Acceptance
Stable status, reason, identifier, state and localization-key inputs are verified by maintained contract tests. No user-facing text is embedded as a technical key.
