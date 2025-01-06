# CRUD Operations for OrderService
from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from sqlalchemy.orm import joinedload

from core.models import OrderService, Order, Service
from core.schemas.carwash import OrderServiceCreate, OrderServiceUpdate
import pytz
logger = logging.getLogger(__name__)



from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import OrderService, Order, Service
from core.schemas.carwash import OrderServiceCreate
import pytz
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


LOCAL_TIMEZONE = pytz.timezone("Asia/Krasnoyarsk")  # Замените на ваш часовой пояс, если он другой

# async def create_order_service(session: AsyncSession, order_service_create: OrderServiceCreate) -> OrderService:
#     # Step 1: Extract order by order_id
#     stmt_order = select(Order).filter(Order.id == order_service_create.order_id)
#     result_order = await session.execute(stmt_order)
#     order = result_order.scalars().first()
#
#     if not order:
#         logger.error(f"Order with id {order_service_create.order_id} not found.")
#         raise HTTPException(status_code=404, detail="Order not found")
#
#     # Step 2: Extract service by service_id
#     stmt_service = select(Service).filter(Service.id == order_service_create.service_id)
#     result_service = await session.execute(stmt_service)
#     service = result_service.scalars().first()
#
#     if not service:
#         logger.error(f"Service with id {order_service_create.service_id} not found.")
#         raise HTTPException(status_code=404, detail="Service not found")
#
#     # Step 3: Check if the order is in progress (status != 0)
#     if order.status == 0:
#         # Check if the order already has services
#         stmt_existing_order_service = select(OrderService).filter(OrderService.order_id == order_service_create.order_id)
#         result_existing_order_service = await session.execute(stmt_existing_order_service)
#         existing_order_service = result_existing_order_service.scalars().first()
#
#         if existing_order_service:
#             logger.error(f"Cannot add service to order with status 0. Order ID: {order_service_create.order_id}")
#             raise HTTPException(status_code=400, detail="Cannot add service to order with status 0")
#         else:
#             logger.info(f"Order with ID {order_service_create.order_id} has no services yet. Proceeding to add new service.")
#
#     # Step 4: Check if the service already exists in the order
#     stmt_existing_service = select(OrderService).filter(
#         OrderService.order_id == order_service_create.order_id,
#         OrderService.service_id == order_service_create.service_id
#     )
#     result_existing_service = await session.execute(stmt_existing_service)
#     existing_service = result_existing_service.scalars().first()
#
#     if existing_service:
#         service_name = existing_service.service.name
#         logger.error(f"Service '{service_name}' already exists in this order.")
#         raise HTTPException(status_code=400, detail=f"This service '{service_name}' already exists in the order.")
#
#     # Step 5: Create the new OrderService
#     order_service = OrderService(**order_service_create.dict())
#     session.add(order_service)
#
#     # Step 6: Update the order's end_date based on the service's time
#     if order.end_date:
#         order.end_date += timedelta(seconds=service.time)
#         logger.info(f"Order end_date updated to {order.end_date} after adding service.")
#     else:
#         order.end_date = order.start_date + timedelta(seconds=service.time)
#         logger.info(f"Order end_date set to {order.end_date} after adding service.")
#
#     # Step 7: Commit the changes to the session
#     session.add(order)
#
#     # Step 8: Perform the commit and refresh the order and order_service objects
#     await session.commit()
#
#     # Refresh the objects after commit to get the latest data
#     await session.refresh(order)
#     await session.refresh(order_service)
#
#     logger.info(f"Order with ID {order_service_create.order_id} updated successfully.")
#     logger.info(f"New order_service created with ID {order_service.id}.")
#
#     return order_service

KRASNOYARSK_TZ = pytz.timezone("Asia/Krasnoyarsk")  # Часовой пояс Красноярска

async def create_order_service(session: AsyncSession, order_service_create: OrderServiceCreate):
    # Step 1: Extract order by order_id
    stmt_order = select(Order).filter(Order.id == order_service_create.order_id)
    result_order = await session.execute(stmt_order)
    order = result_order.scalars().first()

    if not order:
        return {"error": "order_not_found", "message": "Order not found"}

    # Step 2: Extract service by service_id
    stmt_service = select(Service).filter(Service.id == order_service_create.service_id)
    result_service = await session.execute(stmt_service)
    service = result_service.scalars().first()

    if not service:
        return {"error": "service_not_found", "message": "Service not found"}

    # Step 3: Check if the order is in progress (status != 0)
    if order.status == 0:
        stmt_existing_order_service = select(OrderService).filter(OrderService.order_id == order_service_create.order_id)
        result_existing_order_service = await session.execute(stmt_existing_order_service)
        existing_order_service = result_existing_order_service.scalars().first()

        if existing_order_service:
            return {
                "error": "invalid_order_status",
                "message": "Cannot add service to order with status 0"
            }

    # Step 4: Check if the service already exists in the order
    stmt_existing_service = select(OrderService).filter(
        OrderService.order_id == order_service_create.order_id,
        OrderService.service_id == order_service_create.service_id
    )
    result_existing_service = await session.execute(stmt_existing_service)
    existing_service = result_existing_service.scalars().first()

    if existing_service:
        return {
            "error": "duplicate_service",
            "message": f"Service '{existing_service.service.name}' already exists in the order"
        }

    # Step 5: Create the new OrderService
    order_service = OrderService(**order_service_create.dict())
    session.add(order_service)

    # Step 6: Update the order's end_date based on the service's time
    if order.end_date:
        order.end_date += timedelta(seconds=service.time)
    else:
        order.end_date = order.start_date + timedelta(seconds=service.time)

    session.add(order)

    # Step 7: Commit the changes to the session
    await session.commit()

    # Refresh the objects after commit to get the latest data
    await session.refresh(order)
    await session.refresh(order_service)

    return {"success": True, "data": order_service}
async def get_order_service(session: AsyncSession, order_service_id: int) -> OrderService:
    stmt = select(OrderService).filter(OrderService.id == order_service_id)
    result = await session.execute(stmt)
    order_service = result.scalars().first()
    if not order_service:
        raise ValueError("OrderService not found")
    return order_service

async def get_order_services(
    session: AsyncSession,
    orders: list[OrderService],  # Фильтрованные заказы пользователя
    order_id: Optional[int] = None,
    sort_by: Optional[str] = "id",
    order: Optional[str] = "asc"
) -> Sequence[OrderService]:
    order_services = orders

    # Фильтрация по order_id (если передан параметр)
    if order_id is not None:
        order_services = [service for service in order_services if service.order_id == order_id]

    # Сортировка для всей коллекции
    if sort_by:
        # Проверка, что сортировка происходит по существующему полю
        if not hasattr(OrderService, sort_by):
            raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")

        # Сортируем данные для всей коллекции
        reverse = order == "desc"
        order_services = sorted(order_services, key=lambda service: getattr(service, sort_by), reverse=reverse)

    return order_services

async def update_order_service(session: AsyncSession, order_service_id: int, order_service_update: OrderServiceUpdate) -> OrderService:
    stmt = select(OrderService).filter(OrderService.id == order_service_id)
    result = await session.execute(stmt)
    order_service = result.scalars().first()
    if not order_service:
        raise ValueError("OrderService not found")

    for key, value in order_service_update.dict(exclude_unset=True).items():
        setattr(order_service, key, value)

    await session.commit()
    await session.refresh(order_service)
    return order_service

async def delete_order_service(session: AsyncSession, order_service_id: int) -> OrderService:
    stmt = select(OrderService).filter(OrderService.id == order_service_id)
    result = await session.execute(stmt)
    order_service = result.scalars().first()
    if not order_service:
        raise ValueError("OrderService not found")

    await session.delete(order_service)
    await session.commit()
    return order_service

