from backend.models.response_user import ResponseUser
from backend.models.user import User
from backend.models.token import Token
from backend import db
from datetime import datetime

class DBHandler:

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username = username).first()

    @staticmethod
    def get_user_by_id(_id):
        return User.query.get(_id)
    
    @staticmethod
    def delete_user_by_username(username):
        user = DBHandler.get_user_by_username(username)
        print(user)
        DBHandler.delete_user_by_id(user.id)
    
    @staticmethod
    def delete_user_by_id(_id):
        user = DBHandler.get_user_by_id(_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            raise ValueError("User not exists")

    @staticmethod 
    def add_user(user):
        if type(user) is User:
            db.session.add(user)
            db.session.commit()
        else:
            raise ValueError("User should be of type User")

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def update_user_by_username(username, user_with_new_details):
        user_in_db = DBHandler.get_user_by_username(username)
        return DBHandler.update_user(user_in_db, user_with_new_details)
    
    @staticmethod
    def update_user_by_id(_id, user_with_new_details):
        user_in_db = DBHandler.get_user_by_id(_id)
        return DBHandler.update_user(user_in_db, user_with_new_details)

    @staticmethod
    def update_user(user_in_db, user_with_new_details):
        if type(user_with_new_details) is User:
            user_not_exists = user_in_db == None

            if user_not_exists:
                DBHandler.add_user(user_with_new_details)
            else:
                user_in_db.id = user_with_new_details.id
                user_in_db.username = user_with_new_details.username
                user_in_db.password = user_with_new_details.password
                user_in_db.first_name = user_with_new_details.first_name
                user_in_db.last_name = user_with_new_details.last_name
                user_in_db.email = user_with_new_details.email
                db.session.commit()
                return ResponseUser(user_in_db)
        else:
            raise ValueError("User should be of type User")

    @staticmethod
    def add_blacklisted_jti(jti):
        blacklisted_token = Token(jti, datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        db.session.add(blacklisted_token)
        db.session.commit()

    @staticmethod
    def is_jti_blacklisted(jti):
        return Token.query.get(jti) != None
