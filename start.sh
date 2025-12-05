#!/bin/bash
# Silent Signal - Startup Script

echo "🚀 Starting Silent Signal..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your API keys before continuing."
    exit 1
fi

# Start Docker services
echo "🐳 Starting Docker services (PostgreSQL, Redis)..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if database is initialized
echo "🗄️  Checking database..."
python scripts/init_db.py

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    npm run build:css
    cd ..
fi

# Start the application
echo "✅ Starting Silent Signal API..."
echo "🌐 Application will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
