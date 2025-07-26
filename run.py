import subprocess
import sys
import threading
import time
import socket

def cleanup():
    try:
        subprocess.run(["./cleanup.sh"], check=True)
        print("cleanup.sh executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error while running cleanup.sh")
        print(e)

def wait_for_redis(port=6379, timeout=30):
    """Check if Redis is up before starting Celery"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            socket.create_connection(("localhost", port), timeout=1)
            print("Redis is up and running")
            return True
        except OSError:
            time.sleep(1)
    print("Redis did not start in time")
    return False

def run_redis():
    try:
        subprocess.Popen(['redis-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Redis server starting...")
    except FileNotFoundError:
        print("Redis not found. Please install Redis first.")
        sys.exit(1)

def run_celery():
    # and imports tasks so they are registered
    hostname = socket.gethostname()
    subprocess.Popen(['celery', '-A', 'tasks.reminders', 'worker', '-n', f'worker@{hostname}', '--loglevel=info'], cwd='backend')
    subprocess.Popen(['celery', '-A', 'tasks.reminders', 'beat', '--schedule=new-schedule.db', '--loglevel=info'], cwd='backend')
    print("Celery worker and beat started")

def run_backend():
    subprocess.Popen(['python', 'app.py'], cwd='backend')
    print("Backend started")

def run_frontend():
    subprocess.Popen(['npm', 'run', 'dev', '--', '--host'], cwd='frontend')
    print("Frontend started")

def main():
    print("Starting Quiz Master V2...")

    cleanup()
    # Start Redis
    threading.Thread(target=run_redis).start()
    if not wait_for_redis():
        sys.exit(1)

    # Start Celery (beat + worker)
    threading.Thread(target=run_celery).start()
    time.sleep(5)

    # Start Frontend
    threading.Thread(target=run_frontend).start()
    time.sleep(3)

    # Start Backend (Flask or FastAPI app)
    run_backend()

if __name__ == "__main__":
    main()
