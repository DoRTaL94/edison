from models.user import User

# This class should be used for sending users information to client.
# We don't want to send sensitive information such as password or email.
class ResponseUser:
    def __init__(self, user):
        if type(user) is User:
            self.id = user.id
            self.username = user.username
            self.firstname = user.firstname
            self.lastname = user.lastname
        else:
            raise ValueError("user parameter should be of type User")
