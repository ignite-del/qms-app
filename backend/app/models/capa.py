from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base

class CAPAStatus(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    CLOSED = "closed"

class CAPAType(str, enum.Enum):
    CORRECTIVE = "corrective"
    PREVENTIVE = "preventive"

class CAPA(Base):
    __tablename__ = "capas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    capa_type = Column(SQLEnum(CAPAType), nullable=False)
    status = Column(SQLEnum(CAPAStatus), nullable=False, default=CAPAStatus.DRAFT)
    root_cause = Column(Text)
    immediate_action = Column(Text)
    corrective_action = Column(Text)
    preventive_action = Column(Text)
    
    # Tracking fields
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime)
    closed_date = Column(DateTime)
    
    # Relations
    assignee_id = Column(Integer, ForeignKey("users.id"))
    assignee = relationship("User", back_populates="capas")
    signatures = relationship("ElectronicSignature", back_populates="capa")
    attachments = relationship("Document", back_populates="capa")
    
    def __repr__(self):
        return f"<CAPA {self.id}: {self.title}>" 