import pymysql
import uuid
import re
from app import app
from validator import Validator
from db_config import mysql
from flask import jsonify
from flask import Flask, request, make_response
from werkzeug import generate_password_hash, check_password_hash

###############################
# To define our token's secret;
###############################
app.config['SECRET_KEY'] = 'HFI_client$.r3porting_APP'



# This route is to test if project works successfully.
# @app.route('/', methods = ['GET'])
# def homepage():
#     resp = jsonify('Hi!')
#     resp.status_code = 200
#     return resp
        
########################
# To define all routers;
########################
@app.route('/signin', methods = ['POST'])
def signin():
    return ''

# Route for sign up the new user with data validation
@app.route('/signup', methods = ['POST'])
def signup():
    try:
        # To connect with MySQL server
        # print('MySQL connecting......')
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
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

        # Give a flag to check the username
        # if flag's status code equals 200, go on checking
        # or it will return flag back as response
        # print('Username checking......')
        flag_is_Username_Valid = Validator.is_Username_Valid(data['user_name'])
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

@app.route('/update/<public_user_ID>')
def update_user(public_user_ID):
    return ''

@app.route('/overview/<public_clientID>')
def get_overview(public_clientID):
    return ''

@app.route('/appeals/<public_clientID>')
def get_appeals(public_clientID):
    return ''

@app.route('/approvals/<public_clientID>')
def get_approvals(public_clientID):
    return ''

@app.route('/closed/<public_clientID>')
def get_closed(public_clientID):
    return ''

@app.route('/closed_new/<public_clientID>')
def get_closed_new(public_clientID):
    return ''

@app.route('/outreach/<public_clientID>')
def get_outreach(public_clientID):
    return ''

@app.route('/outreach_new/<public_clientID>')
def get_outreach_new(public_clientID):
    return ''

@app.route('/pending/<public_clientID>')
def get_pending(public_clientID):
    return ''

@app.route('/referrals/<public_clientID>')
def get_referrals(public_clientID):
    return ''
    # try:
    #     print("Connection begins!")
    #     conn = mysql.connect()
    #     cursor = conn.cursor(pymysql.cursors.DictCursor)
    #     print("Selection query begins!")
    #     cursor.execute("select * from address where LINE1 = '31 Sutherland St.'" )
    #     print("Begin to call procedure!")
    #     args = [49, "wkly"]
    #     results = cursor.callproc("cr_standard_outreach", args)
    #     print(results[0])
    #     rows = cursor.fetchall()
    #     resp = jsonify(rows)
    #     resp.status_code = 200
    #     return resp
    # except Exception as e:
    #     print(e)
    # finally:
    #     cursor.close() 
    #     conn.close()

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
