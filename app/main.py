# backend/app/main.py
from fastapi import FastAPI
from .routers import cases, characters, llm
from .database import engine, Base
from .utils import create_initial_data
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Shadows of Veritas Backend")

# Remove the synchronous call to create_all()
# Base.metadata.create_all(bind=engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cases.router)
app.include_router(characters.router)
app.include_router(llm.router)

@app.on_event("startup")
async def startup_event():
    # Create tables asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Optionally, create initial data
    # await create_initial_data()
