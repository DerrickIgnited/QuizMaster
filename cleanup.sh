#!/bin/bash

echo "Stopping Celery workers and beat..."
pkill -f 'celery'

echo "Stopping Redis server..."
pkill -f 'redis-server'

echo "Freeing up port 8001 (Flask)..."
lsof -ti :8001 | xargs kill -9 2>/dev/null

echo "Freeing up port 5173 (Vite)..."
lsof -ti :5173 | xargs kill -9 2>/dev/null

echo "Verifying remaining processes..."
pkill -f 'celery'
pkill -f 'redis-server'

echo "Celery:"
ps aux | grep celery | grep -v grep

echo "Redis:"
ps aux | grep redis | grep -v grep

echo "Port 8001 usage:"
lsof -i :8001

echo "Port 5173 usage:"
lsof -i :5173

echo "Deleting Celery schedule database..."
rm -rf backend/new-schedule.db*

echo "Cleanup complete."
