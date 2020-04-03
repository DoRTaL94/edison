class User:
    def __init__(self, _id, username, password, firstname, lastname, email):
        self.username = username
        self.id = _id
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email