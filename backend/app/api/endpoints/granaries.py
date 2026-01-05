from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.db import get_db
from app.models import Granary, GranaryConfig
from app.schemas import GranaryCreate, GranaryResponse, GranaryConfigCreate

router = APIRouter()

@router.get("/", response_model=List[GranaryResponse])
async def read_granaries(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Load config eagerly
    result = await db.execute(select(Granary).options(selectinload(Granary.config)).offset(skip).limit(limit))
    granaries = result.scalars().all()
    return granaries

@router.post("/", response_model=GranaryResponse)
async def create_granary(granary_in: GranaryCreate, db: AsyncSession = Depends(get_db)):
    # Extract config data
    config_data = granary_in.config
    granary_data = granary_in.dict(exclude={"config"})
    
    db_granary = Granary(**granary_data)
    db.add(db_granary)
    await db.commit()
    await db.refresh(db_granary)
    
    if config_data:
        db_config = GranaryConfig(granary_id=db_granary.id, **config_data.dict())
        db.add(db_config)
        await db.commit()
        await db.refresh(db_granary) # Refresh to load config relation
    
    # Reload with config
    result = await db.execute(select(Granary).options(selectinload(Granary.config)).where(Granary.id == db_granary.id))
    db_granary = result.scalars().first()
    return db_granary

@router.get("/{granary_id}", response_model=GranaryResponse)
async def read_granary(granary_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Granary).options(selectinload(Granary.config)).where(Granary.id == granary_id))
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
