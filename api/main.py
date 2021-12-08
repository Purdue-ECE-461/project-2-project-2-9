import json
import datetime
import jwt
import pyrebase

from flask import Flask, jsonify
from flask_restful import Api, Resource, request
from google.cloud import firestore

import main_rate as rate

# config = {
#   "apiKey": "AIzaSyAgpUJ9lfto0Qn3WX4T_BO6Hp458yWDB2o",
#   "authDomain": "test-ae93d.firebaseapp.com",
#   "databaseURL": "https://test-ae93d-default-rtdb.firebaseio.com/",
#   "storageBucket": "test-ae93d.appspot.com"
# }

config = {
  "apiKey": API_KEY,
  "authDomain": "lexical-botany-331616.firebaseapp.com",
  "databaseURL": "https://lexical-botany-331616-default-rtdb.firebaseio.com/",
  "storageBucket": "lexical-botany-331616.appspot.com"
}

firebase = pyrebase.initialize_app(config)
app = Flask(__name__)
# db = firebase.database()
auth = firebase.auth()
api=Api(app)

"""
Begin helper functions:
"""

def convertJSONFormat(code, data):
    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

def checkAuth():
    #Get & process authentification
    auth_token = request.headers.get('X-Authorization').split()[1]

    try:
        #Check permissions:
        #   1. Search db of Users with auth_token as filter:
        db = firebase.database()
        auth_validation = db.child("User").order_by_child("Token").equal_to(auth_token)
        #   2. Get results & return if the query yields any Users
        return len(list(auth_validation.fetch()))
    except Exception:
        return 0

"""
/package/<id> URLS:
"""
@app.route("/package/<id>", methods=['GET'])
def packageRetrieve(id):
    request.get_data()    

    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'Error!  You do not have the permissions to view this item!'})

    db = firebase.database()
    
    try:
        results = db.child("package").order_by_child("ID").equal_to(id).get()
        if(list(results) != []):
            #Query for package by ID
            pack = results.get(results.key('package', id))

            api_response = {
                'metadata': {
                        'Name': pack['Name'],
                        'Version': pack['Version'],
                        'ID': pack['ID']
                    },
                    'data': {
                        'Content': pack['Content'],
                        'URL': pack['URL'],
                        'JSProgram': pack['JSProgram']
                    }   
                }
            return convertJSONFormat(200, api_response)
    except Exception:
        pass

    return convertJSONFormat(400, {'code': 400, 'message': 'Error! Something went wrong when processing your request!  Please ensure that your request was made properly!'})

@app.route("/package/<id>", methods=['PUT'])
def updatePackageVersion(id):
    request.get_data()

    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'Error!  You do not have the permissions to view this item!'})

    #Load Request Body as JSON:
    req_body = json.loads(request.data.decode('utf-8'))

    #Parse Data as metadata and data:
    try:
        metadata = req_body['metadata']
        data = req_body['data']
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Malformed request (e.g. no such package).'})
    
    db = firebase.database()

    #Check that Metadata matches URL
    try:
        if(id == req_body['ID']):
            #Select from database to make sure package exists:
            search = db.child("package")
            #Add filters for name...
            search.order_by_child("Name").equal_to(metadata["Name"])
            #...and version (specified as a unique identifier pair)
            search.order_by_child("Version").equal_to(metadata["Version"])

            if(list(search.get()) != []): #If this is a valid (existing) identifier pair:
                #Get most recent package:
                former_version = search
                former_version.order_by_child("package").equal_to(id).get()
                #Remove most recent package:
                former_version.remove()

                #Update with newest version with metadata and data info:
                package_payload = {
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
                }

                #Add to database:
                db.child("package").set(package_payload)
                return convertJSONFormat(200, {'code': 200, 'Payload': package_payload})
    except Exception:
        pass

    return convertJSONFormat(400, {'code' : 400, 'message': 'Malformed request (e.g. no such package).'})

@app.route("/package/<id>", methods=['DEL'])
def deletePackageVersion(id):
    request.get_data()
    
    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'Error!  You do not have the permissions to delete this item!'})
    
    db = firebase.database()

    try:
        #Query packages to find package {id}
        results = db.child("package").order_by_child("ID").equal_to(id)
        if(list(results.get()) != []):
            #Delete package by ID:
            results.remove()
            return convertJSONFormat(200, {'code': 200, 'message': 'Package is deleted.'})
    except Exception:
        pass

    return convertJSONFormat(400, {'code': 400, 'message':'No such package.'})

@app.route("/package/<id>/rate", methods=['GET'])
def ratePackage(id):
    request.get_data()

    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'Error!  You do not have the permissions to view this item!'})

    db = firebase.database()

    results = db.child("package").order_by_child("ID").equal_to(id)

    try:
        if(list(results.get()) != []):
            #Query database for package by ID
            pack = results.get()
            try:
                netScore, rampUpScore, correctnessScore, busFactorScore, responsiveMaintainerScore, licenseScore, dependencyScore = rate.call_main(pack['URL'])

                api_response = {{
                'BusFactor': busFactorScore,
                'Correctness': correctnessScore,
                'RampUp': rampUpScore,
                'ResponsiveMaintainer': responsiveMaintainerScore,
                'LicenseScore': licenseScore,
                'GoodPinningPractice': dependencyScore
                }}


            except Exception:
                return convertJSONFormat(500, {'code': 500, 'message': "The package rating system choked on at least one of the metrics."})
            return convertJSONFormat(200, api_response)
    except Exception:
        pass

    return convertJSONFormat(400, {'code': 400, 'message': 'No such package.'})
    
"""
/reset URL:
"""
@app.route("/reset", methods=['DEL'])
def resetRegistry():
    request.get_data()
    
    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'You do not have permission to reset the registry.'})

    db = firebase.database()
    #Query for all packages:
    packages = db.child("package")

    try:
        packages.remove
        return convertJSONFormat(200, {'code': 200, 'message': 'Registry is reset.'})
    except Exception:
        return convertJSONFormat(401, {'code': 401, 'message': 'Something went wrong when trying to reset the registry!'})

"""
/packages URLS:
"""
@app.route("/packages", methods=['POST'])
def getPackages():
    request.get_data()

    offset = 1
    try:
        offset = request.args.get('offset')
    except Exception:
        pass

    offset *= 10

    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'You do not have permission to view the registry.'})

    try:
        db = firebase.database()
        #Query for all packages:
        packages = db.child("package").get()

        response = []

        for i in packages:
            offset -= 1
            if offset >= 0:
                response.append({
                'id': i['id'],        
                'name': i['name'],        
                'tag': i['tag']
                })
        return convertJSONFormat(200, response)
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Error! Something went wrong when processing your request!'})

"""
/package URL:
"""
@app.route("/package", methods=['POST'])
def createPackage():
    request.get_data()
    
    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'You do not have permission to add to the registry.'})
    
    #Load Request Body as JSON:
    req_body = json.loads(request.data.decode('utf-8'))

    #Parse Data as metadata and data:
    try:
        metadata = req_body['metadata']
        data = req_body['data']
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Malformed request.'})
    
    db = firebase.database()
    try:
        #Check if package exists:
        if list(db.child("package").order_by_child("ID").equal_to(metadata["id"].get())):
            return convertJSONFormat(403, {'code': 403, 'message': 'Package exists already.'})

        data = {'Name': metadata['Name'], 'Version': metadata['Version'], 'ID': metadata['ID']}
        db.set(data)
        
        return convertJSONFormat(201, data)
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Something went wrong when trying to add a package.'})

"""
/package/byName/<name> URLS:
"""
@app.route("/package/byName/<name>", methods=['GET'])
def getPackageByName(name):
    request.get_data()
    
    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'You do not have permission to view the package.'})

    db = firebase.database()

    try:
        #Query for all packages:
        packages = db.child("package").order_by_child("Name").equal_to(name).get()

        if(list(packages)==[]):
            return convertJSONFormat(400, {'code': 400, 'message': 'No such package.'})

        data = { 
            'id': packages['id'],
            'name': name,
            'tag': packages['tag']
        }
        return convertJSONFormat(200, data)
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Error in retrieving package.'})
    

@app.route("/package/byName/<name>", methods=['DEL'])
def deletePackageVersions(name):
    request.get_data()
    
    if(checkAuth() == 0): 
        return convertJSONFormat(401, {'code': 401, 'message': 'You do not have permission to modify the package.'})

    db = firebase.database()

    #Query for all packages:
    try:
        packages = db.child("package").order_by_child("Name").equal_to(name)
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Error in retrieving package for deletion.'})

    if(list(packages.get())==[]):
        return convertJSONFormat(400, {'code': 400, 'message': 'No such package.'})

    try:
        packages.remove()
        return convertJSONFormat(200, {'code': 200, 'message': 'Package is deleted.'})
    except Exception:
        return convertJSONFormat(400, {'code': 400, 'message': 'Error in deleting package.'})
    

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
