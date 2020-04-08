from flask import request
from flask_restful import Resource
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
import backend.models as models

class SignUp(Resource):
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    def post(self):
        data = request.get_json()
        response = {}
        status = 200
        hashed_password = models.User.generate_hashed_password(data['password'])
        
        try:
            self.DBHandler.add_user(
                models.User( 
                    data['username'], 
                    hashed_password, 
                    data['first_name'], 
                    data['last_name'], 
                    data['email']
                )
            )
            response = { 
                'msg': 'success',
                'user' : { 
                    'username': data['username']
                } 
            }

        except KeyError:
            response = {'msg': 'Update failed. Json missing keys.'}
            status = 400

        except IntegrityError as e:
            status = 400
            if isinstance(e.orig, UniqueViolation):
                response = {'msg': 'Username is taken.'}
            else:
                response = {'msg': 'Unknown error.'}
        
        return response, status