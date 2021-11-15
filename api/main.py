# # import sqlite3
# import flask
# import json

# app = flask.Flask(__name__)

# def test_case():
#     print("*************")
#     print("Hello, World!")
#     print("*************")

# #Get Del Put to make for this specific webpage (I want to make sure this works before writing the framework for everything else)
# @app.route("/packages/offset=<offset>", methods=['GET','POST'])
# def post_package_offset(): #URL: http://127.0.0.1:8001/packages
#     #Check if there is an offset given (http://127.0.0.1:8001/packages/offset=?)
#     offset = flask.request.args.get('offset')

#     #Just a placeholder for the data that would be returned
#     info = {
#         "Name": "string",
#         "Version": "1.2.3",
#         "ID": "string"
#     }

#     #This is the official response that will be recieved (error code and data)
#     response = app.response_class(
#         response=json.dumps(info),
#         status=201,
#         mimetype='application/json'
#     )
    
#     return response

# @app.route("/packages/", methods=['GET','POST'])
# def post_package(): #URL: http://127.0.0.1:8001/packages
#     #Check if there is an offset given (http://127.0.0.1:8001/packages/)
#     offset = 1
    
#     #Just a placeholder for the data that would be returned
#     info = {
#         "Name": "string",
#         "Version": "1.2.3",
#         "ID": "string"
#     }

#     #This is the official response that will be recieved (error code and data)
#     response = app.response_class(
#         response=json.dumps(info),
#         status=201,
#         mimetype='application/json'
#     )
    
#     return response

# if __name__ == '__main__':
# 	# Start the server on "127.0.0.1:8001"
#     app.run(port=8001, host='127.0.0.1', debug=True, use_evalex=False)
import json
import datetime
import jwt
import pyrebase
from flask import Flask, request
from flask_restful import Api, Resource




config = {
  "apiKey": "AIzaSyAgpUJ9lfto0Qn3WX4T_BO6Hp458yWDB2o",
  "authDomain": "test-ae93d.firebaseapp.com",
  "databaseURL": "https://test-ae93d-default-rtdb.firebaseio.com/",
  "storageBucket": "test-ae93d.appspot.com"
}

firebase = pyrebase.initialize_app(config)
app = Flask(__name__)
# db = firebase.database()
auth = firebase.auth()
api=Api(app)

def test_case():
    print("*************")
    print("Hello, World!")
    print("*************")

#Get Del Put to make for this specific webpage (I want to make sure this works before writing the framework for everything else)
@app.route("/packages/offset=<offset>", methods=['GET','POST'])
def post_package_offset(): #URL: http://127.0.0.1:8001/packages
    #Check if there is an offset given (http://127.0.0.1:8001/packages/offset=?)
    # offset = flask.request.args.get('offset')

    #Just a placeholder for the data that would be returned
    info = {
        "Name": "string",
        "Version": "1.2.3",
        "ID": "string"
    }

    #This is the official response that will be recieved (error code and data)
    response = app.response_class(
        response=json.dumps(info),
        status=201,
        mimetype='application/json'
    )
    return response

@app.route("/packages/", methods=['GET','POST'])
def post_package(): #URL: http://127.0.0.1:8001/packages
    #Check if there is an offset given (http://127.0.0.1:8001/packages/)
    # offset = 1
    #Just a placeholder for the data that would be returned
    info = {
        "Name": "string",
        "Version": "1.2.3",
        "ID": "string"
    }

    #This is the official response that will be recieved (error code and data)
    response = app.response_class(
        response=json.dumps(info),
        status=201,
        mimetype='application/json'
    )
    
    return response

class Authenticate(Resource):
    # @marshal_with(metadata_payload)
    def put(self):
        try:
            data = request.data
            # print(data)
            data = json.loads(data)
            # print(data['User']['name'])
            user_info_dict = data['User']
            user_name = user_info_dict['name']
            is_admin = user_info_dict['isAdmin']
            user_password = data['Secret']['password']
            app.config['SECRET_KEY'] = user_password
        
            token = jwt.encode({'user' : user_name, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=600)}, app.config['SECRET_KEY'])
            # print(token.decode("utf-8"))
            # token = json.loads(token)
            token = token.decode("utf-8")

            # user = auth.sign_in_with_email_and_password(userName, userPassword)
            # token_with_additional_claims = auth.create_custom_token(token, {"isAdmin": isAdmin})

            # Get a reference to the database service
            db = firebase.database()

            # data to save
            data = {"User": {"name": user_name,"isAdmin": is_admin},"Secret": {"password": user_password},"Token": token}
            # token_with_additional_claims = auth.create_custom_token(token, {"isAdmin": isAdmin})

            # Pass the user's idToken to the push method
            db.child("users").child(user_name).set(data)



            # response = app.response_class(
            #     response=token,
            #     status=201,
            #     mimetype='application/json'
            #     )
            return token
        except:
            return None, 400

api.add_resource(Authenticate, "/authenticate")


if __name__ == '__main__':
	# Start the server on "127.0.0.1:8001"
    app.run(port=8001, host='127.0.0.1', debug=True, use_evalex=False)