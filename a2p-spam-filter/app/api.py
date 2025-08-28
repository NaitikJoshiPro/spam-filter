from fastapi import FastAPI
from pydantic import BaseModel
from app.whitelist import is_whitelisted
from app.rules import hard_block
from app.inference import predict_single, load_model
from app.config import load_settings, load_whitelist
from app.logging_utils import log_event

app = FastAPI(title='A2P SMS Spam Filter')

settings = load_settings()
whitelist = load_whitelist()

class SMSIn(BaseModel):
    message: str

@app.on_event('startup')
def startup_event():
    # Preload model
    try:
        load_model(settings.get('vectorizer_path','model/artifacts/vectorizer.joblib'),
                   settings.get('model_path','model/artifacts/model.joblib'))
    except Exception as e:
        print('Model load error (startup):', e)

@app.post('/check_sms')
def check_sms(payload: SMSIn):
    msg = payload.message.strip()
    if is_whitelisted(msg, whitelist):
        log_event(msg, 'allowed', 'whitelisted', meta={})
        return {'verdict':'allowed','reason':'whitelisted'}
    rule = hard_block(msg)
    if rule:
        log_event(msg, 'blocked', 'rule_match', meta={'rule':rule})
        return {'verdict':'blocked','reason':'rule_match'}
    pred, p_spam, latency_ms = predict_single(msg)
    settings_local = settings or {}
    threshold = float(settings_local.get('block_threshold', 0.8))
    if pred == 'spam' and p_spam >= threshold:
        log_event(msg, 'blocked', 'ai', meta={'label':pred,'p_spam':p_spam,'latency_ms':latency_ms})
        return {'verdict':'blocked','reason':'ai','label':pred,'confidence':p_spam}
    else:
        log_event(msg, 'allowed', 'ai', meta={'label':pred,'p_spam':p_spam,'latency_ms':latency_ms})
        return {'verdict':'allowed','reason':'ai','label':pred,'confidence':p_spam}
