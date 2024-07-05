from app import app

def handler(event, context):
    from flask import request
    from werkzeug.serving import run_simple

    return run_simple('localhost', 5000, app)
