from app import app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

def handler(event, context):
    return run_simple('0.0.0.0', 5000, app)
