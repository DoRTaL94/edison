from passlib.hash import pbkdf2_sha256 as sha256
from backend import db

class User(db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(150), nullable = False)
    
    def __init__(self, username, password, first_name, last_name, email):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    
    @staticmethod
    def generate_hashed_password(password):
        return sha256.hash(password)

    @staticmethod
    def verify_password(password, hashed_password):
        return sha256.verify(password, hashed_password)