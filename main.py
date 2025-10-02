from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routes import upload, generate, recommend, feedback, sustainability
from services.database import init_database
from services.carbon_tracker import CarbonTracker

# Load environment variables
load_dotenv()

# Initialize carbon tracker
carbon_tracker = CarbonTracker()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_database()
    carbon_tracker.start_tracking()
    yield
    # Shutdown
    carbon_tracker.stop_tracking()

app = FastAPI(
    title="EcoAd AI Backend",
    description="AI-powered adtech platform for personalized, sustainable advertising",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(generate.router, prefix="/generate", tags=["Generate"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommend"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
app.include_router(sustainability.router, prefix="/sustainability", tags=["Sustainability"])

@app.get("/")
async def root():
    return {
        "message": "EcoAd AI Backend API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "carbon_tracking": carbon_tracker.is_tracking
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
