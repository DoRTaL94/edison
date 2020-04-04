from flask_restful import Resource
from flask import request
from services.dbhandler import DBHandler
from models.user import User
from flask_jwt_extended import (get_raw_jwt, jwt_required, jwt_refresh_token_required)

class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        
        try:
            DBHandler.add_blacklisted_jti(jti)
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            DBHandler.add_blacklisted_jti(jti)
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500