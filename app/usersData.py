

from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import imp



helper_module = imp.load_source('*', './app/helpers.py')


db = client.restfulapi

collection = db.users

@app.route("/")
def get_initial_response():
    
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    
    resp = jsonify(message)
    
    return resp


@app.route("/api/v1/users", methods=['POST'])
def create_user():
   
    try:
        
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            
            
            return "", 400

        record_created = collection.insert(body)

        
        if isinstance(record_created, list):
            
            return jsonify([str(v) for v in record_created]), 201
        else:
            
            return jsonify(str(record_created)), 201
    except:
        
        
        return "", 500


@app.route("/api/v1/users", methods=['GET'])
def fetch_users():
    
       
    try:
        
        query_params = helper_module.parse_query_params(request.query_string)
        
        if query_params:

            
            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            
            records_fetched = collection.find(query)

            
            if records_fetched.count() > 0:
                
                return dumps(records_fetched)
            else:
                
                return "", 404

        
        else:
            
            if collection.find().count > 0:
                
                return dumps(collection.find())
            else:
                
                return jsonify([])
    except:
        
        
        return "", 500


@app.route("/api/v1/users/<user_id>", methods=['POST'])
def update_user(user_id):
    
       
       
    try:
        
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            
            
            return "", 400

        
        records_updated = collection.update_one({"id": int(user_id)}, body)

        
        if records_updated.modified_count > 0:
            
            return "", 200
        else:
            
            
            return "", 404
    except:
        
        
        return "", 500


@app.route("/api/v1/users/<user_id>", methods=['DELETE'])
def remove_user(user_id):
    
    try:
        
        delete_user = collection.delete_one({"id": int(user_id)})

        if delete_user.deleted_count > 0 :
            
            return "", 204
        else:
            
            return "", 404
    except:
        
        
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
