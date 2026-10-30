# Stage 21.17 - Clean-environment integration closure

## Status

**PASS_ACCEPTED** - Stage 21.17 is closed at parent HEAD `316f1e5150009cc34fc5554f8f5bdb5c2b59047f`.

## Accepted integration

- isolated V2 registration and character persistence;
- idempotent `/start` for existing characters;
- persisted profile query and Telegram profile menu;
- explicit reset confirmation, non-mutating cancel, account preservation and re-registration;
- canonical six-class labels from `DEFAULT_CLASS_CATALOG`;
- zero parallel six-class presentation catalogs;
- side-effect-free canonical V2 CI.

## Manual evidence

The user-performed Telegram acceptance verified reset cancel, reset confirm, account preservation, replacement-character registration, restart persistence, and matching `🏹 Скаут` labels in registration result and profile.

## Deferred boundaries

Production entrypoint switching remains deferred. Stage 21.18 scope and formal acceptance requirements must be established by a read-only audit before further implementation.
