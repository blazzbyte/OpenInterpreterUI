.PHONY: all
all: build

CONTAINER_NAME=openinterpreterui
IMAGE_NAME=$(CONTAINER_NAME)
PORT=8501

.PHONY: build
build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run: build
	@echo "Running Docker container..."
	docker run -v $(PWD)/workspace:/workspace -p $(PORT):$(PORT) $(IMAGE_NAME)

.PHONY: stop
stop:
	@echo "Stopping Docker container..."
	docker stop $(CONTAINER_NAME)

.PHONY: test
test:
	@echo "Running tests..."
	./test.sh
