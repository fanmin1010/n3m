'''MODEL'''
import sys, os
from index import db, bcrypt
from sqlalchemy.exc import IntegrityError


class User(db.Model):
    '''User model class to handle all users'''
    user_id = db.Column(db.Integer(), primary_key=True)
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

    def __str__(self):
        return '''User::::::
        USERID: ''' + str(self.user_id) + '''
        EMAIL: ''' + self.email + '''
        USERNAME: ''' + self.username + '''
        PASSWORD: ''' + self.password + '''
        PGP: ''' + self.pgp_key + '''
        AVATAR: ''' + self.avatar + '''
        '''

    @staticmethod
    def hashed_password(password):
        '''encrypt password'''
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user(email, password):
        '''load user from login credentials'''
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None

    @staticmethod
    def get_avatar_for_useremail(useremail):
        '''find user avatar based on email'''
        user = User.query.filter_by(email=useremail).first()
        if user:
            return user.avatar
        else:
            return None

    @staticmethod
    def get_avatar_for_username(uname):
        '''find user avatar based on username'''
        print('inside get avatar for username')
        print(uname)
        try:
            user = User.query.filter_by(username=uname).first()
            if user:
                return user.avatar
            else:
                return None
        except sqlalchemy.exc.InvalidRequestError as sqlIRE:
            return None

class Friendship(db.Model):
    '''Friendship model class handles chat between two users'''
    fs_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    friender = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    friendee = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    est_time = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now())
    __table_args__ = (
        db.UniqueConstraint(
            'friender',
            'friendee',
            name='uix_1'),
    )

    def __init__(self, friender, friendee):
        self.friender = friender
        self.friendee = friendee

    def __repr__(self):
        return '<Friendship between %r and %r>' % (
            self.friender, self.friendee)

    @staticmethod
    def get_friendship_with_user_ids(friender_id, friendee_id):
        '''get firendship instance of two users'''
        f_ship = Friendship.query.filter_by(
            friender=friender_id, friendee=friendee_id).first()
        if f_ship:
            return f_ship
        else:
            return None

    @staticmethod
    def get_all_friendship_of_user(friender_id):
        '''get all friendship instances for a user'''
        f_ship = Friendship.query.filter_by(friender=friender_id).all()
        return f_ship


class Party(db.Model):
    '''Party model class handles chat between multiple users'''
    party_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    party_name = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        nullable=False)
    avatar = db.Column(db.String(128), unique=False)
    __table_args__ = (
        db.UniqueConstraint(
            'party_name',
            'owner_id',
            name='unique_pname_with_owner'),
    )

    def __init__(self, party_name, owner_id, avatar):
        self.party_name = party_name
        self.owner_id = owner_id
        self.avatar = avatar

    def __repr__(self):
        return '<Party %r owned by %r>' % (self.party_name, self.owner_id)

    @staticmethod
    def get_my_parties(owner_id):
        '''get all parties created by a specific user'''
        parties = Party.query.filter_by(owner_id=owner_id).all()
        # print(parties)
        if parties:
            return parties
        else:
            return None


class PartyUser(db.Model):
    '''PartyUser model class handles relationship between a party and users'''
    __tablename__ = 'partyuser'
    pu_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    party_id = db.Column(
        db.Integer(),
        db.ForeignKey('party.party_id'),
        nullable=False)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        nullable=False)
    __table_args__ = (
        db.UniqueConstraint(
            'party_id',
            'user_id',
            name='unique_pid_with_user'),
    )

    def __init__(self, party_id, user_id):
        self.party_id = party_id
        self.user_id = user_id

    @staticmethod
    def get_party_users(party_id):
        '''get all users of a party'''
        party_users = PartyUser.query.filter_by(party_id=party_id).first()
        if party_users:
            return party_users
        else:
            return None


class FriendMessage(db.Model):
    '''FriendMessage model class stores messages of a Friendship chat'''
    __tablename__ = 'friendmessage'
    fm_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    fs_id = db.Column(
        db.Integer(),
        db.ForeignKey('friendship.fs_id'),
        nullable=False)
    sender_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        nullable=False)
    timestamp = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now())
    message = db.Column(db.String(65535), nullable=False)

    def __init__(self, fs_id, sender_id, message):
        self.fs_id = fs_id
        self.sender_id = sender_id
        self.message = message
        self.timestamp = db.func.now()

    @staticmethod
    def add_friend_message(sender, receiver, messagetext):
        '''store message from a Friendship chat'''
        senderuser = User.query.filter_by(username=sender).first()
        print('in add_friend_message')
        if senderuser is None:
            return "empty sender user"
        sender_id = senderuser.user_id
        receiveruser = User.query.filter_by(username=receiver).first()
        print('got receiveruser')
        if receiveruser is None:
            return "empty receiver user"
        receiver_id = receiveruser.user_id
        # always store the message with one friendship where
        # friender_id<=friendee_id
        friendship = (
            Friendship.get_friendship_with_user_ids(sender_id, receiver_id)
            if sender_id < receiver_id else
            Friendship.get_friendship_with_user_ids(receiver_id, sender_id))
        print('made friendship object')
        if friendship is None:
            return "empty friendship"
        else:
            fs_id = friendship.fs_id
            message = FriendMessage(fs_id, sender_id, messagetext)
            print('made friendmessage object')
            db.session.add(message)
            try:
                db.session.commit()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                return "database error"
            return "success"

    @staticmethod
    def get_friend_messages(user1, user2):
        '''get Friendship message history'''
        senderuser = User.query.filter_by(username=user1).first()
        if senderuser is None:
            return "empty user1"
        sender_id = senderuser.user_id
        receiveruser = User.query.filter_by(username=user2).first()
        if receiveruser is None:
            return "empty user2"
        receiver_id = receiveruser.user_id
        # always store the message with one friendship where
        # friender_id<=friendee_id
        if sender_id < receiver_id:
            friendship = Friendship.get_friendship_with_user_ids(
                sender_id, receiver_id)
        else:
            friendship = Friendship.get_friendship_with_user_ids(
                receiver_id, sender_id)
        if friendship is None:
            return "empty friendship"
        fs_id = friendship.fs_id
        friend_messages = (FriendMessage
                           .query
                           .filter_by(fs_id=fs_id)
                           .order_by(FriendMessage.timestamp)
                           .all())
        sender_av = User.get_avatar_for_username(user1)
        receiver_av = User.get_avatar_for_username(user2)
        if not friend_messages:
            return friend_messages
        else:
            msg_list = []
            for msg in friend_messages:
                if msg.sender_id == sender_id:
                    avatar = sender_av
                    username = user1
                else:
                    avatar = receiver_av
                    username = user2
                msg_list.append(
                    dict(
                        time=str(msg.timestamp),
                        text=msg.message,
                        avatar=avatar,
                        username=username))
            return msg_list


class PartyMessage(db.Model):
    '''PartyMessage model class stores party chat messages'''
    __tablename__ = 'partymessage'
    pm_id = db.Column(db.Integer(), primary_key=True, nullable=False)
    party_id = db.Column(
        db.Integer(),
        db.ForeignKey('party.party_id'),
        nullable=False)
    sender_id = db.Column(
        db.Integer(),
        db.ForeignKey('user.user_id'),
        nullable=False)
    timestamp = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=db.func.now())
    message = db.Column(db.String(65535), nullable=False)

    def __init__(self, party_id, sender_id, message):
        self.party_id = party_id
        self.sender_id = sender_id
        self.message = message
        self.timestamp = db.func.now()

    @staticmethod
    def add_party_message(party_id, sender, messagetext):
        '''store message from party chat'''
        senderuser = User.query.filter_by(username=sender).first()
        if not senderuser:
            return "empty sender user"
        sender_id = senderuser.user_id
        message = PartyMessage(party_id, sender_id, messagetext)
        db.session.add(message)
        try:
            db.session.commit()
        except IntegrityError:
            return "database error"
        return "success"

    @staticmethod
    def get_party_messages(party_id):
        '''get message history for a party'''
        party_messages = (PartyMessage
                          .query
                          .filter_by(party_id=party_id)
                          .order_by(PartyMessage.timestamp)
                          .all())
        if not party_messages:
            return party_messages
        else:
            msg_list = []
            for msg in party_messages:
                sender = User.query.filter_by(user_id=msg.sender_id).first()
                sender_avatar = sender.avatar
                msg_list.append(
                    dict(
                        time=str(msg.timestamp),
                        text=msg.message,
                        avatar=sender_avatar,
                        username=sender.username))
            return msg_list
