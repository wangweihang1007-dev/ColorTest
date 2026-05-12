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

from fastapi.responses import HTMLResponse

@app.get("/api/admin/records", response_class=HTMLResponse)
async def get_admin_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestRecord).order_by(TestRecord.created_at.desc()))
    records = result.scalars().all()
    
    # Generate simple HTML table
    rows = ""
    for r in records:
        rows += f"""
        <tr class="border-b hover:bg-gray-50">
            <td class="px-4 py-2">{r.id}</td>
            <td class="px-4 py-2 font-bold">{r.final_color}</td>
            <td class="px-4 py-2 text-sm text-gray-600">{r.score_detail}</td>
            <td class="px-4 py-2 text-sm">{r.created_at}</td>
        </tr>
        """
    
    html_content = f"""
    <html>
        <head>
            <title>ColorQA Admin - 测试记录</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="bg-gray-100 p-8">
            <div class="max-w-6xl mx-auto bg-white rounded-xl shadow-md p-6">
                <h1 class="text-2xl font-bold mb-6 text-gray-800">所有测试记录 ({len(records)})</h1>
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-800 text-white">
                            <th class="px-4 py-2">ID</th>
                            <th class="px-4 py-2">主色调</th>
                            <th class="px-4 py-2">得分详情</th>
                            <th class="px-4 py-2">时间</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
                { '<p class="text-center py-10 text-gray-400">暂无数据</p>' if not records else '' }
            </div>
        </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
