import unittest
import main as tasks
import json

class TestSuite(unittest.TestCase): 
    #We have hardcoded the API responses FOR NOW and we will be testing to
    # ensure that the data responses and types are as expected.

    #NOTE: We are only testing the 'post_package' method.  We do not want to use the offset method as it epects an offset, but functions the same as 'post_package'.
      
    # def test_basicAPI_response(self):
    #     #Testing the API response.
    #     # Expected value: 201 CREATED

    #     status_response = tasks.post_package().status
    #     self.assertEqual("201 CREATED", status_response)

    #     # with self.subTest(key=201):
    #     #     status_response = tasks.post_package().status
    #     #     self.assertEqual(201, status_response)
        
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

if __name__ == '__main__':


    unittest.main()
    exit(0)