import pymysql
import uuid
import re
import jwt
import datetime
import json
from app import app
from validator import Validator
from user import User
from db_config import mysql
from flask import jsonify
from flask import Flask, request, make_response
from werkzeug import generate_password_hash
from functools import wraps

###############################
# To define our token's secret;
###############################
app.config['SECRET_KEY'] = 'demo4_HFI_client$.r3porting_APP'

# This route is to test if project works successfully.
# @app.route('/', methods = ['GET'])
# def homepage():
#     resp = jsonify('Hi!')
#     resp.status_code = 200
#     return resp
        
########################
# To define all routers;
########################
def toker_validation(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # To check if there is a valided token in the request header
        # if not, return a 401 response back
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify('Token is missing!'), 401
        # Then try to decode the token with secret key
        # if cant decode successfully, return token is invalid back
        # if success, get this user info by it's public_user_ID from the request payload
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            # To connect with MySQL server
            # print('MySQL connecting......')
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            # TO search this user by using it's public_user_ID
            cursor.execute('SELECT * FROM users where public_user_ID=%s', (data['Public User ID'],))
            conn.commit()
            rows = cursor.fetchall()
            # get all iofo we need in the feture to create a User instance fot current login user
            _public_user_ID = rows[0]['public_user_ID']
            _user_name = rows[0]['user_name']
            _public_client_ID = rows[0]['public_client_ID']
            if(rows[0]['admin'] == 1):
                _admin = True
            else:
                _admin = False
            current_user = User(_public_user_ID, _user_name, _public_client_ID, _admin)
        except:
            return jsonify('Token is invalid!'), 401
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/signup', methods = ['POST'])
@toker_validation
def signup(current_user):
    # Using this current login use's info to check if he/she is an admin user
    # if not, so this client user can only access methods for client users
    # if so, this admin user can access all methods
    if current_user.admin is False:
        return jsonify("This method isn't available for current user!"), 401
    try:
        # To get json data from web request
        data = request.get_json()
        # To check if there are filled data for signup
        # if there are one or more data fields are missing
        # will return a 400 response, or go on checking
        # print('Data checking......')
        if not (data['client_ID'] and data['user_name'] and data['user_password'] and data['password_confirmation']):
            resp = jsonify('Some fields of signup data are missing, please retry!')
            resp.status_code = 400
            return resp
        # To connect with MySQL server
        # print('MySQL connecting......')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # Give a flag to check the username
        # if flag's status code equals 200, go on checking
        # or it will return flag back as response
        # print('Username checking......')
        flag_is_Username_Valid = Validator.is_Username_Valid(data['user_name'], conn, cursor)
        # print(flag_is_Username_Valid)
        if(flag_is_Username_Valid.status_code != 200):
            return flag_is_Username_Valid
        # Give a flag to check the password
        # if flag's status code equals 200, go on checking
        # or it will return flag back as response
        # print('Password checking......')
        flag_is_Password_Valid = Validator.is_Password_Valid(data['user_password'])
        if(flag_is_Password_Valid.status_code != 200):
            return flag_is_Password_Valid
        # To check if password and the confirmation password are equal
        # if not, return a bad response 
        # or all check done, go on creating this new user
        # print('Password double checking......')
        if(data['user_password'] != data['password_confirmation']):
            resp = jsonify('Password and confirmation password are not same, please try again!')
            resp.status_code = 400
            return resp
        else:
            # To create new user in database
            # if success, give a 201 created response back
            # print('New user creating......')
            # To encode the client_ID and password by using hash function
            hash_client_ID = generate_password_hash(data['client_ID'], method = 'sha256')
            hash_password = generate_password_hash(data['user_password'], method = 'sha256')
            # query need to be executed
            MySQL_query = 'INSERT INTO users (public_user_ID, user_name, user_password, client_ID, public_client_ID) values (%s, %s, %s, %s, %s)'
            # corresponding parameters for this query
            MySQL_data = (str(uuid.uuid4()), data['user_name'], hash_password, data['client_ID'], hash_client_ID,)
            cursor.execute(MySQL_query, MySQL_data)
            conn.commit()
            resp = jsonify('User has been created successfully!')
            resp.status_code = 201
            return resp
    # handle and print out the exceptions
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp
    # close the database connection
    finally:
        cursor.close()
        conn.close()

@app.route('/users', methods = ['GET'])
@toker_validation
def get_all_users(current_user):
    # Using this current login use's info to check if he/she is an admin user
    # if not, so this client user can only access methods for client users
    # if so, this admin user can access all methods
    if current_user.admin is False:
        return jsonify("This method isn't available for current user!"), 401
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # print('Select all users query begins.....')
        cursor.execute('SELECT * FROM users')
        conn.commit()
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp
    # close the database connection
    finally:
        cursor.close()
        conn.close()


@app.route('/signin', methods = ['POST'])
def signin():
    # To connect with MySQL server
    print('MySQL connecting......')
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        # To get json data from web request
        print('Data catching......')
        data = request.get_json()
        if not (data['user_name'] and data['user_password']):
            resp = jsonify('These 2 fields are all required, please try again!')
            resp.status_code = 400
            return resp
        
        # To call validator to check signin info is valid
        print('Checking user name and password.....')
        print(data['user_name'])
        flag_is_Signin_Valid = Validator.is_Signin_Valid(data['user_name'], data['user_password'], conn, cursor)
        if((not isinstance(flag_is_Signin_Valid, str)) and flag_is_Signin_Valid.status_code != 200):
            return flag_is_Signin_Valid
        else:
            print('Token creating.........')
            token = jwt.encode({'Public User ID' : flag_is_Signin_Valid, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 1)}, app.config['SECRET_KEY'])
            resp = jsonify({'token' : token.decode('UTF-8')})
            resp.status_code = 200
            return resp
        # else:
        #     client_token = jwt.encode({'Public User ID' : flag_is_Signin_Valid[1], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY_CLIENT'])
        #     resp = jsonify({'token' : client_token.decode('UTF-8')})
        #     resp.status_code = 209
        #     print('client')
        #     return resp
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp
    # close the database connection
    finally:
        cursor.close()
        conn.close()

@app.route('/update/<public_user_ID>', methods = ['PUT'])
@toker_validation
def update_user(current_user, public_user_ID):
    # Using this current login use's info to check if he/she is an admin user
    # if not, so this client user can only access methods for client users
    # if so, this admin user can access all methods
    if current_user.admin is False:
        return jsonify("This method isn't available for current user!"), 401
    try:
        # To connect with MySQL server
        # print('MySQL connecting......')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # print('Select query begins.....')
        cursor.execute('SELECT * FROM users where public_user_ID=%s', (public_user_ID,))
        conn.commit()
        rows = cursor.fetchall()
        if(len(rows) == 0):
            resp = jsonify('User does not exist!')
            resp.status_code = 400
            return resp
        else:
            # print('Update query begins.......')
            cursor.execute('UPDATE users SET admin=1 WHERE public_user_ID=%s', (public_user_ID,))
            conn.commit()
            resp = jsonify('User selected has been updated as an administrator!')
            resp.status_code = 200
            return resp
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp
    # close the database connection
    finally:
        cursor.close()
        conn.close()

@app.route('/delete/<public_user_ID>', methods = ['DELETE'])
@toker_validation
def delete_user(current_user, public_user_ID):
    # Using this current login use's info to check if he/she is an admin user
    # if not, so this client user can only access methods for client users
    # if so, this admin user can access all methods
    if current_user.admin is False:
        return jsonify("This method isn't available for current user!"), 401
    try:
        # To connect with MySQL server
        # print('MySQL connecting......')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # print('Select query begins.......')
        cursor.execute('SELECT * FROM users where public_user_ID=%s', (public_user_ID,))
        conn.commit()
        rows = cursor.fetchall()
        if(len(rows) == 0):
            resp = jsonify('User does not exist!')
            resp.status_code = 400
            return resp
        else:
            # print('Delete query begins.......')
            cursor.execute('DELETE FROM users WHERE public_user_ID=%s', (public_user_ID,))
            conn.commit()
            resp = jsonify('User selected has been deleted!')
            resp.status_code = 200
            return resp
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 400
        return resp
    # close the database connection
    finally:
        cursor.close()
        conn.close()    

@app.route('/overview/<public_clientID>')
@toker_validation
def get_overview(current_user, public_clientID):
    return ''

@app.route('/appeals/<public_clientID>')
@toker_validation
def get_appeals(current_user, public_clientID):
    return ''

@app.route('/approvals/<public_clientID>')
@toker_validation
def get_approvals(current_user, public_clientID):
    return ''

@app.route('/closed/<public_clientID>')
@toker_validation
def get_closed(current_user, public_clientID):
    return ''

@app.route('/closed_new/<public_clientID>')
@toker_validation
def get_closed_new(current_user, public_clientID):
    return ''

@app.route('/outreach/<public_clientID>')
@toker_validation
def get_outreach(current_user, public_clientID):
    return ''

@app.route('/outreach_new/<public_clientID>')
@toker_validation
def get_outreach_new(current_user, public_clientID):
    return ''

@app.route('/pending/<public_clientID>')
@toker_validation
def get_pending(current_user, public_clientID):
    return ''

@app.route('/referrals/<public_clientID>')
@toker_validation
def get_referrals(current_user, public_clientID):
    return ''

#######################################################
# To handle all errors we will encounter in the future; 
#######################################################
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
        
if __name__ == '__main__':
    app.run(debug = True)
