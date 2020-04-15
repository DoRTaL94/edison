from flask_restful import Resource
from flask_jwt_extended import (get_raw_jwt, jwt_required, jwt_refresh_token_required)
import backend.models as models
from datetime import datetime


class LogoutAccess(Resource):
    def __init__(self, db_handler):
        self.DBHandler = db_handler

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = models.Token(jti, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            self.DBHandler.add(blacklisted_token)
            return {'msg': 'Access token has been revoked'}
        except Exception:
            return {'msg': 'Something went wrong'}, 500


class LogoutRefresh(Resource):
    def __init__(self, db_handler):
        self.DBHandler = db_handler

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = models.Token(jti, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            self.DBHandler.add(blacklisted_token)
            return {'msg': 'Refresh token has been revoked'}
        except Exception:
            return {'msg': 'Something went wrong'}, 500