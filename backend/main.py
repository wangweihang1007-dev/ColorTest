import os
import sys
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

# Ensure backend directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from app.core.database import get_db
from app.models.database import TestRecord
from app.api import questions, records

app = FastAPI(title="ColorQA API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for production or specify your Render URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers with /api prefix
app.include_router(questions.router, prefix="/api")
app.include_router(records.router, prefix="/api")

# Serve Frontend Static Files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    
    # Catch-all route for SPA (Vue Router)
    @app.exception_handler(404)
    async def not_found_handler(request, exc):
        if not request.url.path.startswith("/api"):
            return FileResponse(os.path.join(frontend_path, "index.html"))
        return {"detail": "Not Found"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/admin/records")
async def get_admin_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestRecord).order_by(TestRecord.created_at.desc()))
    records = result.scalars().all()
    return records

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
