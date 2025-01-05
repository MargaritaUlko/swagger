# Pydantic Schemas
from datetime import datetime
from http.client import HTTPException
from typing import Optional, Any

from pydantic import BaseModel, root_validator, Field, field_validator
from sqlalchemy.future import select

from core.models import Order


class BrandBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        from_attributes = True
class BrandCreate(BrandBase):
    pass

class BrandRead(BrandBase):
    id: int

class CarBase(BaseModel):
    model: str
    brand_id: int

class CarCreate(CarBase):
    pass
class CarUpdate(CarBase):
    pass
class CarRead(BaseModel):
    id: int
    model: str
    brand: BrandBase


    class Config:
        orm_mode = True
        from_attributes = True


class CarsResponse(BaseModel):
    cars: list[CarRead]
    pagination: dict
class ServiceBase(BaseModel):
    pass

class Price(BaseModel):
    minValue: int
    maxValue: int = Field(0)
    format: str = Field("")

class Time(BaseModel):
    second: int
    minute: int = Field(0)

class ServiceCreate(BaseModel):
    name: str
    price: Price
    time: Time

class ServiceRead(BaseModel):
    id: int
    name: str
    price: Price
    time: Time

    @classmethod
    def from_orm(cls, obj: Any) -> "ServiceRead":
        # Используем преобразования, которые уже сделали в модели Service
        price = Price(minValue=obj.price, maxValue=obj.convert_price(obj.price),
                      format=f"{obj.convert_price(obj.price)} руб.")

        # Преобразуем время в экземпляр Time
        time = Time(second=obj.time, minute=obj.convert_time(obj.time))  # Переводим в минуты и секунды

        return cls(id=obj.id, name=obj.name, price=price, time=time)

    class Config:
        orm_mode = True
        from_attributes = True


class OrderServiceBase(BaseModel):
    service_id: int
    order_id: int

class OrderServiceCreate(OrderServiceBase):
    pass

class OrderServiceRead(OrderServiceBase):
    id: int


class OrderBase(BaseModel):
    administrator_id: int
    customer_car_id: int
    employee_id: int
    status: int
    start_date: datetime = Field(default_factory=datetime.utcnow)
    end_date: datetime




class OrderCreate(OrderBase):
    status: int = 1
    @root_validator(pre=True)
    def enforce_status(cls, values):
            values["status"] = 1  # Принудительно устанавливаем статус
            return values
class OrderRead(OrderBase):
    id: int



# class CustomerCarRead(CustomerCarBase):
#     id: int

class UserRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
class CustomerCarBase(BaseModel):
    car_id: int
    customer_id: int
    year: int
    number: str

class CustomerCarCreate(CustomerCarBase):
    pass

class CustomerCarRead(BaseModel):
    id: int
    year: int
    number: str
    car: CarRead
    customer: UserRead

    class Config:
        orm_mode = True

class CustomerCarUpdate(BaseModel):
    customer_id: int
    year: int
    number: str

class OrderServiceUpdate(BaseModel):

    service_id: Optional[int] = None
    order_id: Optional[int] = None

class OrderUpdate(BaseModel):
    administrator_id: Optional[int] = None
    customer_car_id: Optional[int] = None
    employee_id: Optional[int] = None
    status: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    time: Optional[int] = None



class BrandUpdate(BaseModel):
    name: Optional[str] = None
