from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError

from database import get_db, engine, Base
from models.customer import Customer
from services.ingestion import run_ingestion
from packages.shared.src.schemas import (
    HealthResponse,
    CustomerResponse,
    PaginatedResponse,
    IngestResponse,
    ErrorResponse,
)

app = FastAPI(title="Pipeline Service", description="Data ingestion pipeline")


@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
    except ProgrammingError:
        pass


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy")


@app.post("/api/ingest", response_model=IngestResponse)
def ingest_data():
    try:
        result = run_ingestion()
        return IngestResponse(
            status="success",
            records_processed=result.get("rows_loaded", 0),
            details=result.get("load_info", ""),
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error=str(e)
            ).model_dump()
        )


@app.get("/api/customers", response_model=PaginatedResponse)
def get_customers(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    
    total = db.query(Customer).count()
    offset = (page - 1) * limit
    
    customers = db.query(Customer).offset(offset).limit(limit).all()
    
    data = []
    for c in customers:
        data.append({
            "customer_id": c.customer_id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address,
            "date_of_birth": str(c.date_of_birth) if c.date_of_birth else None,
            "account_balance": float(c.account_balance) if c.account_balance else None,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        })
    
    return PaginatedResponse(
        data=data,
        total=total,
        page=page,
        limit=limit
    )


@app.get("/api/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if not customer:
        raise HTTPException(
            status_code=404, 
            detail=f"Customer {customer_id} not found"
        )
    
    return CustomerResponse(
        customer_id=customer.customer_id,
        first_name=customer.first_name,
        last_name=customer.last_name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address,
        date_of_birth=customer.date_of_birth,
        account_balance=float(customer.account_balance) if customer.account_balance else None,
        created_at=customer.created_at,
    )