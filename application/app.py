'''CONTROLLER'''
from __future__ import print_function
import datetime
import time
import json
import re
import sys
import os
import difflib
from random import randint
import requests
import geocoder
from flask import request, render_template, jsonify, g
from flask_socketio import SocketIO
from index import app, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from bs4 import BeautifulSoup
import application.constants as constants
from application.OpenTable import restaurants
from .utils.auth import generate_token, requires_auth, verify_token
from .models import User, Friendship, Party, PartyUser, FriendMessage, PartyMessage


socketio = SocketIO(app)


@app.route('/', methods=['GET'])
def index():
    '''default redirection to index.html'''
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    '''default redirection to index.html'''
    print(path)
    return render_template('index.html')


@app.route("/api/user", methods=["GET"])
@requires_auth
def get_user():
    '''return session user'''
    return jsonify(result=g.current_user)


@app.route("/api/friendlist", methods=["GET"])
@requires_auth
def get_friendlist():
    '''get firends of current user'''
    current_user = g.current_user
    result = db.engine.execute(
        '''select u.user_id, u.avatar, u.username from friendship f ''' +
        '''join "user" u  on f.friendee=u.user_id where f.friender = ''' +
        str(
            current_user["user_id"]))
    return json.dumps([dict(r) for r in result])


@app.route("/api/create_user", methods=["POST"])
def create_user():
    '''create a new user based on passed info and link to api bots'''
    incoming = request.get_json()
    uname = incoming["username"]
    eml = incoming["email"]
    pswd = incoming["password"]
    pgp = incoming["pgp_key"]
    eml_rgx = r"[^@]+@[^@]+\.[^@]+"

    if not uname:
        return jsonify(message='Username cannot be null.'), 400
    elif len(uname) < 3:
        return jsonify(message='Username must be at least 3 characters.'), 400
    elif len(uname) > 20:
        return jsonify(
            message='Username must be no more than 20 characters.'), 400
    elif not eml:
        return jsonify(message='Email cannot be null.'), 400
    elif not re.match(eml_rgx, eml):
        return jsonify(message='Email address not valid.'), 400
    elif not pswd:
        return jsonify(message='Password cannot be null.'), 400
    elif len(pswd) < 6:
        return jsonify(message='Password must be at least 6 characters.'), 400
    elif len(pswd) > 20:
        return jsonify(
            message='Password must be no more than 20 characters.'), 400
    else:
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
        '''create friendship between user and api bots to be able to
        display api responses in chat'''
        if new_user.email in bot_emails:
            return None
        bot = User.query.filter_by(email=botemail).first()
        newfriendship = Friendship(new_user.user_id, bot.user_id)
        newfriendship2 = Friendship(bot.user_id, new_user.user_id)
        db.session.add(newfriendship)
        db.session.commit()
        db.session.add(newfriendship2)
        db.session.commit()
        return

    bot_emails = [constants.UBER_EMAIL, constants.OPENTABLE_EMAIL]
    for email in bot_emails:
        mk_friend(email)

    return jsonify(
        id=user.user_id,
        token=generate_token(new_user)
    ), 201


@app.route("/api/user_add_friend", methods=["POST"])
@requires_auth
def add_friendship():
    '''create firendship between current user and passed friend'''
    incoming = request.get_json()
    # friendemail refers to the email to be added email->friendemail
    db.session.commit()
    friendee = User.query.filter_by(email=incoming["email"]).first()
    # new_user = User.query.filter_by(email="starks@gmail.com").first()

    current_user = g.current_user
    if friendee is None:
        return jsonify(message="User with that email does not exist"), 403
    else:
        friender_id = current_user["user_id"]

        friendee_email = friendee.email
        friendee_id = friendee.user_id
        print('CurrentUserID: ' + str(friender_id) + ', FriendId: ' + str(friendee_id))
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


@app.route("/api/createparty", methods=["POST"])
@requires_auth
def create_party():
    '''create a new party for a given user/owner'''
    incoming = request.get_json()
    # print('The partyname is')
    # print(incoming)
    av_path = "dist/images/team0{}.png".format(randint(0, 9))
    if len(incoming["party_name"]) == 0:
        return jsonify(
            error=True, message="Party name cannot be empty."
        ), 400
    party = Party(
        party_name=incoming["party_name"],
        owner_id=g.current_user["user_id"],
        avatar=av_path
    )
    db.session.add(party)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Party already existed."), 409

    new_party = party
    return jsonify(
        party_id=new_party.party_id, party_name=new_party.party_name
    )


@app.route("/api/partylist", methods=["GET"])
@requires_auth
def get_partylist():
    '''retrieve all parties for a user'''
    current_user = g.current_user
    result = db.engine.execute(
        '''select *
        from party
        where "owner_id" = {}
        UNION
        select p."party_id", p."party_name", p."owner_id", p."avatar"
        from party p
        join partyuser pu on p."party_id"=pu."party_id"
        where pu."user_id" ={}'''.format(
            current_user["user_id"],
            current_user["user_id"]))
    # result=Party.query.filter_by(owner_id=current_user).all()
    parties = json.dumps([dict(r) for r in result])
    print(str(parties), file=sys.stderr)
    return parties


@app.route("/api/add_users_to_party", methods=["POST"])
@requires_auth
def add_to_party():
    ''' add user to a party'''
    incoming = request.get_json()
    party = Party.query.filter_by(
        party_id=incoming["party_id"]).first()
    # print(party)
    if not party:
        return jsonify(message="Party does not exist."), 404
    user = User.query.filter_by(username=incoming["username"]).first()
    if not user:
        return jsonify(message="User does not exist."), 403
    party_user = PartyUser(party.party_id, user.user_id)
    db.session.add(party_user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Party user relation already exists."), 409
    socketio.emit(incoming["username"] + '_newparty', {})
    return jsonify(status="success", avatar=user.avatar,
                   email=user.email, name=user.username)


@app.route("/api/get_token", methods=["POST"])
def get_token():
    '''create token for new user or retrieve existing'''
    incoming = request.get_json()
    if incoming["email"] == 'uber_aid@party.io' or incoming[
            "email"] == 'opentable_aid@party.io':
        return jsonify(error=True), 403
    user = User.get_user(
        incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))
    return jsonify(error=True), 403


@app.route("/api/is_token_valid", methods=["POST"])
def is_token_valid():
    '''validate passed token'''
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True), 202
    else:
        return jsonify(token_is_valid=False), 403


def call_uber(end_address, lat, lng):
    ''' call uber api with destination and position'''
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
        'end_longitude': endlong}
    headers = {
        'Authorization': 'Token x4maHB7QT8tWJqKfkfPVyzWfpbp7g5QmehniOIf5',
        'Content-Type': 'application/json',
        'Accept-Language': 'en_US'}
    api_result = requests.get(url, params=payload, headers=headers)
    json_data = json.loads(api_result.text)
    reply_text = '\n'
    for price in json_data['prices']:
        reply_text = reply_text + \
            price['display_name'] + ': ' + price['estimate'] + '\n'
    return reply_text


def call_opentable(rest_id, guest_count, res_time):
    ''' makes a request to the open table api for available reservation times '''
    timelist = []
    url = 'http://www.opentable.com/restaurant/profile/'
    url = url + str(rest_id)
    url = url + '/search'
    covers = guest_count
    date_time = res_time
    payload = {'covers': covers, 'dateTime': date_time}
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    api_result = requests.post(url, params=payload, headers=headers)
    soup = BeautifulSoup(api_result.text, 'html.parser')

    for tag in soup.select('.dtp-results-times li'):
        timelist.append(tag.string)
    times = '\nReservation Times: \n'
    for time_slot in timelist:
        if time_slot is not None:
            times = times + time_slot + '\n'
    if len(times) <= 22:
        times = times + 'None available \n'
    return times


def party_message_internal(message):
    '''display party message in chat'''
    print('There was a party message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['username'])
    now = datetime.datetime.now().strftime('%H:%M:%S')
    party_id = message['party_id']
    print('This is the time: ' + str(now), file=sys.stderr)
    result = None
    if message['party_id'] != -1:
        result = PartyMessage.add_party_message(
            party_id, message['username'], message['msgtext'])
    if result == "success" or message['party_id'] == -1:
        socketio.emit(message['party_name'],
                      {'username': message['username'],
                       'text': message['msgtext'],
                       'avatar': avatar,
                       'time': now})
    else:
        print("Something happend with error in the database.")
    # This is where the message should get inserted into database. Remove this
    # line.


@socketio.on('party_message')
def party_message(message):
    party_message_internal(message)


@app.route("/api/partyhistory", methods=["POST"])
@requires_auth
def get_party_msg_his():
    '''returns the history of messages for a specific party'''
    incoming = request.get_json()
    party_id = incoming["party_id"]
    msg_list = PartyMessage.get_party_messages(party_id)
    return jsonify(msg_list)


def opentable_message(message):
    '''call opentable api and return response'''
    keylist = restaurants.keys()
    if (message.count('@') != 1) or (message.count('||') != 1):
        return 'Incorrect input for OpenTable reservation.'
    restname, resv_info = message.split('@')
    resv_time, partysize = resv_info.split('||')

    print('^^^^^^^^')
    print(restname)
    print(resv_time)
    print(partysize)
    print('$$$$$$$$$')
    try:
        resv_time = resv_time.strip()
        partysize = partysize.strip()
        datetime.datetime.strptime(resv_time, '%Y-%m-%d %H:%M')
        int(partysize)
    except Exception, e:
        print(str(e))
        return 'Incorrect input for OpenTable reservation.'

    mtch = difflib.get_close_matches(restname.strip(), keylist, 1, 0.1)
    try:
        print(str(mtch))
        reply_text = ''
        if restname != mtch[0]:
            reply_text = '\nCould not find ' + restname + \
                '. Showing results for closest match: \n'
        rest_id = restaurants[mtch[0]]['Id']
        reply_text = '\n' + reply_text + mtch[0] + ' in '
        reply_text = reply_text + restaurants[mtch[0]][ 'Neighborhood']['Name']
        reply_text = reply_text + ', ' + restaurants[mtch[0]]['Region']['Name']
        reply_text = reply_text + call_opentable(rest_id, partysize.strip(), resv_time)
        return reply_text
    except Exception as e:
        print(e.__doc__)
        print(e.message)
        return 'Could not find any restaurants close to that.'


def uber_message(message, lat, lon):
    '''forward uber api response from uber'''
    return call_uber(message, lat, lon)


def get_bot_message(botname, message, lat, lon):
    '''call api based on userbot and forward response'''
    if botname == constants.UBER_USERNAME:
        return uber_message(message, lat, lon)
    elif botname == constants.OPENTABLE_USERNAME:
        return opentable_message(message)


def bot_message(message):
    '''display api response in chat'''
    bot_avatar = User.get_avatar_for_username(message['receiver'])
    text_reply = get_bot_message(
        message['receiver'],
        message['msgtext'],
        message['latitude'],
        message['longitude'])
    bot_now = datetime.datetime.now().strftime('%H:%M:%S')
    print('got past the get_bot_message_call')
    result2 = FriendMessage.add_friend_message(
        message['receiver'], message['username'], text_reply)
    print('got result back from adding griend message')
    print(json.dumps(result2))
    if result2 == "success":
        socketio.emit(message['party_name'],
                      {'username': message['receiver'],
                       'text': text_reply,
                       'avatar': bot_avatar,
                       'time': bot_now})
    else:
        print("Something happend with error in the database.")

@socketio.on('geodata')
def geo_data(message):
    bot_message(message)


@app.route("/test/geodata", methods=["POST"])
@requires_auth
def test_geo_data():
    incoming = request.get_json()
    print('made it to the inside of the test geodata function')
    print(str(incoming))
    try:
        bot_message(incoming)
        return jsonify(status="success")
    except:
        return jsonify(error=True), 403


def user2user_internal(message):
    '''send message between two friends'''
    print('There was a user2user message: ' + str(message), file=sys.stderr)
    avatar = User.get_avatar_for_username(message['sender'])
    print('The avatar is: ')
    print(avatar)
    now = datetime.datetime.now().strftime('%H:%M:%S')
    sender = message['sender']
    receiver = message['receiver']
    print('This is the time: ' + str(now), file=sys.stderr)
    result = FriendMessage.add_friend_message(
        sender, receiver, message['msgtext'])
    print('Result of adding Friend Message:')
    print(result)
    if result == "success":
        socketio.emit(message['party_name'],
                      {'username': sender,
                       'text': message['msgtext'],
                       'avatar': avatar,
                       'time': now})
        if message['receiver'] in constants.BOTLIST:
            socketio.emit(sender + '__geo',
                          {'party_name': message['party_name'],
                           'receiver': receiver,
                           'msgtext': message['msgtext']})
    else:
        print("Something happend with error in the database.")


@socketio.on('user2user_message')
def user2user_message(message):
    user2user_internal(message)
    
@app.route("/test/user2usermessage", methods=["POST"])
@requires_auth
def test_user2user_message():
    incoming = request.get_json()
    print('made it toe the inside of the test user2user message function')
    print(str(incoming))
    try:
        user2user_internal(incoming)
        return jsonify(status="success")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify(error=True), 403

@app.route("/test/party_message", methods=["POST"])
@requires_auth
def test_party_message():
    incoming = request.get_json()
    print('made it toe the inside of the test party message function')
    print(str(incoming))
    try:
        party_message_internal(incoming)
        return jsonify(status="success")
    except:
        return jsonify(error=True), 403

@app.route("/api/friendhistory", methods=["POST"])
@requires_auth
def get_friend_msg_his():
    '''returns the message history between two friends'''
    current_user = g.current_user['username']
    incoming = request.get_json()
    friend = incoming["friend"]
    # both current_user and friend are the usernames that you want to retrieve
    # the message history of
    msg_list = FriendMessage.get_friend_messages(current_user, friend)
    print(msg_list)
    return jsonify(msg_list)
