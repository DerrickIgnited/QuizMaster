import subprocess
import sys
import threading
import time

def run_redis():
    try:
        subprocess.Popen(['redis-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Redis server started")
    except FileNotFoundError:
        print("Redis not found. Please install Redis first.")
        sys.exit(1)

def run_celery():
    subprocess.Popen(['celery', '-A', 'app.celery', 'worker', '--loglevel=info'], cwd='backend')
    subprocess.Popen(['celery', '-A', 'app.celery', 'beat', '--loglevel=info'], cwd='backend')
    print("Celery worker and beat started")

def run_backend():
    subprocess.run(['python', 'app.py'], cwd='backend')

def run_frontend():
    subprocess.run(['npm', 'run', 'dev'], cwd='frontend')

def main():
    print("Starting Quiz Master V2...")
    threading.Thread(target=run_redis).start()
    time.sleep(5)  # Wait for Redis to start
    threading.Thread(target=run_celery).start()
    time.sleep(5)  # Wait for Celery to start
    threading.Thread(target=run_frontend).start()
    time.sleep(5)  # Wait for frontend to start

    run_backend()

if __name__ == "__main__":
    main()
