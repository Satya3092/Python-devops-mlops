IMAGE ?= server-failure-api
TAG   ?= 2.0.0

.PHONY: install train test run docker-build docker-run smoke k8s-deploy clean

install:
	pip install -r requirements-dev.txt

train:
	python train.py --config config.yaml

test:
	pytest -q

run: train
	uvicorn app:app --reload --port 8000

docker-build:
	docker build -t $(IMAGE):$(TAG) .

docker-run:
	docker run -d --rm --name $(IMAGE) -p 8000:8000 $(IMAGE):$(TAG)

smoke:
	BASE_URL=http://127.0.0.1:8000 python smoke_test.py

k8s-deploy:
	kubectl apply -f k8s/ && kubectl rollout status deployment/$(IMAGE)

clean:
	rm -rf models __pycache__ .pytest_cache tests/__pycache__
