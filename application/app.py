from __future__ import print_function
from flask import request, render_template, jsonify, url_for, redirect, g
from flask_socketio import SocketIO, emit
from .models import User, Friendship, Party, PartyUser, FriendMessage #,UberRide
from index import app, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .utils.auth import generate_token, requires_auth, verify_token
import requests
import datetime, time
import json
import re
import sys
import geocoder

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)

@app.route("/api/friendlist", methods=["GET"])
@requires_auth
def get_friendlist():
    current_user = g.current_user
    result = db.engine.execute('select u.id, u.avatar, u.username from friendship f join "user" u  on f.friendee=u.id where f.friender = ' + str(current_user["id"]));
    friends = json.dumps([dict(r) for r in result])
    return friends

@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    uname = incoming["username"]
    eml = incoming["email"]
    pswd = incoming["password"]
    pgp = incoming["pgp_key"]
    eml_rgx=r"[^@]+@[^@]+\.[^@]+"

    if not uname:
        return jsonify(message='Username cannot be null.'), 400
    if len(uname) < 3:
        return jsonify(message='Username must be at least 3 characters.'), 400
    if len(uname) > 20:
        return jsonify(message='Username must be no more than 20 characters.'), 400
    if not eml:
        return jsonify(message='Email cannot be null.'), 400
    if not re.match(eml_rgx, eml):
        return jsonify(message='Email address not valid.'), 400
    if not pswd:
        return jsonify(message='Password cannot be null.'), 400
    if len(pswd) < 6:
        return jsonify(message='Password must be at least 6 characters.'), 400
    if len(pswd) > 20:
        return jsonify(message='Password must be no more than 20 characters.'), 400

    user = User(
        username=uname,
        email=eml,
        password=pswd,
        pgp_key=pgp,
        avatar="dist/images/default_avatar.png"  # waiting for Front-end pass-in
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that username or email already exists"), 409
    new_user = User.query.filter_by(email=incoming["email"]).first()
    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    ), 201

@app.route("/api/user_add_friend", methods = ["POST"])
@requires_auth
def add_friendship():
    incoming = request.get_json()
    # friendemail refers to the email to be added email->friendemail
    db.session.commit()
    friendee = User.query.filter_by(email=incoming["email"]).first()
    # new_user = User.query.filter_by(email="starks@gmail.com").first()

    current_user = g.current_user
    if friendee == None:
        return jsonify(message="User with that email does not exist"), 403
    else:
        friender_email = current_user["email"]
        friender_id = current_user["id"]

        friendee_email = friendee.email
        friendee_id = friendee.id
        friendee_avatar = friendee.avatar
        newfriendship = Friendship(friender_id, friendee_id)
        # this is for early practice that friendship doesnt need to be requested
        newfriendship2 = Friendship(friendee_id, friender_id)

        db.session.add(newfriendship)
        try:
            db.session.commit()
            # again for early practice
            db.session.add(newfriendship2)
            db.session.commit()
        except SQLAlchemyError:
            return jsonify(message="That friendship already exists"), 409
        fs_id = 0
        if friender_id<friendee_id:
            fs_id = newfriendship.fs_id
        else:
            fs_id = newfriendship2.fs_id

        return jsonify(error = False, id = friendee_id, email = friendee_email, avatar = friendee_avatar, friendship_id=fs_id)

@app.route("/api/createParty", methods = ["POST"])
@requires_auth
def createParty():
    incoming = request.get_json()
    party = Party(
        partyName=incoming["partyName"],
        ownerID=g.current_user["id"]
        avatar="dist/images/default_team.png"  # waiting for Front-end pass-in
    )
    db.session.add(party)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Party already existed."),409

    new_party = Party.query.filter_by(partyName=incoming["partyName"]).first()
    return jsonify(
        partyID=new_party.partyID, partyName = new_party.partyName
    )


@app.route("/api/partylist", methods=["GET"])
@requires_auth
def get_partylist():
    current_user = g.current_user
    result = db.engine.execute('select * from party where "ownerID" = ' + str(current_user["id"]));
    #result=Party.query.filter_by(ownerID=current_user).all()
    parties = json.dumps([dict(r) for r in result])
    print(parties)
    return parties



@app.route("/api/add_users_to_party", methods = ["POST"])
@requires_auth
def add_to_party():
    incoming = request.get_json()
    party = Party.query.filter_by(ownerID=g.current_user["id"], partyName=incoming["partyName"]).first()
    # print(party)
    if not party:
        return jsonify(message="Party does not exist."), 404
    user = User.query.filter_by(email=incoming["email"]).first()
    if not user:
        return jsonify(message="User does not exist."), 403
    pu = PartyUser(party.partyID, user.id)
    db.session.add(pu)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Party user relation already exists."), 409

    return jsonify(status = "success", avatar=user.avatar, email = user.email, name = user.username)

@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True), 202
    else:
        return jsonify(token_is_valid=False), 403




@app.route("/api/calluber", methods=["POST"])
def call_uber():
    incoming = request.get_json()
    start_address = '850 3rd Ave. New York, NY 10022'
    end_address = incoming["end_address"]
    startgeo = geocoder.google(start_address)
    endgeo = geocoder.google(end_address)
    url='https://api.uber.com/v1.2/estimates/price'
    payload = {'start_latitude':startgeo.latlng[0], 'start_longitude':startgeo.latlng[1], 'end_latitude':endgeo.latlng[0], 'end_longitude':endgeo.latlng[1]}
    headers = {'Authorization': 'Token x4maHB7QT8tWJqKfkfPVyzWfpbp7g5QmehniOIf5', 'Content-Type': 'application/json', 'Accept-Language': 'en_US' }
    r = requests.get(url, params=payload, headers=headers)
    #print(r.text)
    #print(incoming)
    print("start address: " + start_address)
    print("end address: " + end_address)
    print ("startgeo: " + str(startgeo.latlng))
    print ("endgeo: " + str(endgeo.latlng))
    return jsonify(r.text)

"""
@app.route("/api/saveride", methods = ["POST"])
@requires_auth
def saveride():
    incoming = request.get_json()
    #now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ride = UberRide(
        userID=g.current_user["id"],
        when=incoming["when"],
        duration=incoming["duration"],
        location=incoming["location"],
        destination=incoming["destination"],
        cost=incoming["cost"]
    )
    db.session.add(ride)
    try:
        db.session.commit()
    IntegrityError:
        return jsonify(message="Ride already existed."),409

    new_ride = UberRide.query.filter_by(userID=incoming["userID"]).first()
    # print(new_ride)
    return jsonify(
        rideID=new_ride.id, rideDisplay = new_ride.__repr__
    )
"""



socketio = SocketIO(app)


@socketio.on('party_message')
def party_message(message):
    print('There was a message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['username'])
    now = datetime.datetime.now().strftime('%H:%M:%S')
    print('This is the time: ' + str(now), file=sys.stderr)
    socketio.emit(message['partyname'], {'username': message['username'], 'text': message['msgtext'], 'avatar': avatar, 'time': now})
    # This is where the message should get inserted into database. Remove this line.


@socketio.on('user2user_message')
def user2user_message(message):
    print('There was a message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['sender'])
    now = datetime.datetime.now().strftime('%H:%M:%S')
    sender=message['sender']
    receiver=message['receiver']
    print('This is the time: ' + str(now), file=sys.stderr)
    # socketio.emit(message['partyname'], {'username': sender, 'text': message['msgtext'], 'avatar': avatar, 'time': now})
    # This is where the message should get inserted into database. Remove this line.
    result = FriendMessage.add_friendMessage(sender, receiver, now, message['msgtext'])
    if result == "success":
        socketio.emit(message['partyname'], {'username': sender, 'text': message['msgtext'], 'avatar': avatar, 'time': now})
    else:
        print("Something happend with error in the database.")


def get_friend_msg_his(curr_user, friend):
    # both curr_user and friend are the usernames that you want to retrieve the message history of
    msg_list = FriendMessage.getFriendMessages(curr_user, friend)
    pass
