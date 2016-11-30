from __future__ import print_function
from flask import request, render_template, jsonify, url_for, redirect, g
from flask_socketio import SocketIO, emit
from .models import User, Friendship, Party, PartyUser, FriendMessage  # ,UberRide
from index import app, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .utils.auth import generate_token, requires_auth, verify_token
from bs4 import BeautifulSoup
import requests
import datetime
import time
import json
import re
import sys
import geocoder
from random import randint
import constants
import difflib
from OpenTable import restaurants


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
    result = db.engine.execute(
        'select u.id, u.avatar, u.username from friendship f join "user" u  on f.friendee=u.id where f.friender = ' +
        str(
            current_user["id"]))
    friends = json.dumps([dict(r) for r in result])
    return friends


@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    uname = incoming["username"]
    eml = incoming["email"]
    pswd = incoming["password"]
    pgp = incoming["pgp_key"]
    eml_rgx = r"[^@]+@[^@]+\.[^@]+"

    if not uname:
        return jsonify(message='Username cannot be null.'), 400
    if len(uname) < 3:
        return jsonify(message='Username must be at least 3 characters.'), 400
    if len(uname) > 20:
        return jsonify(
            message='Username must be no more than 20 characters.'), 400
    if not eml:
        return jsonify(message='Email cannot be null.'), 400
    if not re.match(eml_rgx, eml):
        return jsonify(message='Email address not valid.'), 400
    if not pswd:
        return jsonify(message='Password cannot be null.'), 400
    if len(pswd) < 6:
        return jsonify(message='Password must be at least 6 characters.'), 400
    if len(pswd) > 20:
        return jsonify(
            message='Password must be no more than 20 characters.'), 400

    av_path = "dist/images/avatar0{}.png".format(randint(0, 9))
    user = User(
        username=uname,
        email=eml,
        password=pswd,
        pgp_key=pgp,
        avatar=av_path
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(
            message="User with that username or email already exists"), 409
    new_user = User.query.filter_by(email=incoming["email"]).first()

    def mk_friend(botemail):
        if new_user.email in bot_emails:
            return None
        bot = User.query.filter_by(email=botemail).first()
        print(str(bot))
        if bot is not None:
            print('Bot is not none :)')
            newfriendship = Friendship(new_user.id, bot.id)
            newfriendship2 = Friendship(bot.id, new_user.id)
            db.session.add(newfriendship)
            db.session.commit()
            db.session.add(newfriendship2)
            db.session.commit()

    bot_emails = [constants.UBER_EMAIL, constants.OPENTABLE_EMAIL]
    for email in bot_emails:
        mk_friend(email)

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    ), 201


@app.route("/api/user_add_friend", methods=["POST"])
@requires_auth
def add_friendship():
    incoming = request.get_json()
    # friendemail refers to the email to be added email->friendemail
    db.session.commit()
    friendee = User.query.filter_by(email=incoming["email"]).first()
    # new_user = User.query.filter_by(email="starks@gmail.com").first()

    current_user = g.current_user
    if friendee is None:
        return jsonify(message="User with that email does not exist"), 403
    else:
        friender_email = current_user["email"]
        friender_id = current_user["id"]

        friendee_email = friendee.email
        friendee_id = friendee.id
        friendee_avatar = friendee.avatar
        newfriendship = Friendship(friender_id, friendee_id)
        # this is for early practice that friendship doesnt need to be
        # requested
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
        if friender_id < friendee_id:
            fs_id = newfriendship.fs_id
        else:
            fs_id = newfriendship2.fs_id

        return jsonify(error=False, id=friendee_id, email=friendee_email,
                       avatar=friendee_avatar, friendship_id=fs_id)


@app.route("/api/createParty", methods=["POST"])
@requires_auth
def createParty():
    incoming = request.get_json()
    print('The partyname is')
    print(incoming)
    av_path = "dist/images/team0{}.png".format(randint(0, 9))
    party = Party(
        partyName=incoming["partyName"],
        ownerID=g.current_user["id"],
        avatar=av_path
    )
    db.session.add(party)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Party already existed."), 409

    new_party = party
    return jsonify(
        partyID=new_party.partyID, partyName=new_party.partyName
    )


@app.route("/api/partylist", methods=["GET"])
@requires_auth
def get_partylist():
    current_user = g.current_user
    result = db.engine.execute(
        'select * from party where "ownerID" = {} UNION select p."partyID", p."partyName", p."ownerID", p."avatar" from party p join partyuser pu on p."partyID"=pu."partyID" where pu."userID" ={}'.format(
            current_user["id"],
            current_user["id"]))
    # result=Party.query.filter_by(ownerID=current_user).all()
    parties = json.dumps([dict(r) for r in result])
    print(str(parties), file=sys.stderr)
    return parties


@app.route("/api/add_users_to_party", methods=["POST"])
@requires_auth
def add_to_party():
    incoming = request.get_json()
    party = Party.query.filter_by(
        ownerID=g.current_user["id"],
        partyName=incoming["partyName"]).first()
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

    return jsonify(status="success", avatar=user.avatar,
                   email=user.email, name=user.username)


@app.route("/api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    bot_emails = [constants.UBER_EMAIL, constants.OPENTABLE_EMAIL]
    if incoming["email"] in bot_emails:
        return jsonify(error=True), 403
    user = User.get_user_with_email_and_password(
        incoming["email"], incoming["password"])
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


def call_uber(end_address, lat, lng):
    try:
        endgeo = geocoder.google(end_address)
        endlat = endgeo.latlng[0]
        endlong = endgeo.latlng[1]
    except:
        return 'Could not locate the provided address. Sorry.'
    url = 'https://api.uber.com/v1.2/estimates/price'
    payload = {
        'start_latitude': lat,
        'start_longitude': lng,
        'end_latitude': endlat,
        'end_longitude': endlong }
    headers = {
        'Authorization': 'Token x4maHB7QT8tWJqKfkfPVyzWfpbp7g5QmehniOIf5',
        'Content-Type': 'application/json',
        'Accept-Language': 'en_US'}
    r = requests.get(url, params=payload, headers=headers)
    json_data = json.loads(r.text)
    reply_text = '\n'
    for p in json_data['prices']:
        reply_text = reply_text + p['display_name'] + ': ' + p['estimate'] + '\n'
    return reply_text


def call_opentable(rest_id, guest_count, res_time):
    timeList = []
    url = 'http://www.opentable.com/restaurant/profile/'
    url = url + str(rest_id)
    url = url + '/search'
    covers = guest_count
    dateTime = res_time
    payload = {'covers': covers, 'dateTime': dateTime}
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    r = requests.post(url, params=payload, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    for tag in soup.select('.dtp-results-times li'):
        timeList.append(tag.string)
    times = '\nReservation Times: \n'
    for timeSlot in timeList:
        if timeSlot is not None:
            times = times + timeSlot + '\n'
    if len(times) <= 22:
        times = times + 'None available \n'
    return times


@app.route("/api/saveride", methods=["POST"])
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
    except IntegrityError:
        return jsonify(message="Ride already existed."), 409

    new_ride = UberRide.query.filter_by(userID=incoming["userID"]).first()
    # print(new_ride)
    return jsonify(
        rideID=new_ride.id, rideDisplay=new_ride.__repr__
    )


socketio = SocketIO(app)


@socketio.on('party_message')
def party_message(message):
    print('There was a party message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['username'])
    now = datetime.datetime.now().strftime('%H:%M:%S')
    partyId = message['partyId']
    print('This is the time: ' + str(now), file=sys.stderr)
    socketio.emit(message['partyname'] + str(partyId),
                  {'username': message['username'],
                   'text': message['msgtext'],
                   'avatar': avatar,
                   'time': now})
    # This is where the message should get inserted into database. Remove this
    # line.


def get_party_msg_his(partyID):
    # both curr_user and friend are the usernames that you want to retrieve
    # the message history of
    msg_list = PartyMessage.getPartyMessages(partyID)
    pass

def opentable_message(message, lat, lon):
    keylist = restaurants.keys()
    restname, resv_info = message.split('@')
    resv_time, partysize = resv_info.split('||')
    print('^^^^^^^^')
    print(restname)
    print(time)
    print(partysize)
    print('$$$$$$$$$')
    mtch = difflib.get_close_matches(restname.strip(), keylist, 1, 0.1)
    try:
        print(str(mtch))
        reply_text = ''
        if message != mtch[0]:
            reply_text = '\nCould not find ' + restname + '. Showing results for closest match: \n' + mtch[0] 
        rest_id = restaurants[mtch[0]]['Id']
        reply_text = '\n' + reply_text + mtch[0] + ' in ' + restaurants[mtch[0]]['Neighborhood']['Name'] + ', ' + restaurants[mtch[0]]['Region']['Name']  
        reply_text = reply_text + call_opentable(rest_id, partysize.strip(), resv_time)
        return reply_text
    except:
        return 'Could not find any restaurants close to that.'

def uber_message(message, lat, lon):
    return call_uber(message, lat, lon)

def get_bot_message(botname, message, lat, lon):
    if botname == constants.UBER_USERNAME:
        return uber_message(message, lat, lon)    
    elif botname == constants.OPENTABLE_USERNAME:
        return opentable_message(message, lat, lon)

@socketio.on('geodata')
def bot_message(message):
    bot_avatar = User.get_avatar_for_username(message['partyname'])
    text_reply = get_bot_message(message['partyname'], message['msgtext'], message['latitude'], message['longitude'])
    bot_now = datetime.datetime.now().strftime('%H:%M:%S')
    result2 = FriendMessage.add_friendMessage(message['partyname'], message['username'], bot_now, text_reply)
    if result2 == "success":
        socketio.emit(message['partyname'], {'username': message['partyname'], 'text': text_reply, 'avatar': bot_avatar, 'time': bot_now})
    else:
        print("Something happend with error in the database.")


@socketio.on('user2user_message')
def user2user_message(message):
    print('There was a user2user message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['sender'])
    now = datetime.datetime.now().strftime('%H:%M:%S')
    sender = message['sender']
    receiver = message['receiver']
    print('This is the time: ' + str(now), file=sys.stderr)
    # socketio.emit(message['partyname'], {'username': sender, 'text': message['msgtext'], 'avatar': avatar, 'time': now})
    # This is where the message should get inserted into database. Remove this
    # line.
    result = FriendMessage.add_friendMessage(
        sender, receiver, now, message['msgtext'])
    if result == "success":
        socketio.emit(message['partyname'], {'username': sender, 'text': message['msgtext'], 'avatar': avatar, 'time': now})
        if message['partyname'] in constants.BOTLIST:
            socketio.emit(sender+'__geo', {'partyname':message['partyname'], 'msgtext': message['msgtext']});
    else:
        print("Something happend with error in the database.")


@app.route("/api/friendhistory", methods=["POST"])
@requires_auth
def get_friend_msg_his():
    current_user = g.current_user['username']
    incoming = request.get_json()
    friend = incoming["friend"]
    # both current_user and friend are the usernames that you want to retrieve
    # the message history of
    msg_list = FriendMessage.getFriendMessages(current_user, friend)
    print(msg_list)
    return jsonify(msg_list)
