from http.client import HTTPException
from typing import Optional, List, Callable, Awaitable

from fastapi import Depends
from sqlalchemy import select, Sequence
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from core.authentication.dependecy import check_order_list_access
from core.models import Order, OrderService, Customer_Car, User
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
async def get_orders(
    session: AsyncSession,
    limit: int = 10,
    page: int = 1,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc",
    status: Optional[int] = None,
    orders: List[Order] = Depends(check_order_list_access)  # Здесь зависимость
) -> List[Order]:
    # Теперь orders уже является списком заказов
    if not orders:
        return []  # Возвращаем пустой список, если заказов нет

    accessible_order_ids = [order.id for order in orders]

    # Основной запрос с прогрузкой связанных объектов
    query = (
        select(Order)
        .filter(Order.id.in_(accessible_order_ids))  # Фильтрация доступных заказов
        .options(
            joinedload(Order.employee),
            joinedload(Order.administrator),
            joinedload(Order.customer_car).joinedload(Customer_Car.car),
            joinedload(Order.order_services).joinedload(OrderService.service),
        )
    )

    # Фильтрация по статусу заказа
    if status is not None:
        query = query.filter(Order.status == status)

    # Пагинация
    query = query.offset((page - 1) * limit).limit(limit)

    try:
        result = await session.execute(query)
    except InvalidRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Извлекаем заказы
    orders = result.unique().scalars().all()

    # Сортировка
    if sort_by:
        if not hasattr(Order, sort_by):
            raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")
        reverse = order == "desc"
        orders = sorted(orders, key=lambda order: getattr(order, sort_by), reverse=reverse)

    return orders


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



#
# async def get_orders(
#     session: AsyncSession,
#     limit: int = 10,
#     page: int = 1,
#     sort_by: Optional[str] = "id",
#     order: Optional[str] = "asc",
#     status: Optional[int] = None
# ) -> List[Order]:
#     query = select(Order).options(
#         joinedload(Order.employee),
#         joinedload(Order.administrator),
#         joinedload(Order.customer_car).joinedload(Customer_Car.car),
#         joinedload(Order.order_services).joinedload(OrderService.service),
#     )
#
#     # Apply filter based on order status
#     if status is not None:
#         query = query.filter(Order.status == status)
#
#     # Apply pagination: offset based on page and limit
#     query = query.offset((page - 1) * limit).limit(limit)
#
#     # Execute query and get the results
#     try:
#         result = await session.execute(query)
#     except InvalidRequestError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#
#     # Extract all the orders from the result
#     orders = result.unique().scalars().all()
#
#     # Sort orders for the entire collection
#     if sort_by:
#         # Validate sort_by field exists
#         if not hasattr(Order, sort_by):
#             raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")
#
#         # Sort data for the entire collection
#         reverse = order == "desc"
#         orders = sorted(orders, key=lambda order: getattr(order, sort_by), reverse=reverse)
#
#     return orders
async def delete_order(session: AsyncSession, order_id: int) -> Order:
    stmt = select(Order).filter(Order.id == order_id)
    result = await session.execute(stmt)
    order = result.scalars().first()
    if not order:
        raise ValueError("Order not found")

    await session.delete(order)
    await session.commit()
    return order



