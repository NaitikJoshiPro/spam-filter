from app.config import load_whitelist
import re
import tldextract

wl = load_whitelist()

def extract_domain(s):
    # find first domain-like token
    try:
        ext = tldextract.extract(s)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}"
    except Exception:
        return None
    return None

def is_whitelisted(message, whitelist=None):
    if whitelist is None:
        whitelist = wl
    msg = message.lower()
    # phrase whitelist
    for ph in whitelist.get('phrases', []):
        if ph.lower() in msg:
            return True
    # domain whitelist
    dom = extract_domain(msg)
    if dom and dom.lower() in [d.lower() for d in whitelist.get('domains', [])]:
        return True
    return False
