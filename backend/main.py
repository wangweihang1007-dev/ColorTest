from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import questions, records

app = FastAPI(title="ColorQA API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(questions.router)
app.include_router(records.router)

@app.get("/")
async def root():
    return {"message": "Welcome to ColorQA API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
