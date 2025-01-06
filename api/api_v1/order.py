from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user
import asyncio
from core.authentication.dependecy import check_access, check_order_list_access, check_order_by_id
from core.config import settings
from core.models import db_helper, Order, User
from core.schemas.carwash import OrderCreate, OrderRead, OrderUpdate
from crud.carwash import order as order_crud
from crud.carwash.order import get_orders

order_router = APIRouter(
    prefix=settings.api.v1.orders,
    tags=["Orders"],
)
# Инъекции зависимостей

# Customer_car - в ней поиск по моделям машины

@order_router.get("/orders", response_model=List[OrderRead])
async def api_get_orders(
    session: AsyncSession = Depends(db_helper.session_getter),
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1),
    sort_by: Optional[str] = Query("id", regex="^(id|start_date)$"),
    order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    status: Optional[int] = Query(None, ge=0, le=1),
    orders: List[Order] = Depends(check_order_list_access())
):
    orders = await get_orders(
        session,
        limit=limit,
        page=page,
        sort_by=sort_by,
        order=order,
        status=status,
    )

    # Асинхронная обработка
    serialized_orders = [await OrderRead.from_orm(order) for order in orders]

    return serialized_orders


# Получение информации о заказе по id
# @order_router.get("/{order_id}", response_model=OrderRead)
# async def get_order(
#     order_id: int,
#     session: AsyncSession = Depends(db_helper.session_getter),
#     # user: User = Depends(check_access([1]))
# ):
#     order = await order_crud.get_order(session=session, order_id=order_id)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order
@order_router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    order: Order = Depends(check_order_by_id),


):
    return order


@order_router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_create: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(check_access([1]))

):
    order = await order_crud.create_order(session=session, order_create=order_create)
    return order

@order_router.put("/{order_id}", response_model=OrderRead)
async def update_order(
    order_update: OrderUpdate,
    order_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(check_access([1]))
):
    order = await order_crud.update_order(
        session=session, order_id=order_id, order_update=order_update
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to view this order")
# Удаление заказа
@order_router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(check_access([1]))
):
    deleted = await order_crud.delete_order(session=session, order_id=order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}
