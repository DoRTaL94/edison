from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.response_user import ResponseUser

class Users(Resource):
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    @jwt_required
    def get(self, username=None):
        status = 200
        response = list(
            map(
                lambda user: ResponseUser(user).__dict__, self.DBHandler.get_users()
            )
        )

        return response, status