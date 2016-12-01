from testing_config import BaseTestConfig
from application.models import User, Friendship, Party #, UberRide
import json
from application.utils import auth


class TestAPI(BaseTestConfig):
    some_user = {
        "user_id": 6,
        "username": "theone",
        "email": "one@gmail.com",
        "password": "something1",
        "pgp_key": "nJCzzlSEZT1u+qS1Mrj9MNqmNlL pdW5YJJ2aRsaspz1mCR3+NUP78a2iDnTHPaCh+jRK+P5IORJ4Qtpv6CITRz8St7z Z2j3TMtywQgAsZUVKLPujiO9/V9bNp2xjN23JS8CwT3GPlvR1HeJfVDuiE2njNlj enu6ZrU3z5E6gyMmUjUHEsgS3ZGv1+FdUCYYT5ry8js/kcly49tziI0WC6hrQBpC i7tiBXmT/9TYJhJdsQaQptjloQQDwObO7g7L2UOwLTuzLDh3xnnWuvfO90yz/1hu LlpEkNvJh02G7iL7bZPNPKzp16e9Xk8PfxhW3pjh09W3PBx8MpNOkjWN27/Q+Khm rfhYWBomlwauMHH1Yq+gxqzALf0/JNwGOW+vXbavc7PmaM3GQjZanAE8pdxqqiGl ZQ6y0TK/F6xikLudO/eeSvVlddmgnlh+TA== =Yks1"
    }
    another_user = {
        "user_id": 7,
        "username": "Aria",
        "email": "starks@gmail.com",
        "password": "assassin10",
        "pgp_key": " A7G9oJkhLyI3vWhIDnZXvKCkDtTJJjvWCJsUUh4vCY7behNqex5AVcGADs6V0ngn HC1O42TIBUyVXriNBFIhxbQBBADMnyH4Pwh/79SrAEuh88eXl0JLA+9JLcDfQWtC YMsx89R1zLvVJHEdLVCuX2U5ES01b6o1MXi8CEdPHJcWALqmbz0Q4TS//f9qwRKC TPtzy0gGlBZde5J7sk0ksFXgbnE6UODa84aEMh1jB9iJQ4zblRsVOdvmiKlSRC4/ sCRfYwARAQABiQG9BBgBAgAJBQJSIcW0AhsuAKgJEDMnZjdEvIiTnSAEGQECAAYF AlIhxbQACgkQWDaU/OSCATxPZQQAuY+O6Ccc58EkdSXsbT2c72EGWt94pspduUS9 Fs+UO5rfi3aw11xo6jr46gnU7QUvljYrChr1XnJCzzlSEZT1u+qS1Mrj9MNqmNlL pdW5YJJ2aRsaspz1mCR3+NUP78a2iDnTHPaCh+jRK+P5IORJ4Qtpv6CITRz8St7z Z2j3TMtywQgAsZUVKLPujiO9/V9bNp2xjN23JS8CwT3GPlvR1HeJfVDuiE2njNlj enu6ZrU3z5E6gyMmUjUHEsgS3ZGv1+FdUCYYT5ry8js/kcly49tziI0WC6hrQBpC i7tiBXmT/9TYJhJdsQaQptjloQQDwObO7g7L2UOwLTuzLDh3xnnWuvfO90yz/1hu LlpEkNvJh02G7iL7bZPNPKzp16e9Xk8PfxhW3pjh09W3PBx8MpNOkjWN27/Q+Khm rfhYWBomlwauMHH1Yq+gxqzALf0/JNwGOW+vXbavc7PmaM3GQjZanAE8pdxqqiGl ZQ6y0TK/F6xikLudO/eeSvVlddmgnlh+TA== =Yks1"
    }
    friendship = {
        "email": "starks@gmail.com"
    }
    friendship2 = {
        "email": "999@gmail.com"
    }
    party1 = {
        "party_name": "Awesome Fellas"
    }

    def test_get_spa_from_index(self):
        result = self.app.get("/")
        self.assertIn('<html>', result.data.decode("utf-8"))

    def test_get_spaother_from_index(self):
        result = self.app.get("/<path:path>")
        self.assertIn('<html>', result.data.decode("utf-8"))

    def test_create_new_user(self):
        self.assertIsNone(User.query.filter_by(
                email=self.some_user["email"]
        ).first())

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        self.assertTrue(json.loads(res.data.decode("utf-8"))["token"])
        self.assertEqual(User.query.filter_by(email=self.some_user["email"]).first().email, self.some_user["email"])

        res2 = self.app.post(
                "/api/create_user",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )

        self.assertEqual(res2.status_code, 409)

    def test_create_user_without_username(self):
        usr = {
            "username": "",
            "email": "brokenuser@noway.com",
            "password": "something1",
            "pgp_key": ""
        }

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_short_username(self):
        usr = {
            "username": "bu",
            "email": "brokenuser@noway.com",
            "password": "something1",
            "pgp_key": ""
        }
        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_long_username(self):
        usr = {
            "username": "a-broken-user-with-too-long-of-a-username",
            "email": "brokenuser@noway.com",
            "password": "something1",
            "pgp_key": ""
        }
        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_without_email(self):
        usr = {
            "username": "brokenuser",
            "email": "",
            "password": "something1",
            "pgp_key": ""
        }

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_invalid_email(self):
        usr = {
            "username": "brokenuser",
            "email": "broken@user",
            "password": "something1",
            "pgp_key": ""
        }

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_without_password(self):
        usr = {
            "username": "brokenuser",
            "email": "broken@user.com",
            "password": "",
            "pgp_key": ""
        }

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_short_password(self):
        usr = {
            "username": "brokenuser",
            "email": "broken@user.com",
            "password": "short",
            "pgp_key": ""
        }

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)

    def test_create_user_with_long_password(self):
        usr = {
            "username": "brokenuser",
            "email": "broken@user.com",
            "password": "passwordlongerthantwenty",
            "pgp_key": ""
        }

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(usr),
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 400)


    def test_get_token_and_verify_token(self):
        res = self.app.post(
                "/api/get_token",
                data=json.dumps(self.default_user),
                content_type='application/json'
        )

        token = json.loads(res.data.decode("utf-8"))["token"]
        self.assertTrue(auth.verify_token(token))
        self.assertEqual(res.status_code, 200)

        res2 = self.app.post(
                "/api/is_token_valid",
                data=json.dumps({"token": token}),
                content_type='application/json'
        )

        self.assertTrue(json.loads(res2.data.decode("utf-8")), ["token_is_valid"])

        res3 = self.app.post(
                "/api/is_token_valid",
                data=json.dumps({"token": token + "something-else"}),
                content_type='application/json'
        )

        self.assertEqual(res3.status_code, 403)

        res4 = self.app.post(
                "/api/get_token",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )

        self.assertEqual(res4.status_code, 403)

    def test_protected_route(self):
        headers = {
            'Authorization': self.token,
        }

        bad_headers = {
            'Authorization': self.token + "bad",
        }

        response = self.app.get('/api/user', headers=headers)
        self.assertEqual(response.status_code, 200)
        response2 = self.app.get('/api/user')
        self.assertEqual(response2.status_code, 401)
        response3 = self.app.get('/api/user', headers=bad_headers)
        self.assertEqual(response3.status_code, 401)

    def test_add_friendship(self):
        self.test_get_token_and_verify_token()
        headers = {
            'content_type':'application/json',
            'Authorization': self.token
        }
        self.assertIsNone(User.query.filter_by(
                email=self.another_user["email"]
        ).first())

        res = self.app.post(
                "/api/create_user",
                data=json.dumps(self.some_user),
                content_type='application/json'
        )
        res = self.app.post(
                "/api/create_user",
                data=json.dumps(self.another_user),
                content_type='application/json'
        )
        res3 = self.app.post(
                "/api/user_add_friend",
                data=json.dumps(self.friendship),
                headers = headers,
                content_type='application/json'
        )
        self.assertEqual(res3.status_code, 200)

        res4 = self.app.post(
                "/api/user_add_friend",
                headers = headers,
                data=json.dumps(self.friendship2),
                content_type='application/json'
        )
        self.assertEqual(res4.status_code, 403)
        res5 = self.app.post(
                "/api/user_add_friend",
                data=json.dumps(self.friendship),
                headers = headers,
                content_type='application/json'
        )
        self.assertEqual(res5.status_code, 409)
    def test_create_party(self):

        headers = {
            'content_type':'application/json',
            'Authorization': self.token
        }
        res = self.app.post(
                "/api/createparty",
                data=json.dumps(self.party1),
                headers = headers,
                content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        res2 = self.app.post(
                "/api/createparty",
                data=json.dumps(self.party1),
                headers = headers,
                content_type='application/json'
        )
        self.assertEqual(res2.status_code, 409)

    def test_add_users_to_party(self):
        headers = {
            'content_type':'application/json',
            'Authorization': self.token
        }
        res = self.app.post(
            "/api/add_users_to_party",
            data=json.dumps({
                "party_id": 1,
                "username": "secuser"
            }),
            headers = headers,
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)

        res3 = self.app.post(
            "/api/add_users_to_party",
            data=json.dumps({
                "party_id": 2,
                "username": "secuser"
            }),
            headers = headers,
            content_type='application/json'
        )
        self.assertEqual(res3.status_code, 404)
        res4 = self.app.post(
            "/api/add_users_to_party",
            data=json.dumps({
                "party_id": "1",
                "username": "fake"
            }),
            headers = headers,
            content_type='application/json'
        )
        self.assertEqual(res4.status_code, 403)
        res2 = self.app.post(
            "/api/add_users_to_party",
            data=json.dumps({
                "party_id": 1,
                "username": "secuser"
            }),
            headers = headers,
            content_type='application/json'
        )
        self.assertEqual(res2.status_code, 409)

    def test_get_friendlist(self):
        headers = {
            'content_type':'application/json',
            'Authorization': self.token
        }
        res = self.app.get(
                "/api/friendlist",
                data=json.dumps({}),
                headers = headers,
                content_type='application/json'
        )
        print(json.loads(res.data.decode("utf-8")))

        self.assertEqual(res.status_code, 200)


    def test_get_partylist(self):
        headers = {
            'content_type':'application/json',
            'Authorization': self.token
        }
        res = self.app.get(
                "/api/partylist",
                data=json.dumps({}),
                headers = headers,
                content_type='application/json'
        )
        print(json.loads(res.data.decode("utf-8")))
        self.assertEqual(res.status_code, 200)

"""
    def test_getRides(self):
        headers = {
            'content_type':'application/json',
            'Authorization':self.token
        }
        res = self.app.get(
                "/api/
"""
