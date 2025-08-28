# AI-Powered Spam Filter for A2P SMS

This repository contains an **AI-powered spam filtering system** for **A2P (Application-to-Person) SMS messages**.  
It combines **rule-based filtering**, a **whitelisting layer**, and a **lightweight ML classifier** to reduce false positives while blocking spam and scams.  

## Project Overview
- Classifies SMS into **Transactional / Promotional / Spam**
- Supports **trusted whitelist bypass** (domains, OTP templates, sender IDs)
- Runs in **real-time (<100ms/message on CPU)** inside a containerized API

## Live Demo (Temporary)
This service is currently **live** on our GCP instance and open for testing for the next week. (also just a heads up the sub 100ms wont be possible for the time being because the gcp instance that i wanted wasnt available in the Mumbai region, i usually do GPU heavy stuff so i use L4's which are not generally available here)

### Base URL
http://34.59.101.42:8080/check_sms

### Example Requests (feel free to change the messages and try to break this model)

#### OTP / Transactional (should be allowed via whitelist)
```bash
curl -X POST http://34.59.101.42:8080/check_sms \
  -H "Content-Type: application/json" \
  -d '{"message":"Your OTP is 123456 for ICICI login"}'
```
#### Expected Output
```
{
  "verdict": "allowed",
  "reason": "whitelisted"
}

```

### Base URL
## Features
- **SMS preprocessing & dataset cleaning**
  - Deduplication, lowercasing, noise/URL stripping
  - Final dataset with `message, category, cleaned_message`
- **Lightweight ML model**
  - `TfidfVectorizer` + `SGDClassifier` (scikit-learn)
  - Fast inference, CPU-only, <5ms per message
- **Whitelisting layer**
  - Trusted domains (e.g. `trip.com`)
  - OTP templates & safe phrases (e.g. “Your OTP is …”)
  - Optional sender IDs
- **Rule-based checks**
  - Block obvious scams (shortlinks, “free money” phrases, etc.)
- **REST API (FastAPI)**
  - `POST /check_sms`
  - Input: `{"message":"..."}`
  - Output: `{"verdict":"allowed|blocked","reason":"whitelisted|ai|rule_match"}`
- **Config-driven**
  - YAML configs for whitelist & thresholds
- **Logging**
  - Every processed SMS is logged (JSON logs → Cloud Logging)
- **Deployment-ready**
  - Dockerized app
  - Runs on **GCP VM / MIG / Cloud Run**
  - Handles **1000+ messages/sec** with autoscaling

---

## Repository Structure

```text
a2p-spam-filter/
├── app/                 
│   ├── api.py           # REST API (FastAPI)
│   ├── inference.py     # Model loading & prediction
│   ├── whitelist.py     # Whitelisting checks
│   ├── rules.py         # Rule-based filters
│   ├── config.py        # Config loader (YAML)
│   └── logging_utils.py # JSON structured logs
├── model/
│   ├── train.py         # Training pipeline
│   ├── eval.py          # Evaluation script
│   └── artifacts/       # Saved model + vectorizer
├── configs/
│   ├── whitelist.yml    # Trusted domains/phrases/senders
│   └── settings.yml     # Thresholds, paths
├── data/
│   └── README.md        # (Dataset not included – add your CSV here)
├── scripts/
│   └── clean_csv.py     # Dataset cleaning utility
├── Dockerfile           # Container build
├── requirements.txt     # Python deps
├── Makefile             # Shortcuts for train/build/run
└── README.md            # This file
```
