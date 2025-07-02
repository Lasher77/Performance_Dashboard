from fastapi import FastAPI
from .analysis import get_membership_metrics

app = FastAPI()

@app.get('/metrics')
def read_metrics():
    return get_membership_metrics()
