from sqlalchemy import select, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Order
from core.schemas.carwash import OrderCreate, OrderUpdate


# CRUD Operations for Order
async def create_order(session: AsyncSession, order_create: OrderCreate) -> Order:
    order = Order(**order_create.dict())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order

async def get_order(session: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).filter(Order.id == order_id)
    result = await session.execute(stmt)
    order = result.scalars().first()
    if not order:
        raise ValueError("Order not found")
    return order

async def get_orders(session: AsyncSession) -> Sequence[Order]:
    stmt = select(Order)
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_order(session: AsyncSession, order_id: int, order_update: OrderUpdate) -> Order:
    stmt = select(Order).filter(Order.id == order_id)
    result = await session.execute(stmt)
    order = result.scalars().first()
    if not order:
        raise ValueError("Order not found")

    for key, value in order_update.dict(exclude_unset=True).items():
        setattr(order, key, value)

    await session.commit()
    await session.refresh(order)
    return order

async def delete_order(session: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).filter(Order.id == order_id)
    result = await session.execute(stmt)
    order = result.scalars().first()
    if not order:
        raise ValueError("Order not found")

    await session.delete(order)
    await session.commit()
    return order



