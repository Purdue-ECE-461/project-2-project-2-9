import sqlite3
import flask
import json

app = flask.Flask(__name__)

#Get Del Put to make for this specific webpage (I want to make sure this works before writing the framework for everything else)
@app.route("/packages/offset=<offset>", methods=['POST'])
def post_package_offset(): #URL: http://127.0.0.1:8001/packages
    #Check if there is an offset given (http://127.0.0.1:8001/packages/offset=?)
    offset = flask.request.args.get('offset')

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
    offset = 1
    
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

if __name__ == '__main__':
	# Start the server on "127.0.0.1:8001"
    app.run(port=8001, host='127.0.0.1', debug=True, use_evalex=False)