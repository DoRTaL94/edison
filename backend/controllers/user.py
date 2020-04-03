from flask_restful import Resource
from flask_jwt import jwt_required, current_identity
from flask import jsonify, request
from services.dbhandler import DBHandler
from models.response_user import ResponseUser
from models.user import User

class UserController(Resource):
    @jwt_required()
    def get(self, username):
        user = DBHandler.get_user_by_username(username)
        status = 200 if user else 404
        response = { 
            username: ResponseUser(user).__dict__ 
        } if user else { 'message': 'User not found' }

        return response, status

    @jwt_required()
    def delete(self, username):
        response = {'message': 'User deleted'}
        status = 200
        
        if current_identity.username == username:
            DBHandler.delete_user_by_username(username)
        else:
            response = {'message': 'User can delete himself but no other users'}
            status = 403

        return response, status
    
    @jwt_required()
    def put(self, username):
        response = {}
        status = 200

        if(current_identity.username == username):
            data = request.get_json()
            
            try:
                user_to_update = User(
                    0, 
                    data['username'],
                    data['password'],
                    data['firstname'],
                    data['lastname'],
                    data['email']
                )
                user = DBHandler.update_user(username, user_to_update)
                response = {'message': 'User updated', 'user': user.__dict__}
                
            except KeyError:
                response = {'message': 'Update failed. Json missing keys.'}
                status = 400
        else:
            response = {'message': 'User can update himself but no other users'}

        return response, status