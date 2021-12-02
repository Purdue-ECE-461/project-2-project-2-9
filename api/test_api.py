import unittest
import main as tasks
import json
import ast

class TestSuite(unittest.TestCase): 
    #We have hardcoded the API responses FOR NOW and we will be testing to
    # ensure that the data responses and types are as expected.
    
    def test_packageRetrieve(self):
        #Testing invalid credentials:
        bad_case = tasks.packageRetrieve(0)
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('Error!  You do not have the permissions to view this item!', response_message)

        return

    def test_updatePackageVersion(self):
        #Testing invalid credentials:
        bad_case = tasks.updatePackageVersion(0)
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('Error!  You do not have the permissions to view this item!', response_message)

        return
    
    def test_deletePackageVersion(self):
        #Testing invalid credentials:
        bad_case = tasks.deletePackageVersion(0)
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('Error!  You do not have the permissions to view this item!', response_message)

        return

    def test_ratePackage(self):
        #Testing invalid credentials:
        bad_case = tasks.ratePackage(0)
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('Error!  You do not have the permissions to view this item!', response_message)

        return

    def test_resetRegistry(self):
        #Testing invalid credentials:
        bad_case = tasks.resetRegistry()
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('You do not have permission to reset the registry.', response_message)

        return

    def test_getPackages(self):
        #Testing invalid credentials:
        bad_case = tasks.getPackages()
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('You do not have permission to view the registry.', response_message)

        return

    def test_createPackage(self):
        #Testing invalid credentials:
        bad_case = tasks.createPackage()
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('You do not have permission to add to the registry.', response_message)

        return
    
    def test_getPackageByName(self):
        #Testing invalid credentials:
        bad_case = tasks.getPackageByName("test")
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('You do not have permission to view the package.', response_message)

        return
    
    def test_deletePackageVersions(self):
        #Testing invalid credentials:
        bad_case = tasks.deletePackageVersions("test")
        status_code = bad_case._status_code
        self.assertEqual(401, status_code)
        response_code = ast.literal_eval(bad_case.response[0].decode("utf-8"))['code']
        self.assertEqual(401, response_code)
        response_message = ast.literal_eval(bad_case.response[0].decode("utf-8"))['message']
        self.assertEqual('You do not have permission to modify the package.', response_message)

        return
    # #NOTE: We are only testing the 'post_package' method.  We do not want to use the offset method as it epects an offset, but functions the same as 'post_package'.
      
    # def test_basicAPI_response(self):
    #     #Testing the API response.
    #     # Expected value: 201 CREATED

    #     status_response = tasks.post_package().status
    #     self.assertEqual("201 CREATED", status_response)

        # with self.subTest(key=201):
        #     status_response = tasks.post_package().status
        #     self.assertEqual(201, status_response)
        
    # def test_basicAPI_mime(self):
    #     #Testing the API mimetype attribute.
    #     # Expected value: "application/json"

    #     mime_response = tasks.post_package().mimetype
    #     self.assertEqual("application/json", mime_response)

    #     # with self.subTest(key="application/json"):
    #     #     mime_response = tasks.post_package().mimetype
    #     #     self.assertEqual("application/json", mime_response)
        
    # def test_basicAPI_data(self):
    #     #Testing the API data attribute.
    #     # Expected values (all string data types):
    #     #   - Name:string
    #     #   - Version:1.2.3
    #     #   - ID:string

    #     data_response = json.loads(tasks.post_package().response[0].decode('utf8').replace("'", '"')) #To convert we need to:
    #     #   (1) Get list element 
    #     #   (2) Convert to string (from bytes) 
    #     #   (3) Convert from JSON string to Dict

    #     self.assertEqual('string', data_response["Name"])
    #     self.assertEqual("1.2.3", data_response["Version"])
    #     self.assertEqual('string', data_response["ID"])
    #     # with self.subTest(key="Name"):
    #     #     self.assertEqual('string', data_response["Name"])
    #     # with self.subTest(key="Version"):
    #     #     self.assertEqual("1.2.3", data_response["Version"])
    #     # with self.subTest(key="ID"):
    #     #     self.assertEqual('string', data_response["ID"])
    #     return

# pytest --cov-report term --cov=. test_api.py --cov-report=html
# or
# pytest test_api.py

from flask import Flask, jsonify
app = Flask(__name__)
def convertJSONFormat(code, data):
    response = app.response_class(
        response=json.dumps(data),
        status=code,
        mimetype='application/json'
    )
    return response

if __name__ == '__main__':
    
    unittest.main()
    exit(0)