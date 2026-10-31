"""Canonical inventory aggregate and pure membership/capacity invariants."""
from __future__ import annotations
from dataclasses import dataclass
from rom_v2.domain.item import ItemInstance

@dataclass(frozen=True,slots=True)
class InventoryAdditionPlan:
    """Pure plan for filling existing stacks and allocating new item instances."""
    stack_updates:tuple[tuple[ItemInstance,int],...]
    new_stack_quantities:tuple[int,...]

@dataclass(frozen=True,slots=True)
class InventoryAggregate:
    """Own inventory membership and capacity invariants, never persistence or UI."""
    owner_user_id:int
    capacity:int
    instances:tuple[ItemInstance,...]=()
    def __post_init__(self)->None:
        if self.owner_user_id<=0:raise ValueError("inventory_owner_invalid")
        if self.capacity<=0:raise ValueError("inventory_capacity_invalid")
        identities=[item.inventory_id for item in self.instances]
        if len(identities)!=len(set(identities)):raise ValueError("inventory_identity_duplicate")
        if any(item.owner_user_id!=self.owner_user_id for item in self.instances):raise ValueError("inventory_foreign_instance")
        if len(self.instances)>self.capacity:raise ValueError("inventory_capacity_exceeded")
    def require_instance(self,inventory_id:int)->ItemInstance:
        if inventory_id<=0:raise ValueError("inventory_identity_invalid")
        for item in self.instances:
            if item.inventory_id==inventory_id:return item
        raise LookupError("inventory_instance_not_found")
    def plan_addition(self,item_id:int,quantity:int,max_stack:int)->InventoryAdditionPlan:
        if min(item_id,quantity,max_stack)<=0:raise ValueError("inventory_addition_invalid")
        same=sorted((x for x in self.instances if x.item_id==item_id and x.quantity<max_stack),key=lambda x:x.inventory_id)
        left=quantity;updates=[]
        for item in same:
            transfer=min(left,max_stack-item.quantity)
            if transfer:updates.append((item,item.quantity+transfer));left-=transfer
            if not left:break
        new=[]
        while left:new.append(min(left,max_stack));left-=new[-1]
        if len(self.instances)+len(new)>self.capacity:raise OverflowError("inventory_capacity_exceeded")
        return InventoryAdditionPlan(tuple(updates),tuple(new))
