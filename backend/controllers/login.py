from flask_restful import Resource
from flask import request
from services.dbhandler import DBHandler
from models.user import User
from flask_jwt_extended import (create_access_token, create_refresh_token)

class LoginController(Resource):
    def post(self):
        data = request.get_json()
        current_user = DBHandler.get_user_by_username(data['username'])
        status = 200
        response = {}

        if not current_user:
            response = {'message': 'Username or password is incorrect'}
            status = 401

        else:
            if User.verify_password(data['password'], current_user.password):
                access_token = create_access_token(identity = data['username'])
                refresh_token = create_refresh_token(identity = data['username'])

                response = {
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            else:
                response = {'message': 'Username or password is incorrect'}
                status = 401
        
        return response, status