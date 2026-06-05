from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MaterialBase(BaseModel):
    material_type: str
    definition: Optional[str] = None
    simple_rules: List[str] = Field(default_factory=list)
    detailed_config: Optional[Dict[str, Any]] = None


class MaterialCreate(MaterialBase):
    pass


class MaterialResponse(MaterialBase):
    id: int
    policy_id: int

    class Config:
        from_attributes = True


class PolicyBase(BaseModel):
    airline_code: str
    airline_name: str
    ticket_desk_type: str = "all"
    raw_policy: Optional[str] = None
    breakdown_json: Optional[Dict[str, Any]] = None


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    airline_name: Optional[str] = None
    ticket_desk_type: Optional[str] = None
    raw_policy: Optional[str] = None
    breakdown_json: Optional[Dict[str, Any]] = None


class PolicyResponse(PolicyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    current_version_id: Optional[int] = None
    materials: List[MaterialResponse] = []

    class Config:
        from_attributes = True


class VersionBase(BaseModel):
    changes_summary: Optional[str] = None
    changes_detail: Optional[Dict[str, Any]] = None
    operator: str
    operation_type: str = "update"


class VersionCreate(VersionBase):
    policy_snapshot: Optional[Dict[str, Any]] = None


class VersionResponse(VersionBase):
    id: int
    version_number: int
    version_tag: str
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogBase(BaseModel):
    action: str
    operator: str
    details: Optional[Dict[str, Any]] = None


class AuditLogResponse(AuditLogBase):
    id: int
    policy_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PolicySearchFilter(BaseModel):
    airline_code: Optional[str] = None
    ticket_desk_type: Optional[str] = None
    limit: int = 100
    offset: int = 0
