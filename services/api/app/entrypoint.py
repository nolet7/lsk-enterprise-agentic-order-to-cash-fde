"""Stage composition; OIDC override only when explicitly enabled."""
import os
from fastapi.middleware.cors import CORSMiddleware
from .main import app,identity,Base,engine
from .agent import router as agent_router
from .pilot import router as pilot_router
from .oidc import oidc_identity
app.add_middleware(CORSMiddleware,allow_origins=os.getenv("ALLOWED_ORIGINS","http://localhost:18473").split(","),allow_credentials=False,allow_methods=["GET","POST"],allow_headers=["Authorization","Content-Type"])
app.include_router(agent_router)
app.include_router(pilot_router)
if os.getenv("AUTH_MODE")=="oidc":
    app.dependency_overrides[identity]=oidc_identity
