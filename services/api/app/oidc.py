"""Pilot verified OIDC identity. Only signed claims can grant tenant/customer scope."""
import os
from functools import lru_cache
from fastapi import HTTPException, Header
import jwt
from jwt import PyJWKClient

@lru_cache
def jwks_client():
    url=os.environ.get("OIDC_JWKS_URL")
    if not url or not url.startswith("https://") and not os.environ.get("OIDC_ALLOW_HTTP_LOCAL"):
        raise RuntimeError("Validated OIDC_JWKS_URL is required")
    return PyJWKClient(url,cache_jwk_set=True,lifespan=300,timeout=5)
def oidc_identity(authorization:str|None=Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401,"Bearer token required")
    try:
        encoded=authorization.removeprefix("Bearer ").strip()
        key=jwks_client().get_signing_key_from_jwt(encoded).key
        payload=jwt.decode(encoded,key,algorithms=["RS256"],issuer=os.environ["OIDC_ISSUER"],audience=os.environ["OIDC_AUDIENCE"],options={"require":["exp","iat","iss","sub","aud"]},leeway=30)
        tenant=payload.get("tenant_id")
        customer=payload.get("customer_id")
        roles=payload.get("realm_access",{}).get("roles",[])
        role="csr" if "lsk-csr" in roles else "buyer" if "lsk-buyer" in roles else None
        if not role or not isinstance(tenant,str) or not tenant:
            raise HTTPException(403,"Missing authorized tenant or role")
        if role=="buyer" and (not isinstance(customer,str) or not customer):
            raise HTTPException(403,"Missing bound customer")
        return (tenant,payload["sub"],customer if role=="buyer" else None,role)
    except HTTPException: raise
    except (jwt.PyJWTError,KeyError,ValueError,RuntimeError):
        raise HTTPException(401,"Invalid signed OIDC token")
