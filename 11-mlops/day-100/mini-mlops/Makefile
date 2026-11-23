# Convenience commands (Linux/macOS/WSL). On Windows run the commands manually.
IMAGE ?= server-failure-api
TAG   ?= 1.0.0

.PHONY: install train test run docker-build docker-run smoke clean

install:
	pip install -r requirements-dev.txt

train:
	python train.py

test: train
	pytest -q

run: train
	uvicorn app:app --reload --port 8000

docker-build:
	docker build -t $(IMAGE):$(TAG) .

docker-run:
	docker run -d --rm --name $(IMAGE) -p 8000:8000 $(IMAGE):$(TAG)

smoke:
	BASE_URL=http://127.0.0.1:8000 python smoke_test.py

clean:
	rm -rf models __pycache__ .pytest_cache
