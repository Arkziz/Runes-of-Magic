# Stage 21.17.3c - Registration class catalog parity

The duplicate `CLASS_LABELS` presentation catalog was removed. Registration buttons, validation, and creation results now consume `DEFAULT_CLASS_CATALOG`, the same canonical owner used by the profile flow. Stable class keys and persisted data are unchanged. A HEAD-wide AST guard found zero parallel six-class string catalogs after the refactor.
