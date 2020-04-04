from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.response_user import ResponseUser
from services.dbhandler import DBHandler

class UsersController(Resource):
    @jwt_required
    def get(self, username=None):
        status = 200
        response = list(
            map(
                lambda user: ResponseUser(user).__dict__, DBHandler.get_users()
            )
        )

        return response, status