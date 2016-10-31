from flask import request, render_template, jsonify, url_for, redirect, g
from .models import User, Friendship
from index import app, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from .utils.auth import generate_token, requires_auth, verify_token


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


@app.route("/api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        username=incoming["username"],
        email=incoming["email"],
        password=incoming["password"],
        pgp_key=incoming["pgp_key"],
        avatar="placehold"  # waiting for Front-end pass-in
    )
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409
    new_user = User.query.filter_by(email=incoming["email"]).first()
    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )

@app.route("/api/user_add_friend", methods = ["POST"])
@requires_auth
def add_friendship():
    incoming = request.get_json()
    # friendemail refers to the email to be added email->friendemail
    friendee = User.query.filter_by(email=incoming["email"]).first()

    current_user = g.current_user
    if friendee == None:
        return jsonify(message="User with that email does not exist"), 409
    else:
        friender_email = current_user.email
        friender_id = current_user.id

        friendee_email = friendee.email
        friendee_id = friendee.id
        friendee_avatar = friendee.avatar
        newfriendship = Friendship(friender_id, friendee_id)

        db.session.add(newfriendship)
        try:
            db.session.commit()
        except SQLAlchemyError:
            return jsonify(message="That friendship already exits"), 410

        return jsonify(error = False, id = friendee_id, email = friendee_email, avatar = friendee_avatar)



@app.route("/api/createParty", methods = ["POST"])
@requires_auth
def createParty():
    incoming = request.get_json()
    party = Party(
        partyName=incoming["partyName"],
        ownerID=incoming["ownerID"]
    )
    db.session.add(party)
    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="Unable to create party"),409

    new_party = Party.query.filter_by(partyName=incoming["partyName"]).first()
    return jsonify(
        partyID=party.partyID
    )





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
