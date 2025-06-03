from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.capa import CAPAStatus, CAPAType

class CAPABase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    capa_type: CAPAType
    root_cause: Optional[str] = None
    immediate_action: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    due_date: Optional[datetime] = None

class CAPACreate(CAPABase):
    assignee_id: int

class CAPAUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = None
    status: Optional[CAPAStatus] = None
    root_cause: Optional[str] = None
    immediate_action: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

class CAPAResponse(CAPABase):
    id: int
    status: CAPAStatus
    created_at: datetime
    updated_at: datetime
    closed_date: Optional[datetime] = None
    assignee_id: int

    class Config:
        from_attributes = True

class CAPAWithDetails(CAPAResponse):
    assignee: "UserResponse"
    signatures: List["ElectronicSignatureResponse"] = []
    attachments: List["DocumentResponse"] = []

    class Config:
        from_attributes = True 