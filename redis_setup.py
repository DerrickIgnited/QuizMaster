import redis
import subprocess
import sys

def setup_redis():
    """Setup Redis server"""
    try:
        # Test Redis connection
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("Redis is already running")
        return True
    except redis.ConnectionError:
        print("Redis is not running")
        print("MacOS: brew install redis")
        return False

if __name__ == "__main__":
    setup_redis()