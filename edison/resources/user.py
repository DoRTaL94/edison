import edison.models as models

from edison import db
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token)



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

    @jwt_required
    def get(self, username: str):
        user = models.User.query.filter_by(username=username).first()

        status = 200 if user else 404
        response = {
            username: user.to_json()
        } if user else {'msg': 'User not found'}

        return response, status

    @jwt_required
    def delete(self, username: str):
        response = {'msg': 'User deleted'}
        status = 200

        if self.__request_is_legal(username):
            db.session.delete(models.User.query.filter_by(username=username).first())
            db.session.commit()
        else:
            response = {'msg': 'User can delete himself but no other users'}
            status = 403

        return response, status

    @jwt_required
    def put(self, username: str):
        response = {}
        status = 200

        if self.__request_is_legal(username):
            data = User.parser.parse_args()
            try:
                updated_user = self.__create_updated_user(data)
                user_to_be_updated = self.__update_user_in_DB(updated_user, username)
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                response = {'msg': 'User updated',
                            'user': user_to_be_updated.to_json(),
                            'access_token': access_token,
                            'refresh_token': refresh_token}
            except KeyError:
                response = {'msg': 'Update failed. Json missing keys.'}
                status = 400
        else:
            response = {'msg': 'User can update himself but no other users'}

        return response, status

    def __request_is_legal(self, username: str):
        return get_jwt_identity() == username

    def __create_updated_user(self, data):
        data['password'] = sha256.hash(data['password'])
        return models.User(**data)

    def __update_user_in_DB(self, updated_user: models.User, username: str):
        user_to_be_updated = models.User.query.filter_by(username=username).first()
        user_to_be_updated.username = updated_user.username
        user_to_be_updated.first_name = updated_user.first_name
        user_to_be_updated.last_name = updated_user.last_name
        user_to_be_updated.password = updated_user.password
        user_to_be_updated.email = updated_user.email
        db.session.commit()
        return user_to_be_updated