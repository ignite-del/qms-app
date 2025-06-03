from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, UserRole
from app.schemas.capa import CAPACreate, CAPAUpdate, CAPAResponse, CAPAWithDetails
from app.services.capa import CAPAService
from app.utils.audit import create_audit_log
from app.utils.auth import check_permission

router = APIRouter()

@router.post("/", response_model=CAPAResponse, status_code=status.HTTP_201_CREATED)
async def create_capa(
    capa: CAPACreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has permission to create CAPA
    check_permission(current_user, [UserRole.ADMIN, UserRole.QA])
    
    capa_service = CAPAService(db)
    new_capa = capa_service.create_capa(capa, current_user.id)
    
    # Create audit log
    await create_audit_log(
        db,
        user_id=current_user.id,
        action="CREATE_CAPA",
        entity_type="CAPA",
        entity_id=new_capa.id,
        new_data=capa.dict()
    )
    
    return new_capa

@router.get("/", response_model=List[CAPAResponse])
async def list_capas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    capa_service = CAPAService(db)
    return capa_service.get_capas(skip=skip, limit=limit)

@router.get("/{capa_id}", response_model=CAPAWithDetails)
async def get_capa(
    capa_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    capa_service = CAPAService(db)
    capa = capa_service.get_capa(capa_id)
    if not capa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAPA not found"
        )
    return capa

@router.put("/{capa_id}", response_model=CAPAResponse)
async def update_capa(
    capa_id: int,
    capa_update: CAPAUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has permission to update CAPA
    check_permission(current_user, [UserRole.ADMIN, UserRole.QA])
    
    capa_service = CAPAService(db)
    old_capa = capa_service.get_capa(capa_id)
    if not old_capa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAPA not found"
        )
    
    updated_capa = capa_service.update_capa(capa_id, capa_update)
    
    # Create audit log
    await create_audit_log(
        db,
        user_id=current_user.id,
        action="UPDATE_CAPA",
        entity_type="CAPA",
        entity_id=capa_id,
        old_data=old_capa.dict(),
        new_data=updated_capa.dict()
    )
    
    return updated_capa

@router.delete("/{capa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_capa(
    capa_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only admins can delete CAPAs
    check_permission(current_user, [UserRole.ADMIN])
    
    capa_service = CAPAService(db)
    capa = capa_service.get_capa(capa_id)
    if not capa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="CAPA not found"
        )
    
    # Create audit log before deletion
    await create_audit_log(
        db,
        user_id=current_user.id,
        action="DELETE_CAPA",
        entity_type="CAPA",
        entity_id=capa_id,
        old_data=capa.dict()
    )
    
    capa_service.delete_capa(capa_id) 