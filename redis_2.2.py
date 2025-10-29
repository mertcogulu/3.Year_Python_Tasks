from flask import Flask, request, jsonify
import time

app = Flask(__name__)

cache = {}
CACHE_TIMEOUT = 30


def get_from_cache(key):
    """Return cached value if valid, else None."""
    if key in cache:
        value, timestamp = cache[key]
        if time.time() - timestamp < CACHE_TIMEOUT:
            return value
        else:
            del cache[key]
    return None


def set_in_cache(key, value):
    """Store value in cache with current timestamp."""
    cache[key] = (value, time.time())


def slow_function(x):
    """Simulate a slow computation and return result."""
    cached_result = get_from_cache(x)
    if cached_result is not None:
        print("Returning cached result...")
        return cached_result

    print("Computing new result...")
    time.sleep(6)
    result = {"input": x, "output": x ** 2}

    set_in_cache(x, result)
    return result


@app.route('/')
def home():
    return """
    <h2>Welcome to the Flask Custom Cache Demo!</h2>
    <p>Try visiting: <a href="/compute?x=5">/compute?x=5</a></p>
    <p>This endpoint simulates a slow function and caches the result in memory for 30 seconds.</p>
    """


@app.route('/compute')
def compute():
    x = request.args.get("x", 2, type=int)
    result = slow_function(x)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
