"""Bounded HTTP adapter for sandbox ERP/CRM/WMS/Billing; read retries only."""
import time
import hmac
import hashlib
from collections import defaultdict
import httpx
from fastapi import HTTPException

class AdapterUnavailable(Exception): pass
class IntegrationClient:
    def __init__(self, base_url:str,token:str):
        self.base_url=base_url.rstrip("/")
        self.token=token
        self.failures=0
        self.open_until=0.0
    def get(self,path:str):
        if time.monotonic()<self.open_until:raise AdapterUnavailable("circuit open")
        with httpx.Client(timeout=httpx.Timeout(4,connect=2)) as client:
            for attempt in range(3):
                try:
                    response=client.get(self.base_url+path,headers={"Authorization":"Bearer "+self.token})
                    response.raise_for_status()
                    self.failures=0
                    return response.json()
                except (httpx.TransportError,httpx.HTTPStatusError):
                    self.failures+=1
                    if self.failures>=3:
                        self.open_until=time.monotonic()+30
                        break
                    time.sleep(.1*(2**attempt))
        raise AdapterUnavailable("authoritative system unavailable; do not fabricate data")
def verify_webhook(body:bytes,signature:str,timestamp:str,secret:str,now_seconds:int):
    try: ts=int(timestamp)
    except (ValueError,TypeError):return False
    if abs(now_seconds-ts)>300:return False
    digest=hmac.new(secret.encode(),timestamp.encode()+b"."+body,hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature,"sha256="+digest)
