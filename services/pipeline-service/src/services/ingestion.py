import os
import dlt
from dlt.sources.rest_api import rest_api_source

FLASK_API_URL = os.getenv("FLASK_API_URL", "http://localhost:5000")


def run_ingestion():
    source = rest_api_source({
        "client": {
            "base_url": FLASK_API_URL,
        },
        "resource_defaults": {
            "primary_key": "customer_id",
            "write_disposition": "merge",
            "endpoint": {
                "data_selector": "data",
            },
        },
        "resources": [
            {
                "name": "customers",
                "endpoint": {
                    "path": "api/customers",
                    "paginator": {
                        "type": "page_number",
                        "base_page": 1,
                        "page_param": "page",
                    },
                    "params": {
                        "limit": 50,
                    },
                },
            },
        ],
    })
    
    pipeline = dlt.pipeline(
        pipeline_name="customer_ingestion",
        destination="postgres",
        dataset_name="customer_db",
    )
    
    load_info = pipeline.run(source)
    
    row_counts = {}
    if pipeline.last_trace and pipeline.last_trace.last_normalize_info:
        row_counts = pipeline.last_trace.last_normalize_info.row_counts
    
    rows_loaded = row_counts.get("customers", 0)
    
    return {
        "load_info": str(load_info),
        "rows_loaded": rows_loaded,
        "row_counts": row_counts,
    }