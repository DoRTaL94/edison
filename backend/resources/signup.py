from flask import request
from flask_restful import Resource
from models.user import User

class SignUp(Resource):
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    def post(self):
        data = request.get_json()
        response = {}
        status = 200
        hashed_password = User.generate_hashed_password(data['password'])
        
        try:
            self.DBHandler.add_user(
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

        except ValueError as e:
            response = { 'message': str(e) }
            status = 400
        
        return response, status