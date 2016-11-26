from index import db, bcrypt
from datetime import datetime

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

    @staticmethod
    def get_avatar_for_useremail(useremail):
        user = User.query.filter_by(email=useremail).first()
        if user:
            return user.avatar
        else:
            return None
    
    @staticmethod
    def get_avatar_for_username(uname):
        user = User.query.filter_by(username=uname).first()
        if user:
            return user.avatar
        else:
            return None

class Friendship(db.Model):
    fs_id = db.Column(db.Integer(), primary_key = True, nullable=False)
    friender = db.Column(db.Integer(), db.ForeignKey('user.id'))
    friendee = db.Column(db.Integer(), db.ForeignKey('user.id'))
    est_time = db.Column(db.DateTime(), nullable = False, server_default=db.func.now())
    __table_args__ = (db.UniqueConstraint('friender', 'friendee', name = 'uix_1'), )

    def __init__(self, friender, friendee):
        self.friender = friender
        self.friendee = friendee
    def __repr__(self):
        return '<Friendship between %r and %r>' % (self.friender, self.friendee)
    @staticmethod
    def get_friendship_with_user_ids(friender_id, friendee_id):
        f_ship  = Friendship.query.filter_by(friender=friender_id, friendee = friendee_id).first()
        if f_ship:
            return f_ship
        else:
            return None
    @staticmethod
    def get_all_friendship_of_user(friender_id):
        f_ship = Friendship.query.filter_by(friender = friender_id).all()
        if f_ship:
            return f_ship
        else:
            return None

class Party(db.Model):
    partyID = db.Column(db.Integer(), primary_key = True, nullable=False)
    partyName = db.Column(db.String(255), nullable=False)
    ownerID = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    avatar = db.Column(db.String(128), unique=False)
    __table_args__ = (db.UniqueConstraint('partyName', 'ownerID', name = 'unique_pname_with_owner'), )

    def __init__(self, partyName, ownerID):
        self.partyName = partyName
        self.ownerID = ownerID
        self.avatar = avatar

    def __repr__(self):
        return '<Party %r owned by %r>' % (self.partyName, self.ownerID)

    @staticmethod
    def getMyParties(ownerID):
        parties = Party.query.filter_by(ownerID=ownerID).all()
        # print(parties)
        if parties:
            return parties
        else:
            return None

class PartyUser(db.Model):
    puID = db.Column(db.Integer(), primary_key = True, nullable=False)
    partyID = db.Column(db.Integer(), db.ForeignKey('party.partyID'), nullable=False)
    userID = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('partyID', 'userID', name = 'unique_pid_with_user'), )

    def __init__(self, partyID, userID):
        self.partyID = partyID
        self.userID = userID

    @staticmethod
    def getPartyUsers(partyID):
        partyUsers = PartyUser.query.filter_by(partyID=partyID).first()
        if partyUsers:
            return partyUsers
        else:
            return None

"""
class UberRide(db.Model):
    id = db.Column(db.Integer(), primary_key = True, nullable=False)
    userID = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    when = db.Column(db.DateTime(), server_default=sa.func.current_timestamp())
    duration = db.Column('duration', sa.Interval())
    location = db.Column('location', sa.String(length=255), nullable=False)
    destination = db.Column('destination', sa.String(length=255), nullable=False)
    cost = db.Column('cost', sa.Float(), nullable=False)

    def __init__(self, userID, when, duration, location, destination, cost):
        self.userID = userID 
        self.when = when
        self.duration = duration
        self.location = location
        self.destination = destination
        self.cost = cost

    def __repr__(self):
        return '<Uber Ride on %r from %r to %r for %r>' % (self.when, self.location, self.destination, self.cost)

    @staticmethod
    def getRides(userID):
        userRides = UberRide.query.filter_by(userID=userID).all()
        if userRides:
            return userRides 
        else:
            return None

class FriendMessage(db.Model):
    fmID = db.Column(db.Integer(), primary_key = True, nullable = False)
    fs_id = db.Column(db.Integer(), db.ForeignKey('friendship.fs_id'), nullable=False)
    senderID = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    message = db.Column(db.String(65535), nullable=False)

    def __init__(self, fs_id, senderID, timestamp, message):
        self.fs_id = fs_id
        self.senderID = senderID
        self.message = message

    @staticmethod
    def getFriendMessages(senderID):
        friendMessages = FriendMessage.query.filter_by(senderID=senderID)
        return friendMessages

class PartyMessage(db.Model):
    pmID = db.Column(db.Integer(), primary_key = True, nullable=False)
    partyID = db.Column(db.Integer(), db.ForeignKey('party.partyID'), nullable=False)
    senderID = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    message = db.Column(db.String(65535), nullable=False)

    def __init__(self, partyID, senderID, timestamp, message):
        self.partyID = partyID
        self.senderID = senderID
        self.message = message

    @staticmethod
    def getPartyMessages(partyID):
        partyMessages = PartyMessage.query.filter_by(partyID=partyID)
        if partyMessages:
            return partyMessages
        else:
            return None
"""
