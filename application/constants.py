from index import db, bcrypt
from datetime import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import desc
from .models import User

# This values in this file are also duplicated in js under the constants dir.
UBER_EMAIL='uber_aid@party.io'
UBER_USERNAME='uber_aid'
OPENTABLE_EMAIL='opentable_aid@party.io'
OPENTABLE_USERNAME='opentable_aid'
BOTLIST=['uber_aid','opentable_aid']
