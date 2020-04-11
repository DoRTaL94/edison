from flask_restful import Resource
from flask_jwt_extended import jwt_required
import backend.models as models

class Users(Resource):
    def __init__(self, db_handler):
        self.DBHandler = db_handler

    @jwt_required
    def get(self, username=None):
        status = 200
        response = list(
            map(
                lambda user: models.ResponseUser(user).__dict__, self.DBHandler.get_all(models.User)
            )
        )

        return response, status