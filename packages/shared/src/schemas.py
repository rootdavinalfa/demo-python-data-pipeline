from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from decimal import Decimal
from typing import Optional


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    account_balance: Decimal
    created_at: datetime


class CustomerResponse(CustomerBase):
    pass


class PaginatedResponse(BaseModel):
    data: list
    total: int
    page: int
    limit: int


class IngestResponse(BaseModel):
    status: str
    records_processed: int