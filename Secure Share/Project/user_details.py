import user_authentication

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def getusername(self):
        return self.username

    def getpassword(self):
        return self.password

    def getemail(self):
        return self.email

    def register(self):
        errors = user_authentication.get_errors(self.username, self.password, self.email)
        return errors


