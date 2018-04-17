from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import DB, LOGIN

class User(UserMixin, DB.Model):
    __table_args__ = {'extend_existing': True}
    id = DB.Column('User_id', DB.Integer, primary_key = True)
    name = DB.Column(DB.String(100))
    email = DB.Column(DB.String(50), unique=True, nullable=False)
    password_hash = DB.Column(DB.String(128))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
# @LOGIN.user_loader
# def load_user(id):
#     return User.query.get(int(id))


