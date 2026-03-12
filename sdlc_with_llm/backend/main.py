"""
FastAPI main application for IT Support Portal.

This module initializes the FastAPI application, configures CORS,
includes routers, and manages database lifecycle.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.database.connection import init_db, close_db
from backend.routers import tickets, analytics, users

# Load environment variables
load_dotenv()

# Get CORS origins from environment
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for database connection.

    Handles startup and shutdown events:
    - Startup: Initialize database tables
    - Shutdown: Close database connections

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI application
app = FastAPI(
    title="IT Support Portal API",
    description="Backend API for IT Support Portal with ticket management and analytics",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tickets.router)
app.include_router(analytics.router)
app.include_router(users.router)


@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "IT Support Portal API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "ok"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "healthy"}
