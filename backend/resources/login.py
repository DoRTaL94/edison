from flask_restful import Resource
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token)
import backend.models as models

class Login(Resource):
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    def post(self):
        data = request.get_json()
        current_user = self.DBHandler.get_user_by_username(data['username'])
        status = 200
        response = {}

        if not current_user:
            response = {'msg': 'Username or password is incorrect'}
            status = 401

        else:
            if models.User.verify_password(data['password'], current_user.password):
                access_token = create_access_token(identity = data['username'])
                refresh_token = create_refresh_token(identity = data['username'])

                response = {
                    'msg': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            else:
                response = {'msg': 'Username or password is incorrect'}
                status = 401
        
        return response, status