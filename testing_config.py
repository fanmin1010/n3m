from flask_testing import TestCase
from application.app import app, db
from application.models import User
import os
from setup import basedir
import json
import application.constants as constants

class BaseTestConfig(TestCase):
    default_user = {
        "id": 1,
        "username": "thesecond",
        "email": "default@gmail.com",
        "password": "something2",
        "pgp_key": "=Yks1"
    }
    d_user_two = {
        "id": 2,
        "username": "secuser",
        "email": "default2@gmail.com",
        "password": "something3",
        "pgp_key": " rfhYWBomlwauMHH1Yq+gxqzALf0/JNwGOW+vXbavc7PmaM3GQjZanAE8pdxqqiGl ZQ6y0TK/F6xikLudO/eeSvVlddmgnlh+TA== =Yks1"
    }
    d_user_three = {
        "id": 3,
        "username": "thirduser",
        "email": "default3@gmail.com",
        "password": "something4",
        "pgp_key": "rKflcno7 LHgtR4I6LHuQProGOQoj/naZzMPfGkhfIkPOe1aSnTtJbWcfhY6VB7wiD4cw7p4D hSeSIkko7dqYLQaae9WryFcJd/gZt0IuRfheWFKfFPlYc0JG3D7Nt0mExJsdGO58 tpdiDSmkUQHTVbPtdTRKpPJ5drF+rDcAfmK1lpUZuStlHirxGzQiTvMHfaGiqhKl voQJxVlZiHi6vUPcp9lpSa9QUuYP0vQjaRFrUF8S3B3dZqRy4C+nG48ukNm1BBel A7G9oJkhLyI3vWhIDnZXvKCkDtTJJjvWCJsUUh4vCY7behNqex5AVcGADs6V0ngn HC1O42TIBUyVXriNBFIhxbQBBCANnyH4Pwh/79SrAEuh88eXl0JLA+9JLcDfQWtC YMsx89R1zLvVJHEdLVCuX2U5ES01b6o1MXi8CEdPHJcWALqmbz0Q4TS//f9qwRKC TPtzy0gGlBZde5J7sk0ksFXgbnE6UODa84aEMh1jB9iJQ4zblRsVOdvmiKlSRC4/ sCRfYwARAQABiQG9BBgBAgAJBQJSIcW0AhsuAKgJEDMnZjdEvIiTnSAEGQECAAYF AlIhxbQACgkQWDaU/OSCATxPZQQAuY+O6Ccc58EkdSXsbT2c72EGWt94pspduUS9 Fs+UO5rfi3aw11xo6jr46gnU7QUvljYrChr1XnJCzzlSEZT1u+qS1Mrj9MNqmNlL pdW5YJJ2aRsaspz1mCR3+NUP78a2iDnTHPaCh+jRK+P5IORJ4Qtpv6CITRz8St7z Z2j3TMtywQgAsZUVKLPujiO9/V9bNp2xjN23JS8CwT3GPlvR1HeJfVDuiE2njNlj enu6ZrU3z5E6gyMmUjUHEsgS3ZGv1+FdUCYYT5ry8js/kcly49tziI0WC6hrQBpC i7tiBXmT/9TYJhJdsQaQptjloQQDwObO7g7L2UOwLTuzLDh3xnnWuvfO90yz/1hu LlpEkNvJh02G7iL7bZPNPKzp16e9Xk8PfxhW3pjh09W3PBx8MpNOkjWN27/Q+Khm rfhYWBomlwauMHH1Yq+gxqzALf0/JNwGOW+vXbavc7PmaM3GQjZanAE8pdxqqiGl ZQ6y0TK/F6xikLudO/eeSvVlddmgnlh+TA== =Yks1"
    }

    default_party = {
        "partyID": 1,
        "partyName": "My Party"
    }
    
    uber_user = {
        "username": "uber_aid",
        "email":  constants.UBER_EMAIL,
        "password": "uber_pwd",
        "pgp_key": "uberpgp"
    }

    opentable_user = {
        "username": "opentable_aid",
        "email": constants.OPENTABLE_EMAIL,
        "password": "opentable_pwd",
        "pgp_key": "opentablepgp"
    }

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.create_all()

        res_uber = self.app.post(
                "/api/create_user",
                data=json.dumps(self.uber_user),
                content_type='application/json'
        )
        res_opentable = self.app.post(
                "/api/create_user",
                data=json.dumps(self.opentable_user),
                content_type='application/json'
        )

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(self.default_user),
                content_type='application/json'
        )
        self.token = json.loads(res.data.decode("utf-8"))["token"]
        res2 = self.app.post(
                "/api/create_user",
                data=json.dumps(self.d_user_two),
                content_type='application/json'
        )

        res3 = self.app.post(
                "/api/create_user",
                data=json.dumps(self.d_user_three),
                content_type='application/json'
        )
      
      
        headers = {
            'content_type':'application/json',
            'Authorization': self.token
        }

        f_res = self.app.post(
                "/api/user_add_friend",
                headers = headers,
                data=json.dumps(self.d_user_two),
                content_type='application/json'
        )
        self.fs_id = json.loads(f_res.data.decode("utf-8"))["friendship_id"]
        p_res = self.app.post(
            "/api/createParty",
            data=json.dumps(self.default_party),
            headers = headers,
            content_type='application/json'
        )
        pu_res = self.app.post(
            "/api/add_users_to_party",
            data=json.dumps({
                "partyName": "My Party",
                "email": "default3@gmail.com"
            }),
            headers = headers,
            content_type='application/json'
        )


    def tearDown(self):
        db.session.remove()
        db.drop_all()
