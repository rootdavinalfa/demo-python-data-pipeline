import os
import httpx
import dlt
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.customer import Customer
from database import engine


FLASK_API_URL = os.getenv("FLASK_API_URL", "http://localhost:5000")


@dlt.resource(name="customers", write_disposition="merge", primary_key="customer_id")
def fetch_customers_from_flask():
    page = 1
    limit = 10
    all_customers = []
    
    with httpx.Client() as client:
        while True:
            response = client.get(
                f"{FLASK_API_URL}/api/customers",
                params={"page": page, "limit": limit}
            )
            response.raise_for_status()
            data = response.json()
            
            customers = data.get("data", [])
            all_customers.extend(customers)
            
            if len(all_customers) >= data.get("total", 0):
                break
            page += 1
    
    for customer in all_customers:
        yield customer


def upsert_customers(db: Session, customers: list) -> int:
    for customer_data in customers:
        customer_dict = {
            "customer_id": customer_data.get("customer_id"),
            "first_name": customer_data.get("first_name"),
            "last_name": customer_data.get("last_name"),
            "email": customer_data.get("email"),
            "phone": customer_data.get("phone"),
            "address": customer_data.get("address"),
            "date_of_birth": customer_data.get("date_of_birth"),
            "account_balance": customer_data.get("account_balance"),
            "created_at": customer_data.get("created_at"),
        }
        
        if customer_dict["date_of_birth"]:
            customer_dict["date_of_birth"] = datetime.strptime(
                customer_dict["date_of_birth"], "%Y-%m-%d"
            ).date()
        
        if customer_dict["created_at"]:
            customer_dict["created_at"] = datetime.fromisoformat(
                customer_dict["created_at"].replace("Z", "+00:00")
            )
        
        stmt = insert(Customer.__table__).values(**customer_dict)
        stmt = stmt.on_conflict_do_update(
            index_elements=["customer_id"],
            set_={
                "first_name": stmt.excluded.first_name,
                "last_name": stmt.excluded.last_name,
                "email": stmt.excluded.email,
                "phone": stmt.excluded.phone,
                "address": stmt.excluded.address,
                "date_of_birth": stmt.excluded.date_of_birth,
                "account_balance": stmt.excluded.account_balance,
                "created_at": stmt.excluded.created_at,
            }
        )
        db.execute(stmt)
    
    db.commit()
    return len(customers)


def run_ingestion(db: Session) -> int:
    all_customers = list(fetch_customers_from_flask())
    return upsert_customers(db, all_customers)