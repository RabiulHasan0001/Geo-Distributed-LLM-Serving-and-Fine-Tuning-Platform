from prometheus_client import Counter, generate_latest
from fastapi import FastAPI

app = FastAPI()
request_count = Counter("requests_total", "Total API Requests")

@app.get("/metrics")
def metrics():
    return generate_latest()
