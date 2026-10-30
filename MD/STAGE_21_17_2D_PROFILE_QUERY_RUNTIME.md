# Stage 21.17.2d - Profile query/runtime integration

Read-only persisted account/character lookup is connected to the V2 Telegram profile flow. The flow presents only values actually owned by the persisted character aggregate. No V1 imports, SQL duplication, or stat formula duplication were introduced. Manual Telegram acceptance is required before Stage 21.17.3.
