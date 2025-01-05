from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Brand
from core.schemas.carwash import BrandCreate, BrandUpdate


async def create_brand(session: AsyncSession, brand_create: BrandCreate) -> Brand:
    brand = Brand(**brand_create.dict())
    session.add(brand)
    await session.commit()
    await session.refresh(brand)
    return brand

async def get_brand(session: AsyncSession, brand_id: int) -> Brand:
    stmt = select(Brand).filter(Brand.id == brand_id)
    result = await session.execute(stmt)
    brand = result.scalars().first()
    if not brand:
        raise ValueError("Brand not found")
    return brand

async def get_brands(session: AsyncSession) -> Sequence[Brand]:
    stmt = select(Brand)
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_brand(session: AsyncSession, brand_id: int, brand_update: BrandUpdate) -> Brand:
    stmt = select(Brand).filter(Brand.id == brand_id)
    result = await session.execute(stmt)
    brand = result.scalars().first()
    if not brand:
        raise ValueError("Brand not found")

    for key, value in brand_update.dict(exclude_unset=True).items():
        setattr(brand, key, value)

    await session.commit()
    await session.refresh(brand)
    return brand

async def delete_brand(session: AsyncSession, brand_id: int) -> Brand:
    stmt = select(Brand).filter(Brand.id == brand_id)
    result = await session.execute(stmt)
    brand = result.scalars().first()
    if not brand:
        raise ValueError("Brand not found")

    await session.delete(brand)
    await session.commit()
    return brand