from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

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

# Получение списка всех заказов


@order_router.get("", response_model=list[OrderRead])
async def api_get_orders(
        limit: int = Query(10, ge=1),
        page: int = Query(1, ge=1),
        sort_by: Optional[str] = Query("id", regex="^(id|start_date)$"),
        order: Optional[str] = Query("asc", regex="^(asc|desc)$"),
        status: Optional[int] = Query(None, ge=0, le=1),
        orders: list[Order] = Depends(check_order_list_access()),
):

    if status is not None:
        orders = [order for order in orders if order.status == status]


    if sort_by:

        if not hasattr(Order, sort_by):
            raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")


        reverse = order == "desc"
        orders = sorted(orders, key=lambda order: getattr(order, sort_by), reverse=reverse)


    offset = (page - 1) * limit
    orders_paginated = orders[offset:offset + limit]

    return orders_paginated


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
