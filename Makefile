.PHONY: help install start stop clean test deploy

help:
	@echo "Silent Signal - Available Commands"
	@echo ""
	@echo "  make install    - Install all dependencies"
	@echo "  make start      - Start the application"
	@echo "  make stop       - Stop all services"
	@echo "  make clean      - Clean temporary files"
	@echo "  make test       - Run tests"
	@echo "  make deploy     - Deploy to production"
	@echo "  make logs       - View application logs"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	cd frontend && npm install
	@echo "Dependencies installed!"

start:
	@echo "Starting Silent Signal..."
	docker-compose up -d
	sleep 5
	python scripts/init_db.py
	uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

stop:
	@echo "Stopping services..."
	docker-compose down

clean:
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

test:
	@echo "Running tests..."
	pytest --cov=backend

deploy:
	@echo "Deploying to production..."
	cd deploy && ./vultr_deploy.sh

logs:
	docker-compose logs -f

db-init:
	python scripts/init_db.py

db-seed:
	python scripts/seed_demo_data.py

frontend-build:
	cd frontend && npm run build:css
