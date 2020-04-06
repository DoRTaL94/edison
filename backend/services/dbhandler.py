from models.user import User
from models.response_user import ResponseUser

# Temporary databases
_id = 1
username_mapping = {}
userid_mapping = {}
jti_mapping = {}

# This class should be modified to work against PostgreSQL.
class DBHandler:

    @staticmethod
    def get_user_by_username(username):
        return username_mapping.get(username, None)

    @staticmethod
    def get_user_by_id(_id):
        return userid_mapping.get(_id, None)
    
    @staticmethod
    def delete_user_by_username(username):
        user = username_mapping.get(username, None)
        if user:
            userid_mapping.pop(user.id)
            username_mapping.pop(username)
    
    @staticmethod
    def delete_user_by_id(_id):
        user = userid_mapping.get(_id, None)
        if user:
            username_mapping.pop(user.username)
            userid_mapping.pop(_id)

    @staticmethod 
    def add_user(user):
        if type(user) is User:
            user_in_map = username_mapping.get(user.username, None)
            user_not_exists = user_in_map == None

            if user_not_exists:
                global _id
                user.id = _id
                username_mapping[user.username] = user
                userid_mapping[_id] = user
                _id += 1
            else:
                raise ValueError("User already exists")
        else:
            raise ValueError("User should be of type User")

    @staticmethod
    def get_users():
        return username_mapping.values()

    @staticmethod
    def update_user(username, user):
        if type(user) is User:
            user_in_map = username_mapping.get(username, None)
            user_not_exists = user_in_map == None

            if user_not_exists:
                DBHandler.add_user(user)
            else:
                user.id = user_in_map.id # the id shouldn't be changed
                username_mapping.update({ username: user })
                userid_mapping.update({ user.id: user })
                return ResponseUser(username_mapping.get(username, None))
        else:
            raise ValueError("User should be of type User")

    @staticmethod
    def add_blacklisted_jti(jti):
        jti_mapping[jti] = jti

    @staticmethod
    def is_jti_blacklisted(token):
        return jti_mapping.get(token, None) != None
