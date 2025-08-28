.PHONY: train build run
train:
	python model/train.py --input data/message_dataset.csv --out model/artifacts
build:
	docker build -t a2p-spam:latest .
run:
	docker run -p 8080:8080 a2p-spam:latest
