from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
import backend.models as models

class User(Resource):
    
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    @jwt_required
    def get(self, username):
        user = self.DBHandler.get_user_by_username(username)
        status = 200 if user else 404
        response = { 
            username: models.ResponseUser(user).__dict__ 
        } if user else { 'msg': 'User not found' }

        return response, status

    @jwt_required
    def delete(self, username):
        response = {'msg': 'User deleted'}
        status = 200
        
        if get_jwt_identity() == username:
            self.DBHandler.delete_user_by_username(username)
        else:
            response = {'msg': 'User can delete himself but no other users'}
            status = 403

        return response, status
    
    @jwt_required
    def put(self, username):
        response = {}
        status = 200

        if(get_jwt_identity() == username):
            data = request.get_json()
            
            try:
                user_to_update = models.User(
                    data['username'],
                    data['password'],
                    data['firstname'],
                    data['lastname'],
                    data['email']
                )
                user = self.DBHandler.update_user(username, user_to_update)
                response = {'msg': 'User updated', 'user': user.__dict__}
                
            except KeyError:
                response = {'msg': 'Update failed. Json missing keys.'}
                status = 400
        else:
            response = {'msg': 'User can update himself but no other users'}

        return response, status