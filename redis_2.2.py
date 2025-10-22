from flask import Flask, request, jsonify
from flask_caching import Cache
import time

app = Flask(__name__)

# Redis config
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_DEFAULT_TIMEOUT'] = 30

cache = Cache(app)


@cache.memoize(timeout=30)
def slow_function(x):
    # Simulate a slow task
    time.sleep(6)
    return {"input": x, "output": x ** 2}


@app.route('/')
def home():
    return """
    <h2>Welcome to the Flask Redis Cache Demo!</h2>
    <p>Try visiting: <a href="/compute?x=5">/compute?x=5</a></p>
    <p>This endpoint simulates a slow function and caches the result in Redis for 30 seconds.</p>
    """


@app.route('/compute')
def compute():
    x = request.args.get("x", 2, type=int)
    return jsonify(slow_function(x))


if __name__ == '__main__':
    app.run(debug=True, port=5001)
