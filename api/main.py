from fastapi import FastAPI
from dotenv import load_dotenv
import os
from database_module import connect_to_db, close_db
from routes import router

load_dotenv()

app = FastAPI()
app.include_router(router, prefix="/api")

@app.on_event("startup")
async def startup():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Hello from RentFlatBot"}
