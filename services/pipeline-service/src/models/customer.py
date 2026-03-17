from sqlalchemy import Column, String, Text, Date, Numeric, DateTime
from database import Base


class Customer(Base):
    __tablename__ = "customers"
    __table_args__ = {"schema": "customer_db"}

    customer_id = Column(String(50), primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    date_of_birth = Column(Date)
    account_balance = Column(Numeric(15, 2))
    created_at = Column(DateTime)
    _dlt_load_id = Column(String(50))
    _dlt_id = Column(String(50))