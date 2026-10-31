# Stage 21.18.1b profile/inventory navigation correction

Corrected the inventory flow to call canonical `ProfileQueryService.by_telegram_user_id`. The persistent navigation now follows V1 parity: `/start` exposes `👤 Профіль`; profile exposes `🎒 Інвентар` and `🔙 Назад`; back restores `👤 Профіль`. V2 callback owners remain canonical.

Status: `PASS_AUTOMATED_PENDING_MANUAL`.
