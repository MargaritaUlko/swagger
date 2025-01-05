from fastapi import Depends, HTTPException, status
from typing import List, Callable, Awaitable
import logging

from sqlalchemy import select, or_, and_
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api.api_v1.fastapi_users import fastapi_users
from core.models import User, Order, db_helper, Customer_Car, OrderService  # или корректный путь к модели
# Зависимость для получения текущего пользователя

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def check_access(allowed_roles: List[int]):
    async def dependency(user: User = Depends(fastapi_users.current_user())):
        role = user.role_id
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this resource"
            )
        return user
    return dependency



def check_order_list_access() -> Callable[..., Awaitable[list[Order]]]:
    async def dependency(
        session: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(fastapi_users.current_user()),
    ):
        logger.info(f"User ID: {user.id}")

        query = select(Order).filter(
            or_(
                Order.employee_id == user.id,
                Order.administrator_id == user.id,
                Order.customer_car_id.in_(
                    select(Customer_Car.id).filter(Customer_Car.customer_id == user.id)
                ),
            )
        )
        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        logger.info(f"Compiled SQL Query: {compiled_query}")

        result = await session.execute(query)
        orders = result.scalars().all()

        for order in orders:
            logger.info(
                f"Order id {order.id}: employee_id={order.employee_id}, "
                f"administrator_id={order.administrator_id}, customer_car_id={order.customer_car_id}"
            )

        return orders

    return dependency


def check_order_list_access22() -> Callable[..., Awaitable[list[OrderService]]]:
    async def dependency(
        session: AsyncSession = Depends(db_helper.session_getter),
        user: User = Depends(fastapi_users.current_user()),
    ):
        logger.info(f"User ID: {user.id}")

        # Создаем запрос с фильтрацией
        query = select(OrderService).join(Order).options(
            joinedload(OrderService.order)  # Подгружаем связанный заказ
        ).filter(
            or_(
                Order.employee_id == user.id,  # Если пользователь является сотрудником
                Order.administrator_id == user.id,  # Если пользователь является администратором
                Order.customer_car_id.in_(
                    select(Customer_Car.id).filter(Customer_Car.customer_id == user.id)
                ),  # Если у пользователя есть машина в заказе
            )
        )

        # Скомпилируем запрос, чтобы убедиться, что фильтрация применяется
        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        logger.info(f"Compiled SQL Query: {compiled_query}")

        async with session:
            result = await session.execute(query)  # Выполняем запрос с фильтрацией
            order_services = result.scalars().all()  # Получаем все отфильтрованные записи

        # Логируем информацию о найденных записях
        for order_service in order_services:
            logger.info(
                f"OrderService id {order_service.id}: order_id={order_service.order.id}, "
                f"employee_id={order_service.order.employee_id}, "
                f"administrator_id={order_service.order.administrator_id}, "
                f"customer_car_id={order_service.order.customer_car_id}"
            )

        return order_services

    return dependency


async def check_order_by_id(
    order_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    user: User = Depends(fastapi_users.current_user())
) -> Order:
    query = select(Order).where(
        Order.id == order_id,
        or_(Order.employee_id == user.id,
        Order.administrator_id == user.id)
    )
    result = await session.execute(query)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this order"
        )
    return order
