from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Session, relationship
from datetime import datetime
import json
from typing import Optional, Any, Dict

from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer)
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    ip_address = Column(String)
    user_agent = Column(String)

    # Relationship
    user = relationship("User", back_populates="audit_logs")

async def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: Optional[int] = None,
    old_data: Optional[Dict[str, Any]] = None,
    new_data: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLog:
    """
    Create an immutable audit log entry for any system change.
    Compliant with 21 CFR Part 11 requirements for audit trails.
    
    Args:
        db: Database session
        user_id: ID of the user performing the action
        action: Type of action performed (CREATE, UPDATE, DELETE, etc.)
        entity_type: Type of entity being modified (CAPA, Document, etc.)
        entity_id: ID of the entity being modified
        old_data: Previous state of the entity (for updates/deletes)
        new_data: New state of the entity (for creates/updates)
        ip_address: IP address of the user
        user_agent: User agent string from the request
    
    Returns:
        AuditLog: The created audit log entry
    """
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_data=old_data,
        new_data=new_data,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.add(audit_log)
    await db.commit()
    await db.refresh(audit_log)
    
    return audit_log

def get_audit_trail(
    db: Session,
    entity_type: Optional[str] = None,
    entity_id: Optional[int] = None,
    user_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
) -> list[AuditLog]:
    """
    Retrieve audit trail entries with optional filtering.
    
    Returns:
        List[AuditLog]: List of audit log entries matching the criteria
    """
    query = db.query(AuditLog)
    
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLog.entity_id == entity_id)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
        
    return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all() 