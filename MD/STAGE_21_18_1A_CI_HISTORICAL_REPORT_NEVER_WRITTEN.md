# Stage 21.18.1a-ci - Historical report write elimination

Canonical V2 CI no longer opens the committed Stage 21.16.2 anti-overlay report for writing. The direct-code ownership verifier writes its generated report only to a `TemporaryDirectory`; the CI restoration wrapper was removed. Automated acceptance proves identical SHA-256, size, `mtime_ns`, and file metadata before and after both focused tests and canonical CI.

Manual game check: `NOT_REQUIRED`.
