# Stage 21.18.1b inventory/equipment UoW runtime wiring correction

Both runtime UoW factories now receive the canonical callable `V2ConnectionFactory.connect_read_write`, not the non-callable factory object. A real isolated runtime smoke test opens inventory and equipment UoWs.

Status: `PASS_AUTOMATED_PENDING_MANUAL`.
