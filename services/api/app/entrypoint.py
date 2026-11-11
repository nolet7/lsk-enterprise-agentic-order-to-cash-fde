"""Application composition: legacy commerce runs without a model; AI is optional."""
from .main import app
from .agent import router as agent_router
app.include_router(agent_router)
