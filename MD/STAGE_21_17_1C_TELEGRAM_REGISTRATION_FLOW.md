# Stage 21.17.1c - Telegram registration flow

- Automated status: **PASS**
- Conclusion: **AWAITING_MANUAL_GAME_CHECK**
- Parent HEAD: `526e650e5df98fe68271bc362b84678e2c3034d6`
- Manual game check: **REQUIRED**

## Automated acceptance
V2 `/start`, name entry, six-class selection, Back, Cancel, validation, persistent creation and idempotent repeat entry passed maintained tests.

## Mandatory manual check
1. Start the V2 development bot for an allowlisted test user.
2. Send `/start`.
3. Enter a valid name and choose a class.
4. Confirm exactly one character is created.
5. Restart the bot and send `/start` again; no duplicate account or character may appear.
6. Verify Back and Cancel.

Stage 21.17.1c remains open until the manual scenario is recorded as PASS.
