from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.db import engine, Base
from app.models import User, Depot, Granary, GranaryConfig # Import to register models
from app.api.endpoints import users, depots, granaries, auth

app = FastAPI(title="Grain Management System")

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:5173", # Vite default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(depots.router, prefix="/api/depots", tags=["depots"])
app.include_router(granaries.router, prefix="/api/granaries", tags=["granaries"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to Grain Management System API"}
