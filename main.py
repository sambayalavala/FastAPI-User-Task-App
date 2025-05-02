from fastapi import FastAPI, Depends, HTTPException
from apis.user import router as user_router  # Single import
from models.user import Base, User
from database import engine, get_db
from sqlalchemy.orm import Session

# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes (ONCE)
app.include_router(user_router)  # ✅ Only register once

# Middleware (optional)
@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Custom-Header"] = "CustomValue"
    return response


