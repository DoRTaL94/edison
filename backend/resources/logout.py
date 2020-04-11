from flask_restful import Resource
from flask_jwt_extended import (get_raw_jwt, jwt_required, jwt_refresh_token_required)

class LogoutAccess(Resource):
    def __init__(self, db_handler):
        self.DBHandler = db_handler

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            self.DBHandler.add_blacklisted_jti(jti)
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
            self.DBHandler.add_blacklisted_jti(jti)
            return {'msg': 'Refresh token has been revoked'}
        except Exception:
            return {'msg': 'Something went wrong'}, 500