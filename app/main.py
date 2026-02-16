from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="Currency Converter")
app.include_router(router)
