import sys
import os

# Add backend directory to path so we can import app
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.api import questions, records
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Standard CORS for local dev, Vercel handles same-origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router, prefix="/api")
app.include_router(records.router, prefix="/api")

@app.get("/api/health")
async def health():
    return {"status": "healthy"}
