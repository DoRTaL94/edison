from flask import request
from flask_restful import Resource
from models.user import User
from services.dbhandler import DBHandler

class SignUpController(Resource):
    def post(self):
        data = request.get_json()
        response = {}
        status = 200
        hashed_password = User.generate_hashed_password(data['password'])
        
        try:
            DBHandler.add_user(
                User(0, 
                    data['username'], 
                    hashed_password, 
                    data['firstname'], 
                    data['lastname'], 
                    data['email']
                )
            )
            response = { 
                'message': 'success',
                'user' : { 
                    'username': data['username']
                } 
            }

        except KeyError:
            response = {'message': 'Update failed. Json missing keys.'}
            status = 400
        
        return response, status