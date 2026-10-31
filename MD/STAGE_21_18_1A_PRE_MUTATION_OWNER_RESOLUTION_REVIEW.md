# Stage 21.18.1a pre-mutation owner-resolution review

## Status

`PASS_READ_ONLY` / `GO_TO_21_18_1A_IMPLEMENTATION_WITH_NARROW_INVENTORY_DOMAIN_OWNER`

## V1 effective-path resolution

The review records top-level definition order, effective final module bindings, imports, core calls and handler-registration evidence for the inventory/equipment runtime path. Earlier same-name top-level definitions are classified as `SUPERSEDED_IN_MODULE`; the final binding is `EFFECTIVE`. This classification is evidence for parity only and is not copied into V2.

## Canonical V2 ownership

- item definition and instance identity: `rom_v2/domain/item.py`;
- inventory aggregate and membership/capacity invariants: new narrow `rom_v2/domain/inventory.py`;
- equipment compatibility and slot policy: `rom_v2/domain/equipment.py`;
- inventory queries/mutations: `rom_v2/application/inventory_service.py`;
- equip/unequip orchestration: `rom_v2/application/equipment_service.py`;
- ports, repositories and UoW remain in their existing canonical modules;
- Telegram inventory UI is deferred to `21.18.1b`.

## inventory.py decision

Creating `rom_v2/domain/inventory.py` is approved only as the single owner of inventory aggregate/value invariants that do not already exist elsewhere. The file must not redefine Item, equipment compatibility, repositories, SQL, UoW, sorting, pagination, localization, callbacks or equip/unequip orchestration.

## Duplicate prevention gate

Before every new public symbol is written, the implementation patch must scan all production `rom_v2` modules for the same name and semantic responsibility. Existing owners are reused by import. Duplicate definitions fail the patch and trigger rollback.

## 21.18.1a mutation boundary

The machine report contains the exact candidate file allowlist and required integration tests. A migration may be added only if a concrete schema gap is proven. No Telegram presentation mutation is allowed in `21.18.1a`.

## Manual game check

`NOT_REQUIRED`: this review is read-only.
