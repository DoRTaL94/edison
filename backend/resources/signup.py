from flask_restful import Resource, reqparse
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
import backend.models as models
from passlib.hash import pbkdf2_sha256 as sha256

class SignUp(Resource):
        # RequestParser enforces arguments in requests. 
    # If one of the arguments not exists, client gets an error response.
    parser = reqparse.RequestParser()
    parser.add_argument(
        'first_name',
        type=str,
        required=True
    )
    parser.add_argument(
        'last_name',
        type=str,
        required=True
    )
    parser.add_argument(
        'username',
        type=str,
        required=True
    )
    parser.add_argument(
        'password',
        type=str,
        required=True
    )
    parser.add_argument(
        'email',
        type=str,
        required=True
    )

    def __init__(self, db_handler):
        self.DBHandler = db_handler

    def post(self):
        data = SignUp.parser.parse_args()
        response = {}
        status = 200
        data['password'] = sha256.hash(data['password'])

        try:
            self.DBHandler.add(
                models.User(**data)
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