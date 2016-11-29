from index import db, bcrypt
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import desc
from .models import User

uber = User.query.filter_by(username="uber_aid").first()
uber_id = uber.id

opentable = User.query.filter_by(username="opentable_aid").first()
opentable_id = opentable.id
