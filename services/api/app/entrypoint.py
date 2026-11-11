"""Compose legacy commerce and optional agent UI with narrowly scoped POC CORS."""
from fastapi.middleware.cors import CORSMiddleware
from .main import app
from .agent import router as agent_router
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:18473","http://127.0.0.1:18473"],allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["Authorization","Content-Type"])
app.include_router(agent_router)
