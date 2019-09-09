import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import Flask, request, make_response
from werkzeug import generate_password_hash, check_password_hash

@app.route('signin', methods = ['POST'])
def signin():
    return ''

@app.route('signin', methods = ['POST'])
def signin():
    return ''

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
        
# flask run --cert=adhoc
if __name__ == "__main__":
    app.run(debug = True, ssl_context = 'adhoc')



