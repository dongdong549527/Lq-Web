from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.db import get_db
from app.models import Depot
from app.schemas import DepotCreate, DepotResponse

router = APIRouter()

@router.get("/", response_model=List[DepotResponse])
async def read_depots(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Depot).offset(skip).limit(limit))
    depots = result.scalars().all()
    return depots

@router.post("/", response_model=DepotResponse)
async def create_depot(depot: DepotCreate, db: AsyncSession = Depends(get_db)):
    db_depot = Depot(**depot.dict())
    db.add(db_depot)
    await db.commit()
    await db.refresh(db_depot)
    return db_depot

@router.get("/{depot_id}", response_model=DepotResponse)
async def read_depot(depot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Depot).where(Depot.id == depot_id))
    depot = result.scalars().first()
    if depot is None:
        raise HTTPException(status_code=404, detail="Depot not found")
    return depot

@router.put("/{depot_id}", response_model=DepotResponse)
async def update_depot(depot_id: int, depot_in: DepotCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Depot).where(Depot.id == depot_id))
    depot = result.scalars().first()
    if depot is None:
        raise HTTPException(status_code=404, detail="Depot not found")
    
    depot.name = depot_in.name
    depot.address = depot_in.address
    depot.contact_person = depot_in.contact_person
    depot.phone = depot_in.phone
    depot.province = depot_in.province
    
    await db.commit()
    await db.refresh(depot)
    return depot

@router.delete("/{depot_id}")
async def delete_depot(depot_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Depot).where(Depot.id == depot_id))
    depot = result.scalars().first()
    if depot is None:
        raise HTTPException(status_code=404, detail="Depot not found")
    
    await db.delete(depot)
    await db.commit()
    return {"ok": True}
