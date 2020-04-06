from flask import Flask
from flask_restful import Api
from resources import (users, user, signup, login, token_refresh, logout)
from flask_jwt_extended import JWTManager
from services.dbhandler import DBHandler
import secrets

# API description in swagger - https://app.swaggerhub.com/apis/DoRTaL94/UserManagment/1.0.0

app = Flask(__name__)
# Enables response message for unauthenticated requests
app.config['PROPAGATE_EXCEPTIONS'] = True
# JWTManager uses this secret key for creating tokens
app.config['JWT_SECRET_KEY'] = secrets.token_hex(24)
# This tells the JWTManager to call 'check_if_token_in_blacklist' function below on every request
app.config['JWT_BLACKLIST_ENABLED'] = True
# We're going to check if both access_token and refresh_token are black listed
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)
# Creation of Json-Web-Token manager.
# In order to reach secured endpoints client should add an authorization header with the value Bearer <token>.
jwt = JWTManager(app)

# This decorator is a callback and it is called every time user is trying to access secured endpoints. 
# The function under the decorator should return true or false depending on if the passed token is blacklisted.
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return DBHandler.is_jti_blacklisted(jti)

# Use of dependecy injection of DBHandler to loosly couple our classes
api.add_resource(user.User, '/user/<string:username>', 
    resource_class_kwargs={ 'DBHandler': DBHandler })
api.add_resource(users.Users, '/users', 
    resource_class_kwargs={ 'DBHandler': DBHandler })
api.add_resource(signup.SignUp, '/signup', 
    resource_class_kwargs={ 'DBHandler': DBHandler })
api.add_resource(login.Login, '/login', 
    resource_class_kwargs={ 'DBHandler': DBHandler })
api.add_resource(logout.LogoutAccess, '/logout/access', 
    resource_class_kwargs={ 'DBHandler': DBHandler })
api.add_resource(logout.LogoutRefresh, '/logout/refresh', 
    resource_class_kwargs={ 'DBHandler': DBHandler })
api.add_resource(token_refresh.TokenRefresh, '/token-refresh')

if __name__ == "__main__":
    app.run(port=3000, debug=True)
