from flask import Flask
from flask_restful import Api
from controllers import (users, user, signup, login, token_refresh, logout)
from flask_jwt_extended import JWTManager
from services.dbhandler import DBHandler
import secrets

# API description in swagger - https://app.swaggerhub.com/apis/DoRTaL94/UserManagment/1.0.0

app = Flask(__name__)
# Enables response message for unauthenticated requests
app.config['PROPAGATE_EXCEPTIONS'] = True
# JWTManager uses this secret key for creating tokens
app.config['JWT_SECRET_KEY'] = secrets.token_hex(24)
# This tell the JWTManager to call 'check_if_token_in_blacklist' function below on every request
app.config['JWT_BLACKLIST_ENABLED'] = True
# We're going to check if both access_token and refresh_token are black listed
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)
# Creation of Json-Web-Token manager.
jwt = JWTManager(app)

# This decorator is a callback and it is called every time user is trying to access secured endpoints. 
# The function under the decorator should return true or false depending on if the passed token is blacklisted.
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return DBHandler.is_jti_blacklisted(jti)

api.add_resource(user.UserController, '/user/<string:username>')
api.add_resource(users.UsersController, '/users')
api.add_resource(signup.SignUpController, '/signup')
api.add_resource(login.LoginController, '/login')
api.add_resource(token_refresh.TokenRefresh, '/token-refresh')
api.add_resource(logout.LogoutAccess, '/logout/access')
api.add_resource(logout.LogoutRefresh, '/logout/refresh')

if __name__ == "__main__":
    app.run(port=3000, debug=True)
