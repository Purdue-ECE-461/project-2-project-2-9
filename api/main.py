import json
import datetime
import jwt
import pyrebase

from flask import Flask, request
from flask_restful import Api, Resource

from google.cloud import datastore as GCP

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

#Get Del Put to make for this specific webpage (I want to make sure this works before writing the framework for everything else)
# @app.route("/packages/offset=<offset>", methods=['GET','POST'])
# def post_package_offset(): #URL: http://127.0.0.1:8001/packages
#     #Check if there is an offset given (http://127.0.0.1:8001/packages/offset=?)
#     # offset = flask.request.args.get('offset')

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
#     # offset = 1
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

"""
/packages URLS:
"""
@app.route("/packages", methods=['GET'])
def getPackages():
   return

"""
/package/<id> URLS:
"""
@app.route("/package/<id>", methods=['GET'])
def packageRetrieve(id):
    return

@app.route("/package/<id>", methods=['PUT'])
def updatePackageVersion(id):
    #Get & process authentification
    auth_token = request.headers.get('X-Authorization').split()[1]

    #Check permissions:
    #   1. Search db of Users with auth_token as filter:
    auth_validation = GCP.Client().query(kind='User').addfilter('Token', '=', auth_token)
    #   2. Get results & check if the query yields any Users
    if(len(list(auth_validation.fetch())) == 0): 
        return {'code': 401, 'message': 'Error!  You do not have the permissions to view this item!'}

    #Load Request Body as JSON:
    req_body = json.loads(request.data.decode('utf-8'))

    #Parse Data as metadata and data:
    try:
        metadata = req_body['metadata']
        data = req_body['data']
    except Exception:
        return {'code': 400, 'message': 'Error! Something went wrong when parsing your request!\nAre you sure your request was formatted correctly?'}
    
    #Check that Metadata matches URL
    if(id == req_body['ID']):
        #Select from database to make sure package exists:
        search =  GCP.Client().query(kind='package')
        #Add filters for name and version (specified as a unique identifier pair)
        search.add_filter('Name', '=', metadata['Name']).add_filter('Version', '=', metadata['Version'])
        if(len(list(search.fetch())) != 0): #Valid identifier pair:
            #Hide most recent package:
            former_version = GCP.get(GCP.key('package', id))
            package_payload = GCP.Entity(former_version, exclude_from_indexes=['Content'])

            #Update with newest version with metadata and data info:
            package_payload.update({
                'metadata':{
                    'Name': metadata['Name'],
                    'Version': metadata['Version'],
                    'ID': metadata['ID']
                },
                'data':{
                    'Content': data['Content'],
                    'URL': data['URL'],
                    'JSProgram': data['JSProgram']
                }
            })

            GCP.put(package_payload)
            return {'code': 200, 'Payload': package_payload}

    return {'code' : 400, 'message': 'Error! Something went wrong when parsing your request!\nPlease check to make sure your request was formatted correctly!'}

@app.route("/package/<id>", methods=['DEL'])
def deletePackageVersion(id):
    return

@app.route("/package/<id>/rate", methods=['GET'])
def ratePackage(id):
    return

"""
/reset URL:
"""
@app.route("/reset", methods=['DEL'])
def resetRegistry():
    return

"""
/package URL:
"""
@app.route("/package", methods=['POST'])
def createPackage():
    return

"""
/package/byName/<name> URLS:
"""
@app.route("/package/byName/<name>", methods=['GET'])
def getPackageByName(name):
    return

@app.route("/package/byName/<name>", methods=['DEL'])
def deletePackageVersions(name):

    return


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