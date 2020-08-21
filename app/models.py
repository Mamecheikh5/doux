from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class utilisateur(UserMixin, db.Model):
    """
    Create an user table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True,unique=True)
    nom = db.Column(db.String(60), index=True)
    prenom = db.Column(db.String(60), index=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_invite = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_vendeur = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(60), index=True, unique=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<utilisateur: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return utilisateur.query.get(int(user_id))




 


