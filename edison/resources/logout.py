from edison import db
from edison.models import Token
from flask_restful import Resource
from flask_jwt_extended import (get_raw_jwt, jwt_required, jwt_refresh_token_required)
from datetime import datetime


class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = Token(jti=jti, creation_timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            db.session.add(blacklisted_token)
            db.session.commit()

            return {'msg': 'Access token has been revoked'}
        except Exception as e :
            print(e)
            return {'msg': 'Something went wrong'}, 500


class LogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            blacklisted_token = Token(jti=jti, creation_timestamp=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
            db.session.add(blacklisted_token)
            db.session.commit()

            return {'msg': 'Refresh token has been revoked'}
        except Exception:
            return {'msg': 'Something went wrong'}, 500
