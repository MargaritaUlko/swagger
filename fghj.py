import asyncio
from datetime import datetime
import pytz
from sqlalchemy import select
from sqlalchemy.sql import func
from core.models import Order, db_helper


async def test_query():
    async for session in db_helper.session_getter():
        krasnoyarsk_tz = pytz.timezone("Asia/Krasnoyarsk")
        now = datetime.now(krasnoyarsk_tz)
        print(f"Текущее время Красноярска: {now}")

        # Выполнение запроса
        result = await session.execute(
            select(Order).filter(
                func.timezone("Asia/Krasnoyarsk", Order.end_date) < now,
                Order.status == 1
            )
        )

        # Извлечение данных
        orders = result.scalars().all()
        print(f"Найдено заказов: {len(orders)}")
        for order in orders:
            print(f"Заказ ID: {order.id}, Статус: {order.status}, Дата окончания: {order.end_date}")

        # Закрываем сессию
        await session.close()


# Запуск теста
if __name__ == "__main__":
    test_query()
