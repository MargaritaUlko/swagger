# from typing import Sequence
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from sqlalchemy.orm import Session, joinedload
# from sqlalchemy.exc import NoResultFound
# from core.models.carwash import Brand, Car, Service, OrderService, Order, Customer_Car
# from core.schemas.carwash import (
#     BrandCreate, BrandUpdate,
#     CarCreate, CarUpdate,
#     ServiceCreate, ServiceUpdate,
#     OrderServiceCreate, OrderServiceUpdate,
#     OrderCreate, OrderUpdate,
#     CustomerCarCreate, CustomerCarUpdate, Price, Time
# )
#
# # CRUD Operations for Brand
# async def create_brand(session: AsyncSession, brand_create: BrandCreate) -> Brand:
#     brand = Brand(**brand_create.dict())
#     session.add(brand)
#     await session.commit()
#     await session.refresh(brand)
#     return brand
#
# async def get_brand(session: AsyncSession, brand_id: int) -> Brand:
#     stmt = select(Brand).filter(Brand.id == brand_id)
#     result = await session.execute(stmt)
#     brand = result.scalars().first()
#     if not brand:
#         raise ValueError("Brand not found")
#     return brand
#
# async def get_brands(session: AsyncSession, limit: int) -> Sequence[Brand]:
#     stmt = select(Brand).limit(limit)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
# async def update_brand(session: AsyncSession, brand_id: int, brand_update: BrandUpdate) -> Brand:
#     stmt = select(Brand).filter(Brand.id == brand_id)
#     result = await session.execute(stmt)
#     brand = result.scalars().first()
#     if not brand:
#         raise ValueError("Brand not found")
#
#     for key, value in brand_update.dict(exclude_unset=True).items():
#         setattr(brand, key, value)
#
#     await session.commit()
#     await session.refresh(brand)
#     return brand
#
# async def delete_brand(session: AsyncSession, brand_id: int) -> Brand:
#     stmt = select(Brand).filter(Brand.id == brand_id)
#     result = await session.execute(stmt)
#     brand = result.scalars().first()
#     if not brand:
#         raise ValueError("Brand not found")
#
#     await session.delete(brand)
#     await session.commit()
#     return brand
#
# # CRUD Operations for Car
#
# async def create_car(session: AsyncSession, car_create: CarCreate) -> Car:
#     # Создание новой записи
#     car = Car(**car_create.dict())
#     session.add(car)
#     await session.commit()
#     await session.refresh(car)
#
#     # Подгрузка связанного объекта brand
#     result = await session.execute(
#         select(Car)
#         .options(joinedload(Car.brand))  # Указываем подгрузку
#         .filter(Car.id == car.id)        # Фильтр по только что созданному ID
#     )
#     car_with_brand = result.scalars().first()
#
#     return car_with_brand
#
# async def get_car(session: AsyncSession, car_id: int) -> Car:
#     stmt = select(Car).filter(Car.id == car_id)
#     result = await session.execute(stmt)
#     car = result.scalars().first()
#     if not car:
#         raise ValueError("Car not found")
#     return car
#
# async def get_cars(session: AsyncSession, limit: int) -> Sequence[Car]:
#     stmt = select(Car).limit(limit)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
# async def update_car(session: AsyncSession, car_id: int, car_update: CarUpdate) -> Car:
#     stmt = select(Car).filter(Car.id == car_id)
#     result = await session.execute(stmt)
#     car = result.scalars().first()
#     if not car:
#         raise ValueError("Car not found")
#
#     for key, value in car_update.dict(exclude_unset=True).items():
#         setattr(car, key, value)
#
#     await session.commit()
#     await session.refresh(car)
#     return car
#
# async def delete_car(session: AsyncSession, car_id: int) -> Car:
#     stmt = select(Car).filter(Car.id == car_id)
#     result = await session.execute(stmt)
#     car = result.scalars().first()
#     if not car:
#         raise ValueError("Car not found")
#
#     await session.delete(car)
#     await session.commit()
#     return car
#
# # CRUD Operations for Service
# # async def create_service(session: AsyncSession, service_create: ServiceCreate, price: Price, time: Time) -> Service:
# #     service = Service(
# #         name=service_create.name,
# #         price=service_create.price.minValue,  # Получаем minValue из объекта Price
# #         time=service_create.time.second, # Время в секундах
# #     )
# #     session.add(service)
# #     await session.commit()
# #     await session.refresh(service)
# #     return service
# async def create_service(session: AsyncSession, service_create: ServiceCreate) -> Service:
#     service = Service(
#         name=service_create.name,
#         price=service_create.price.minValue,  # Используем поле minValue из Price
#         time=service_create.time.second,  # Используем поле second из Time
#     )
#     session.add(service)
#     await session.commit()
#     await session.refresh(service)
#     return service
#
# async def get_service(session: AsyncSession, service_id: int) -> Service:
#     stmt = select(Service).filter(Service.id == service_id)
#     result = await session.execute(stmt)
#     service = result.scalars().first()
#     if not service:
#         raise ValueError("Service not found")
#     return service
#
# async def get_services(session: AsyncSession, limit: int) -> Sequence[Service]:
#     stmt = select(Service).limit(limit)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
# async def update_service(session: AsyncSession, service_id: int, service_update: ServiceUpdate) -> Service:
#     stmt = select(Service).filter(Service.id == service_id)
#     result = await session.execute(stmt)
#     service = result.scalars().first()
#     if not service:
#         raise ValueError("Service not found")
#
#     for key, value in service_update.dict(exclude_unset=True).items():
#         setattr(service, key, value)
#
#     await session.commit()
#     await session.refresh(service)
#     return service
#
# async def delete_service(session: AsyncSession, service_id: int) -> Service:
#     stmt = select(Service).filter(Service.id == service_id)
#     result = await session.execute(stmt)
#     service = result.scalars().first()
#     if not service:
#         raise ValueError("Service not found")
#
#     await session.delete(service)
#     await session.commit()
#     return service
#
#
# # CRUD Operations for OrderService
# async def create_order_service(session: AsyncSession, order_service_create: OrderServiceCreate) -> OrderService:
#     order_service = OrderService(**order_service_create.dict())
#     session.add(order_service)
#     await session.commit()
#     await session.refresh(order_service)
#     return order_service
#
# async def get_order_service(session: AsyncSession, order_service_id: int) -> OrderService:
#     stmt = select(OrderService).filter(OrderService.id == order_service_id)
#     result = await session.execute(stmt)
#     order_service = result.scalars().first()
#     if not order_service:
#         raise ValueError("OrderService not found")
#     return order_service
#
# async def get_order_services(session: AsyncSession, limit: int) -> Sequence[OrderService]:
#     stmt = select(OrderService).limit(limit)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
# async def update_order_service(session: AsyncSession, order_service_id: int, order_service_update: OrderServiceUpdate) -> OrderService:
#     stmt = select(OrderService).filter(OrderService.id == order_service_id)
#     result = await session.execute(stmt)
#     order_service = result.scalars().first()
#     if not order_service:
#         raise ValueError("OrderService not found")
#
#     for key, value in order_service_update.dict(exclude_unset=True).items():
#         setattr(order_service, key, value)
#
#     await session.commit()
#     await session.refresh(order_service)
#     return order_service
#
# async def delete_order_service(session: AsyncSession, order_service_id: int) -> OrderService:
#     stmt = select(OrderService).filter(OrderService.id == order_service_id)
#     result = await session.execute(stmt)
#     order_service = result.scalars().first()
#     if not order_service:
#         raise ValueError("OrderService not found")
#
#     await session.delete(order_service)
#     await session.commit()
#     return order_service
#
# # CRUD Operations for Order
# async def create_order(session: AsyncSession, order_create: OrderCreate) -> Order:
#     order = Order(**order_create.dict())
#     session.add(order)
#     await session.commit()
#     await session.refresh(order)
#     return order
#
# async def get_order(session: AsyncSession, order_id: int) -> Order:
#     stmt = select(Order).filter(Order.id == order_id)
#     result = await session.execute(stmt)
#     order = result.scalars().first()
#     if not order:
#         raise ValueError("Order not found")
#     return order
#
# async def get_orders(session: AsyncSession, limit: int) -> Sequence[Order]:
#     stmt = select(Order).limit(limit)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
# async def update_order(session: AsyncSession, order_id: int, order_update: OrderUpdate) -> Order:
#     stmt = select(Order).filter(Order.id == order_id)
#     result = await session.execute(stmt)
#     order = result.scalars().first()
#     if not order:
#         raise ValueError("Order not found")
#
#     for key, value in order_update.dict(exclude_unset=True).items():
#         setattr(order, key, value)
#
#     await session.commit()
#     await session.refresh(order)
#     return order
#
# async def delete_order(session: AsyncSession, order_id: int) -> Order:
#     stmt = select(Order).filter(Order.id == order_id)
#     result = await session.execute(stmt)
#     order = result.scalars().first()
#     if not order:
#         raise ValueError("Order not found")
#
#     await session.delete(order)
#     await session.commit()
#     return order
#
# # CRUD Operations for Customer_Car
# async def create_customer_car(session: AsyncSession, customer_car_create: CustomerCarCreate) -> Customer_Car:
#     customer_car = Customer_Car(**customer_car_create.dict())
#     session.add(customer_car)
#     await session.commit()
#     await session.refresh(customer_car)
#     return customer_car
#
# async def get_customer_car(session: AsyncSession, customer_car_id: int) -> Customer_Car:
#     stmt = select(Customer_Car).filter(Customer_Car.id == customer_car_id)
#     result = await session.execute(stmt)
#     customer_car = result.scalars().first()
#     if not customer_car:
#         raise ValueError("CustomerCar not found")
#     return customer_car
#
# async def get_customer_cars(session: AsyncSession, limit: int) -> Sequence[Customer_Car]:
#     stmt = select(Customer_Car).limit(limit)
#     result = await session.execute(stmt)
#     return result.scalars().all()
#
# async def update_customer_car(session: AsyncSession, customer_car_id: int, customer_car_update: CustomerCarUpdate) -> Customer_Car:
#     stmt = select(Customer_Car).filter(Customer_Car.id == customer_car_id)
#     result = await session.execute(stmt)
#     customer_car = result.scalars().first()
#     if not customer_car:
#         raise ValueError("CustomerCar not found")
#
#     for key, value in customer_car_update.dict(exclude_unset=True).items():
#         setattr(customer_car, key, value)
#
#     await session.commit()
#     await session.refresh(customer_car)
#     return customer_car
#
# async def delete_customer_car(session: AsyncSession, customer_car_id: int) -> Customer_Car:
#     stmt = select(Customer_Car).filter(Customer_Car.id == customer_car_id)
#     result = await session.execute(stmt)
#     customer_car = result.scalars().first()
#     if not customer_car:
#         raise ValueError("CustomerCar not found")
#
#     await session.delete(customer_car)
#     await session.commit()
#     return customer_car