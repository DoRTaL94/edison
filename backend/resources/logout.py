from flask_restful import Resource
from flask_jwt_extended import (get_raw_jwt, jwt_required, jwt_refresh_token_required)

class LogoutAccess(Resource):
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            self.DBHandler.add_blacklisted_jti(jti)
            return {'msg': 'Access token has been revoked'}
        except Exception as e:
            return {'msg': 'Something went wrong'}, 500


class LogoutRefresh(Resource):
    def __init__(self, **kwargs):
        self.DBHandler = kwargs['DBHandler']

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            self.DBHandler.add_blacklisted_jti(jti)
            return {'msg': 'Refresh token has been revoked'}
        except Exception as e:
            print(e)
            return {'msg': 'Something went wrong'}, 500