from flask import Flask
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import threading
import requests

sentry_sdk.init(
    dsn="http://6b7be59c74a640338a9daf64308b7853@23.140.40.144:8000/10",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0,
    debug=True
)

app = Flask(__name__)

def send_heartbeat():
    try:
        requests.get("http://23.140.40.144:8000/api/0/organizations/student/heartbeat_check/78666581-c732-4fca-9378-15555c9ef218/")
        print("Heartbeat sent successfully.")
    except Exception as e:
        print("Heartbeat failed:", e)
    threading.Timer(60, send_heartbeat).start()

send_heartbeat()

@app.route('/')
def home():
    return """
    <h2>Flask + GlitchTip Integration </h2>
    <p>Error tracking and heartbeat monitoring are active.</p>
    <p>Test error logging → <a href='/cause_error'>/cause_error</a></p>
    """

@app.route('/cause_error')
def cause_error():
    raise Exception("Test error for GlitchTip integration ")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
