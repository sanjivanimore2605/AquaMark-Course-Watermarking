#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting AquaMark Secure Document Platform"
echo "=========================================================="

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Start Backend FastAPI Server
echo "-> Starting Backend on http://127.0.0.1:8000..."
cd "$ROOT_DIR/backend"
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# 2. Start Frontend Vite Development Server
echo "-> Starting Frontend on http://127.0.0.1:3000..."
cd "$ROOT_DIR/frontend"
npm run dev -- --host 127.0.0.1 --port 3000 &
FRONTEND_PID=$!

trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT SIGTERM

echo "AquaMark is live!"
echo "-> Web Application: http://localhost:3000"
echo "-> Interactive API Docs: http://localhost:8000/docs"
wait
