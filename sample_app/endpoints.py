import logging
from flask_pymongo import pymongo
from flask import jsonify, request

con_string = "mongodb+srv://lokitha:Sairam@cluster0.jqxhu3y.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('flasktraining')

user_collection = pymongo.collection.Collection(db,'flask')
print("MongoDB connected Successfully")

def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Welcome to Flask Training'
        print("Welcome to Flask Training")
        return res
    
    @endpoints.route('/register-project', methods=['POST'])
    def register_project():
        resp = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)
            print("Project details stored successfully in the database.")
            status = {
                "statusCode" : "200",
                "statusMessage" : "Project details Stored Successfully in the database"
             }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp
    

    @endpoints.route('/read-projects', methods=['GET'])
    def read_projects():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode" : "200",
                "statusMessage" : "User data Stored Successfully in the database"
            }
            output = [{'Project_Name': user['name'],'Team_Lead':user['name'],'Email': user['email']} for user in users]
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp

    @endpoints.route('/update-projects', methods=['PUT'])
    def update_projects():
        resp = {}
        try:
            req_body = request.json
            user_collection.update_one({"id":req_body['id']},{"$set":req_body['updated_user_body']})
            print("Project detail updated successfully in the database")
            status = {
            "statusCode" : "200",
            "statusMessage" : "Project detail Updated Successfully in the database"
             }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp


    @endpoints.route('/delete', methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
            "statusCode" : "200",
            "statusMessage" : "Project detail Deleted Successfully in the database"
             }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp
    return endpoints

    
