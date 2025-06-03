from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.api.routes import capa, auth, documents
from app.core.database import engine, Base
from app.core.security import get_current_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QMS API",
    description="Pharma-compliant Quality Management System API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(
    capa.router,
    prefix="/api/capa",
    tags=["CAPA"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    documents.router,
    prefix="/api/documents",
    tags=["Documents"],
    dependencies=[Depends(get_current_user)]
)

@app.get("/")
async def root():
    return {"message": "QMS API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 