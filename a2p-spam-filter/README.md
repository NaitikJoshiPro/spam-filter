# A2P SMS Spam Filter (GCP-ready)

This repository contains a lightweight AI-powered spam filtering system for A2P SMS messages.
It includes data preprocessing, model training (scikit-learn), a FastAPI inference service, whitelist/rule checks, Dockerfile, and configs ready for deployment to GCP (Cloud Run or GCE MIG).

## Contents
- `app/` - FastAPI service and helper modules
- `model/` - training & evaluation scripts and artifacts
- `configs/` - whitelist and settings YAML files
- `data/` - provided dataset (message_dataset.csv)

## Quick start (local)
1. Build Docker image:
   ```bash
   docker build -t a2p-spam:latest .
   ```
2. Run container:
   ```bash
   docker run -p 8080:8080 a2p-spam:latest
   ```
3. Example request:
   ```bash
   curl -X POST http://localhost:8080/check_sms -H "Content-Type: application/json" -d '{"message":"Your OTP is 123456"}'
   ```

## Train model (locally)
Run the training script to produce `model/artifacts/model.joblib` and `model/artifacts/vectorizer.joblib`:
```bash
python model/train.py --input data/message_dataset.csv --out model/artifacts
```

## Deploy to GCP (Cloud Run recommended)
- Build and push image to Artifact Registry, then deploy to Cloud Run.
- Alternatively, use a Managed Instance Group (MIG) template with the container image.

See `model/train.py` and `app/` files for implementation details and configs in `configs/`.
