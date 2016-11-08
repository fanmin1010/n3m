from testing_config import BaseTestConfig
from application.models import User
from application.models import Party
from application.models import PartyUser

class TestModels(BaseTestConfig):
    def test_get_user_with_email_and_password(self):
        self.assertTrue(
                User.get_user_with_email_and_password(
                        self.default_user["email"],
                        self.default_user["password"])
        )

    def test_getMyParties(self):
        self.assertTrue(
                Party.getMyParties(self.default_user["id"])
        )

    def test_getPartyUsers(self):
        self.assertTrue(
                PartyUser.getPartyUsers(self.default_party["partyID"])
        )
