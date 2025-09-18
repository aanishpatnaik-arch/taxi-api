from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Taxi Trips API")

# Register routes
app.include_router(router, prefix="/api/v1")
