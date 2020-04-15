from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import backend.models as models
from passlib.hash import pbkdf2_sha256 as sha256


class User(Resource):
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

    @jwt_required
    def get(self, username):
        user = self.DBHandler.get_by_filters(models.User, {'username': username})
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
            self.DBHandler.delete(self.DBHandler.get_by_username(models.User, username))
        else:
            response = {'msg': 'User can delete himself but no other users'}
            status = 403

        return response, status
    
    @jwt_required
    def put(self, username):
        response = {}
        status = 200

        if(get_jwt_identity() == username):
            data = User.parser.parse_args()
            
            try:
                data['password'] = sha256.hash(data['password'])
                updated_user = models.User(**data)

                user_to_be_updated = self.DBHandler.get_by_filters(models.User, {'username': username})
                if user_to_be_updated is None:
                    raise ValueError(f"The user with username: {username} is not in the DB.")

                user_to_be_updated.username = updated_user.username
                user_to_be_updated.first_name = updated_user.first_name
                user_to_be_updated.last_name = updated_user.last_name
                user_to_be_updated.password = updated_user.password
                user_to_be_updated.email = updated_user.email

                self.DBHandler.update()

                response = {'msg': 'User updated', 'user': models.ResponseUser(user_to_be_updated).__dict__}
            except KeyError:
                response = {'msg': 'Update failed. Json missing keys.'}
                status = 400
        else:
            response = {'msg': 'User can update himself but no other users'}

        return response, status
