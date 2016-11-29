from index import db, bcrypt
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import desc
from .models import User

UBER_EMAIL='uber_aid@party.io'
OPENTABLE_EMAIL='opentable_aid@party.io'

