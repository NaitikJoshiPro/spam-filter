import time, json, hashlib

def log_event(message, verdict, reason, meta=None):
    meta = meta or {}
    record = {
        'ts': time.time(),
        'msg_hash': hashlib.sha1(message.encode('utf-8')).hexdigest()[:10],
        'verdict': verdict,
        'reason': reason,
        'meta': meta
    }
    print(json.dumps(record, ensure_ascii=False))
