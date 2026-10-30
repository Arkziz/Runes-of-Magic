# Stage 21.17.2f - Existing-character start idempotency

`/start` now checks the canonical read-only profile query before opening registration. Existing characters route directly to the V2 menu; missing characters enter registration. A defensive `ALREADY_EXISTS` result no longer claims that a character was newly created. Manual Telegram acceptance is required before Stage 21.17.3.
