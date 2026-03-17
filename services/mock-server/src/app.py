import json
import os
from flask import Flask, jsonify, request, abort
from datetime import datetime

from packages.shared.src.schemas import (
    HealthResponse,
    CustomerResponse,
    PaginatedResponse,
    ErrorResponse,
)

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "customers.json")


def load_customers():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


_customers = None


def get_customers():
    global _customers
    if _customers is None:
        _customers = load_customers()
    return _customers


@app.route("/api/health", methods=["GET"])
def health_check():
    response = HealthResponse(status="healthy")
    return jsonify(response.model_dump())


@app.route("/api/customers", methods=["GET"])
def get_customers_list():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    
    if page < 1:
        page = 1
    if limit < 1:
        limit = 10
    
    customers = get_customers()
    total = len(customers)
    
    start = (page - 1) * limit
    end = start + limit
    paginated_data = customers[start:end]
    
    response = PaginatedResponse(
        data=paginated_data,
        total=total,
        page=page,
        limit=limit
    )
    return jsonify(response.model_dump())


@app.route("/api/customers/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customers = get_customers()
    
    for customer in customers:
        if customer.get("customer_id") == customer_id:
            if customer.get("created_at"):
                customer["created_at"] = datetime.fromisoformat(customer["created_at"])
            
            response = CustomerResponse(**customer)
            return jsonify(response.model_dump())
    
    abort(404, description=f"Customer {customer_id} not found")


@app.errorhandler(404)
def resource_not_found(e):
    response = ErrorResponse(error=str(e))
    return jsonify(response.model_dump()), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)