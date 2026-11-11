import time,hmac,hashlib
from app.adapters import verify_webhook
def test_webhook_accepts_correct_signature():
    body=b'{"status":"shipped"}'
    ts=str(int(time.time()))
    sig="sha256="+hmac.new(b"demo",ts.encode()+b"."+body,hashlib.sha256).hexdigest()
    assert verify_webhook(body,sig,ts,"demo",int(time.time()))
    assert not verify_webhook(body,sig,"1","demo",int(time.time()))
    assert not verify_webhook(b"tampered",sig,ts,"demo",int(time.time()))
