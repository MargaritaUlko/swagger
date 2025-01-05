from datetime import timedelta, datetime
from typing import Optional

import pytz
from pydantic import validator, root_validator
from pytz import timezone
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime, select, event, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

statuses = {0: "processing", 1: "completed"}


LOCAL_TIMEZONE = timezone("Asia/Krasnoyarsk")


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))


    cars = relationship("Car", back_populates="brand")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    
    model = Column(String(100))

    # Связь с моделью Brand
    brand = relationship("Brand", back_populates="cars")
    customer_cars = relationship("Customer_Car", back_populates="car")
#
# class Service(Base):  # Изменил Services на Service
#     __tablename__ = "services"
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     price = Column(Integer)
#     time = Column(Integer)
#
#     def to_response(self):
#         """
#                Преобразует объект Service в словарь для ответа API.
#                """
#         price_rub = self.price // 100  # Конвертируем в рубли (целое число)
#         time_min = self.time // 60  # Конвертируем в минуты (целое число)
#         return {
#             "id": self.id,
#             "name": self.name,
#             "price": {
#                 "minValue": self.price,  # Цена в копейках
#                 "maxValue": price_rub,  # Цена в рублях
#                 "format": f"{price_rub} руб."  # Форматированная строка
#             },
#             "time": {
#                 "second": self.time,  # Время в секундах
#                 "minute": time_min  # Время в минутах
#             },
#         }
class Service(Base):  # Изменил Services на Service
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Integer)
    time = Column(Integer)
    order_services = relationship("OrderService", back_populates="service")  # "service" is the forward relationship in OrderService

    def to_response(self):
        """
        Преобразует объект Service в словарь для ответа API.
        """
        # Преобразования здесь
        price_rub = self.convert_price(self.price)  # Конвертируем в рубли
        time_min = self.convert_time(self.time)  # Конвертируем в минуты
        return {
            "id": self.id,
            "name": self.name,
            "price": {
                "minValue": self.price,  # Цена в копейках
                "maxValue": price_rub,  # Цена в рублях
                "format": f"{price_rub} руб."  # Форматированная строка
            },
            "time": {
                "second": self.time,  # Время в секундах
                "minute": time_min  # Время в минутах
            },
        }

    def convert_price(self, price):
        return price // 100  # Конвертация цены

    def convert_time(self, time):
        return time // 60  # Конвертация времени

class OrderService(Base):
    __tablename__ = "order_service"
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey("services.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    service = relationship("Service", back_populates="order_services")  # "order_services" is the reverse relationship in Service

    # Optionally, define the relationship to the Order model (if needed)
    order = relationship("Order", back_populates="order_services")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    administrator_id = Column(Integer, ForeignKey("user.id"))
    customer_car_id = Column(Integer, ForeignKey("customer_cars.id"))
    employee_id = Column(Integer, ForeignKey("user.id"))
    status = Column(Integer)
    start_date = Column(DateTime(timezone=True))  # Включаем временную зону
    end_date = Column(DateTime(timezone=True))
    notified: Mapped[bool] = mapped_column(Boolean, default=False)
    order_services = relationship("OrderService", back_populates="order")  # "order" is the forward relationship in OrderService


    @validator("status")
    def validate_status(cls, value):
        if value not in statuses.values():
            raise ValueError("Invalid status. Allowed values are 0 (processing) or 1 (completed).")
        return value

    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date < start_date:
            raise ValueError("End date must be after start date.")
        return end_date


class Customer_Car(Base):
    __tablename__ = "customer_cars"
    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    customer_id = Column(Integer, ForeignKey("user.id"))
    year = Column(Integer)
    number = Column(String(100))
    # Связь с Car
    car = relationship("Car", back_populates="customer_cars")

    # Связь с User
    customer = relationship("User", back_populates="customer_cars")