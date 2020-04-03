from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required
from models.user import User
from services.dbhandler import DBHandler

class SignUpController(Resource):
    def post(self):
        data = request.get_json()

        try:
            DBHandler.add_user(
                User(0, 
                    data['username'], 
                    data['password'], 
                    data['firstname'], 
                    data['lastname'], 
                    data['email']
                )
            )
        except KeyError:
            return {
                'message': 'Update failed. Json missing keys.'
            }
            
        return { 
            'message': 'success',
            'user' : { 
                'username': data['username']
            } 
        }