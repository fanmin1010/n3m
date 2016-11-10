from __future__ import print_function
from flask import request, render_template, jsonify, url_for, redirect, g
from flask_socketio import SocketIO, emit
from .models import User, Friendship, Party, PartyUser
from index import app, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .utils.auth import generate_token, requires_auth, verify_token
import requests
import datetime, time
import json
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
    print(friends)
    return friends

@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        username=incoming["username"],
        email=incoming["email"],
        password=incoming["password"],
        pgp_key=incoming["pgp_key"],
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
    )

@app.route("/api/user_add_friend", methods = ["POST"])
@requires_auth
def add_friendship():
    incoming = request.get_json()
    print(incoming)
    # friendemail refers to the email to be added email->friendemail
    db.session.commit()
    friendee = User.query.filter_by(email=incoming["email"]).first()
    print(friendee)
    # new_user = User.query.filter_by(email="starks@gmail.com").first()

    current_user = g.current_user
    if friendee == None:
        return jsonify(message="User with that email does not exist"), 409
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
            return jsonify(message="That friendship already exists"), 410

        return jsonify(error = False, id = friendee_id, email = friendee_email, avatar = friendee_avatar), 200

@app.route("/api/createParty", methods = ["POST"])
@requires_auth
def createParty():
    incoming = request.get_json()
    party = Party(
        partyName=incoming["partyName"],
        ownerID=g.current_user["id"]
    )
    db.session.add(party)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Unable to create party"),409

    new_party = Party.query.filter_by(partyName=incoming["partyName"]).first()
    print(new_party)
    return jsonify(
        partyID=new_party.partyID, partyName = new_party.partyName
    ), 400

@app.route("/api/add_users_to_party", methods = ["POST"])
@requires_auth
def add_to_party():
    incoming = request.get_json()
    party = Party.query.filter_by(ownerID=g.current_user["id"], partyName=incoming["partyName"]).first()
    # print(party)
    if not party:
        return jsonify(message="Party does not exist."), 420
    user = User.query.filter_by(email=incoming["email"]).first()
    if not user:
        return jsonify(message="User does not exist."), 421
    pu = PartyUser(party.partyID, user.id)
    db.session.add(pu)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Party user relation already exists."), 422

    return jsonify(status = "success", avatar=user.avatar, email = user.email, name = user.username), 400

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
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403




@app.route("/api/calluber", methods=["GET"])
def call_uber():
    #incoming = request.get_json()
    start_address = '850 3rd Ave. New York, NY 10022'
    end_address = '205 W 109th St, New York, NY10025'
    startgeo = geocoder.google(start_address)
    endgeo = geocoder.google(end_address)
    url='https://api.uber.com/v1.2/estimates/price'
    payload = {'start_latitude':startgeo.latlng[0], 'start_longitude':startgeo.latlng[1], 'end_latitude':endgeo.latlng[0], 'end_longitude':endgeo.latlng[1]}
    headers = {'Authorization': 'Token x4maHB7QT8tWJqKfkfPVyzWfpbp7g5QmehniOIf5', 'Content-Type': 'application/json', 'Accept-Language': 'en_US' }
    r = requests.get(url, params=payload, headers=headers)
    print(r.text)
    #print(incoming)
    print ("startgeo: ")
    print (startgeo.latlng)
    print ("endgeo: ")
    print (endgeo.latlng)
    return jsonify(r.text)


socketio = SocketIO(app)


@socketio.on('servermessage')
def chat_message(message):
    print('There was a message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['username'])
    now = datetime.datetime.now().strftime('%H:%M:%S')
    print('This is the time: ' + str(now), file=sys.stderr)
    socketio.emit(message['partyname'], {'username': message['username'], 'text': message['msgtext'], 'avatar': avatar, 'time': now})
