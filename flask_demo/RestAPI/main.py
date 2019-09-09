import pymysql
import uuid
from app import app
from db_config import mysql
from flask import jsonify
from flask import Flask, request, make_response
from werkzeug import generate_password_hash, check_password_hash

###############################
# To define our token's secret;
###############################
app.config['SECRET_KEY'] = 'HFI_client$.r3porting_APP'



# This route is to test if project works successfully.
@app.route('/', methods = ['GET'])
def homepage():
    resp = jsonify('Hi!')
    resp.status_code = 200
    return resp
        
########################
# To define all routers;
########################
@app.route('/signin', methods = ['POST'])
def signin():
    return ''

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        # To connect with MySQL server
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # To get json data from web request
        data = request.get_json()
        # **********************         Give corrent status codes        **********************
        # ********************** Maybe can add more data validations here(username) **********************
        if data['client_ID'] and data['user_name'] and data['user_password'] and data['password_confirmation']:
            flag_is_Username_Valid = is_Username_Valid(data['user_name'])
            flag_is_Password_Valid = is_Password_Valid(data['user_password'])
            if(flag_isPwdValid.status_code == 200):
                if(data['user_password'] == data['password_confirmation']):
                    cursor.execute('SELECT * FROM users where user_name=%s', (data['user_name'],))
                    conn.commit()
                    rows = cursor.fetchall()
                    if(len(rows) != 0):
                        resp = jsonify('User already existed!')
                        resp.status_code = 300
                        return resp
                    else:
                        # To encode the client_ID and password by using hash function
                        hash_client_ID = generate_password_hash(data['client_ID'], method = 'sha256')
                        hash_password = generate_password_hash(data['user_password'], method = 'sha256')
                        MySQL_query = 'INSERT INTO users (public_user_ID, user_name, user_password, client_ID, public_client_ID) values (%s, %s, %s, %s, %s)'
                        MySQL_data = (str(uuid.uuid4()), data['user_name'], hash_password, data['client_ID'], hash_client_ID,)
                        cursor.execute(MySQL_query, MySQL_data)
                        conn.commit()
                        resp = jsonify('User has been created successfully!')
                        resp.status_code = 200
                        return resp
                else:
                    resp = jsonify('Password and confirmation password are not same, please try again!')
                    resp.status_code = 300
                    return resp
            else:
                return flag_isPwdValid
        else:
            resp = jsonify('Some fields of signup data are missing, please retry!')
            resp.status_code = 300
            return resp
    except Exception as e:
        resp = jsonify(str(e))
        resp.status_code = 300
        return resp
    finally:
        cursor.close() 
        conn.close()

def is_Password_Valid(password):
    # check if exisets a A a 1 and .
    # check if exists some illegal characters
    print('Checking pwd')
    if(len(pwd) < 6):
        resp = jsonify('Password is too short!')
        resp.status_code = 300
        return resp
    elif(len(pwd) > 20):
        resp = jsonify('Password is too long!')
        resp.status_code = 300
        return resp
    else:
        resp = jsonify('')
        resp.status_code = 200
        return resp

def is_Username_Valid(user_name):
    return resp

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
