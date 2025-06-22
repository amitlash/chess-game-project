from fastapi import FastAPI
from app.api.routes import router as chess_router

app = FastAPI()
app.include_router(chess_router)