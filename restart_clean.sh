#!/bin/bash

# AWE Agency - Clean Restart Script
echo "🧹 Cleaning up processes and ports..."

# Kill any processes on our ports
lsof -ti:3000,8000,8002 | xargs kill -9 2>/dev/null || true

# Kill any uvicorn, next, or node dev processes
pkill -f "uvicorn\|next\|node.*dev" 2>/dev/null || true

echo "✅ All processes killed"
echo "🚀 Ready to restart with:"
echo "   Backend: python3 start_backend.py"
echo "   Frontend: cd frontend && npm run dev"
