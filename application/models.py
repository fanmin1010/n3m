from index import db, bcrypt


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    pgp_key = db.Column(db.String(255), unique=True)
    avatar = db.Column(db.String(128), unique=False)

    def __init__(self, username, email, password, pgp_key, avatar):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)
        self.username = username
        self.pgp_key = pgp_key
        self.avatar = avatar

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None
