# Stage 21.18.1b menu-entry correction

The V2 `/start` path first installs `🎒 Інвентар` as a persistent Telegram reply keyboard, then sends the canonical inline shell menu. Telegram does not permit reply and inline keyboards in one markup object. Exact text input delegates to the existing `v2:inventory:open` callback owner. V1 callback names and category policy were not copied.

Status: `PASS_AUTOMATED_PENDING_MANUAL`. Restart the bot and repeat manual acceptance from `/start`.
