from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.db import get_db
from app.models import Granary, GranaryConfig
from app.schemas import GranaryCreate, GranaryResponse, GranaryConfigCreate

router = APIRouter()

@router.get("", response_model=List[GranaryResponse])
async def read_granaries(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Load config and info eagerly
    result = await db.execute(
        select(Granary)
        .options(selectinload(Granary.config), selectinload(Granary.info))
        .offset(skip).limit(limit)
    )
    granaries = result.scalars().all()
    return granaries

@router.post("", response_model=GranaryResponse)
async def create_granary(granary_in: GranaryCreate, db: AsyncSession = Depends(get_db)):
    # Extract nested data
    config_data = granary_in.config
    info_data = granary_in.info
    granary_data = granary_in.dict(exclude={"config", "info"})
    
    db_granary = Granary(**granary_data)
    db.add(db_granary)
    await db.commit()
    await db.refresh(db_granary)
    
    if config_data:
        db_config = GranaryConfig(granary_id=db_granary.id, **config_data.dict())
        db.add(db_config)
    
    if info_data:
        from app.models.granary import GranaryInfo
        # Ensure rough_rice_yield is not None, default to 0.0 if necessary
        info_dict = info_data.dict()
        if info_dict.get('rough_rice_yield') is None:
             info_dict['rough_rice_yield'] = 0.0
        if info_dict.get('moisture') is None:
             info_dict['moisture'] = 0.0
        
        # Ensure entry_time is None if it's empty string or invalid (handled by Pydantic mostly, but safe to check)
        # SQLAlchemy expects Python datetime object or None, not empty string
        
        db_info = GranaryInfo(granary_id=db_granary.id, **info_dict)
        db.add(db_info)
        
    await db.commit()
    
    # Reload with all relations
    result = await db.execute(
        select(Granary)
        .options(selectinload(Granary.config), selectinload(Granary.info))
        .where(Granary.id == db_granary.id)
    )
    db_granary = result.scalars().first()
    return db_granary

@router.get("/{granary_id}", response_model=GranaryResponse)
async def read_granary(granary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Granary)
        .options(selectinload(Granary.config), selectinload(Granary.info))
        .where(Granary.id == granary_id)
    )
    granary = result.scalars().first()
    if granary is None:
        raise HTTPException(status_code=404, detail="Granary not found")
    return granary

@router.delete("/{granary_id}")
async def delete_granary(granary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Granary).where(Granary.id == granary_id))
    granary = result.scalars().first()
    if granary is None:
        raise HTTPException(status_code=404, detail="Granary not found")
    
    await db.delete(granary)
    await db.commit()
    return {"ok": True}

@router.put("/{granary_id}", response_model=GranaryResponse)
async def update_granary(granary_id: int, granary_in: GranaryCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if granary exists
    result = await db.execute(
        select(Granary)
        .options(selectinload(Granary.config), selectinload(Granary.info))
        .where(Granary.id == granary_id)
    )
    db_granary = result.scalars().first()
    if db_granary is None:
        raise HTTPException(status_code=404, detail="Granary not found")
    
    # 2. Update basic fields
    db_granary.name = granary_in.name
    db_granary.depot_id = granary_in.depot_id
    
    # 3. Update or Create Config
    if granary_in.config:
        if db_granary.config:
            # Update existing config
            for key, value in granary_in.config.dict(exclude_unset=True).items():
                setattr(db_granary.config, key, value)
        else:
            # Create new config
            db_config = GranaryConfig(granary_id=granary_id, **granary_in.config.dict())
            db.add(db_config)
            
    # 4. Update or Create Info
    if granary_in.info:
        if db_granary.info:
            # Update existing info
            for key, value in granary_in.info.dict(exclude_unset=True).items():
                setattr(db_granary.info, key, value)
        else:
            # Create new info
            from app.models.granary import GranaryInfo
            info_dict = granary_in.info.dict()
            if info_dict.get('rough_rice_yield') is None:
                 info_dict['rough_rice_yield'] = 0.0
            if info_dict.get('moisture') is None:
                 info_dict['moisture'] = 0.0
            
            # Ensure entry_time is None if it's empty string or invalid (handled by Pydantic mostly, but safe to check)
            # SQLAlchemy expects Python datetime object or None, not empty string
            
            db_info = GranaryInfo(granary_id=granary_id, **info_dict)
            db.add(db_info)
            
    await db.commit()
    await db.refresh(db_granary)
    
    # Reload with all relations
    result = await db.execute(
        select(Granary)
        .options(selectinload(Granary.config), selectinload(Granary.info))
        .where(Granary.id == granary_id)
    )
    return result.scalars().first()
