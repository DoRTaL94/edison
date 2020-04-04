from passlib.hash import pbkdf2_sha256 as sha256

class User:
    def __init__(self, _id, username, password, firstname, lastname, email):
        self.username = username
        self.id = _id
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
    
    @staticmethod
    def generate_hashed_password(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        return sha256.verify(password, hashed_password)