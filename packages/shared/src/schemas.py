from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional, List, Any


class HealthResponse(BaseModel):
    status: str


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None
    account_balance: Optional[float] = None
    created_at: Optional[datetime] = None


class CustomerResponse(CustomerBase):
    pass


class PaginatedResponse(BaseModel):
    data: List[Any]
    total: int
    page: int
    limit: int


class IngestResponse(BaseModel):
    status: str
    records_processed: int
    details: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str