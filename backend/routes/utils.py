import json
import redis
from functools import wraps
from flask import request, jsonify

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_response(key_prefix, timeout=300):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = f"{key_prefix}_{request.path}"
            # Add any query parameters to the key
            if request.args:
                key += "?" + "&".join([f"{k}={v}" for k, v in request.args.items()])

            cached_data = redis_client.get(key)
            if cached_data:
                try:
                    return jsonify(json.loads(cached_data))
                except json.JSONDecodeError:
                    # Handle potential JSON decoding errors
                    print(f"JSONDecodeError for key: {key}")
                    pass  # Proceed to fetch from the database

            response = f(*args, **kwargs)
            try:
                redis_client.setex(key, timeout, json.dumps(response.get_json()))
            except (AttributeError, TypeError):
                # Handle cases where response doesn't have get_json() or is not JSON serializable
                print(f"Could not cache response for key: {key}")
                pass  # Don't cache if it's not JSON serializable

            return response
        return wrapper
    return decorator
