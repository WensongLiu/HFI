import re
import pymysql
from db_config import mysql
from flask import jsonify

# This class is used to check if the requeest data are valid for signin and signup functions.
class Validator():
    # function for user name(email address) data validation
    def is_Username_Valid(user_name):
        # if user name encludes 2 or more '@' or any space
        # will give a 400 bad request response
        # or user name's format is correct, so go on checking
        if not re.match(r'[^@^\s]+@[^@^\s]+\.[^@^\s]+', user_name):
            resp = jsonify('Illegal characters in your User Name!')
            resp.status_code = 400
            return resp
        # To check if there is an existed account with this user name in database
        # if so, give a 405 Method not allowed response back
        # if not, user name is clear
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM users where user_name=%s', (user_name,))
        conn.commit()
        rows = cursor.fetchall()
        if(len(rows) != 0):
            resp = jsonify('User already existed!')
            resp.status_code = 405
            return resp
        else:
            resp = jsonify('')
            resp.status_code = 200
            return resp

    # function for password data validation
    def is_Password_Valid(password):
        # To check the password's length, it should be in 6-20
        # or will give a bad request response back
        if(len(password) < 6):
            resp = jsonify('Password is too short!')
            resp.status_code = 400
            return resp
        elif(len(password) > 20):
            resp = jsonify('Password is too long!')
            resp.status_code = 400
            return resp

        # To check the password's strength
        # it must contain at least 1 number, 1 uppercase, 1 lowercase and 1 special character
        regex_special_characters = re.compile('[,.@_!#$%^&*()<>?/\|}{~:]')
        regex_uppercase_characters = re.compile('[A-Z]')
        regex_lowercase_characters = re.compile('[a-z]')
        regex_numbers = re.compile('[0-9]')
        if(regex_special_characters.search(password) == None):
            resp = jsonify('Password must include 1 or more special character!')
            resp.status_code = 400
            return resp
        elif(regex_uppercase_characters.search(password) == None):
            resp = jsonify('Password must include 1 or more uppercase character!')
            resp.status_code = 400
            return resp
        elif(regex_lowercase_characters.search(password) == None):
            resp = jsonify('Password must include 1 or more lowercase character!')
            resp.status_code = 400
            return resp
        elif(regex_numbers.search(password) == None):
            resp = jsonify('Password must include 1 or more number!')
            resp.status_code = 400
            return resp
        else:
            resp = jsonify('')
            resp.status_code = 200
            return resp

