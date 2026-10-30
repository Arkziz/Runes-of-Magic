# Stage 21.17.3b - Character reset confirmation

The V2 profile now exposes explicit reset confirmation. Cancel is non-mutating, stale confirmation fails closed, confirmed reset deletes only the character, and the account remains available for re-registration. Temporary SQLite tests prove cardinality 1/1 -> 1/1 on cancel and 1/1 -> 1/0 on confirm. Manual Telegram acceptance is required.
