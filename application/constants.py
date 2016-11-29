from index import db, bcrypt
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import desc
from .models import User

uber = User.query.filter_by(email='uber_aid@party.io').first()
uber_id = uber.id
print(uber_id)

opentable = User.query.filter_by(email='opentable_aid@party.io').first()
opentable_id = opentable.id
