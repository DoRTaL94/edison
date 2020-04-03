from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from controllers.users import UsersController
from controllers.user import UserController
from controllers.signup import SignUpController
from security import authenticate, identity
import secrets

app = Flask(__name__)
# Enables response message for unauthenticated requests
app.config['PROPAGATE_EXCEPTIONS'] = True
# JWT uses this secret key for creating the token
app.secret_key = secrets.token_hex(24)
api = Api(app)

# The JWT object uses app, authenticate and identity functions together 
# for authentication of users.
# JWT creates a new endpoint /auth.
# Sending a request to /auth with username and password will send back a token as a response.
# In order for users to reach secured endpoints they required to attach to every
# request header the following pair - Key: Authorization, Value: JWT <token>.
jwt = JWT(app, authenticate, identity)

api.add_resource(UserController, '/user/<string:username>')
api.add_resource(UsersController, '/users')
api.add_resource(SignUpController, '/user/signup')

if __name__ == "__main__":
    app.run(port=3000, debug=True)
