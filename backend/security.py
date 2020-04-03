from werkzeug.security import safe_str_cmp
from services.dbhandler import DBHandler

def authenticate(username, password):
    user = DBHandler.get_user_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

# When we send with a request our token the identity function called.
# It uses the JWT token the get the user id and then returns the user.
def identity(payload):
    user_id = payload['identity']
    return DBHandler.get_user_by_id(user_id)
