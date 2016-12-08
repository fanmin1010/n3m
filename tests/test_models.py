from testing_config import BaseTestConfig
from application.models import User, Friendship, FriendMessage, PartyMessage
from application.models import Party
from application.models import PartyUser
import datetime, time
# from application.models import UberRide

class TestModels(BaseTestConfig):
    def test_get_user_with_email_and_password(self):
        self.assertTrue(
                User.get_user(
                        self.default_user["email"],
                        self.default_user["password"])
        )
    def test_get_avatar_for_user(self):
        self.assertTrue(
                User.get_avatar_for_useremail(
                        self.default_user["email"])
        )
        self.assertFalse(
                User.get_avatar_for_useremail(
                        "fake@fake.com")
        )
        self.assertTrue(
                User.get_avatar_for_username(
                        self.default_user["username"])
        )
        self.assertFalse(
                User.get_avatar_for_username(
                        "fake")
        )

    def test_get_friendship_with_user_ids(self):
        default_user = User.get_user(self.default_user["email"], self.default_user["password"])
        print('Testing User __str___ : ' + str(default_user))
        u_two = User.get_user(self.d_user_two["email"], self.d_user_two["password"])
        self.assertTrue(
            Friendship.get_friendship_with_user_ids(default_user.user_id, u_two.user_id)
        )
        self.assertTrue("Friendship" in repr(Friendship.get_friendship_with_user_ids(default_user.user_id, u_two.user_id)))
        self.assertFalse(
            Friendship.get_friendship_with_user_ids(10101, 10102)
        )
    def test_get_all_friendship_of_user(self):
        default_user = User.get_user(self.default_user["email"], self.default_user["password"])
        self.assertTrue(
            Friendship.get_all_friendship_of_user(default_user.user_id)
        )
        u_three = User.get_user(self.d_user_three["email"], self.d_user_three["password"])
        self.assertEqual(
            len(Friendship.get_all_friendship_of_user(u_three.user_id)), 2
        )

    def test_getMyParties(self):
        default_user = User.get_user(self.default_user["email"], self.default_user["password"])
        u_two = User.get_user(self.d_user_two["email"], self.d_user_two["password"])
        self.default_user["user_id"]=default_user.user_id
        self.d_user_two["user_id"]=u_two.user_id
        self.assertTrue(
                Party.get_my_parties(self.default_user["user_id"])
        )
        self.assertFalse(Party.get_my_parties(self.d_user_two["user_id"]))
        for party in Party.get_my_parties(self.default_user["user_id"]):
            self.assertTrue("Party" in repr(party))
    def test_getPartyUsers(self):
        party = Party.query.filter_by(owner_id=self.default_user["user_id"], party_name=self.default_party["party_name"]).first()
        self.assertTrue(PartyUser.get_party_users(party.party_id))
        self.assertFalse(PartyUser.get_party_users(10101))

    def test_add_and_get_friendMessage(self):
        sender = self.default_user["username"]
        receiver = self.d_user_two["username"]
        other = self.d_user_three["username"]
        res0 = FriendMessage.get_friend_messages(sender, receiver)
        self.assertFalse(res0)
        messagetext = "hello"
        replytext = "hello back"
        res1 = FriendMessage.add_friend_message("nulluser", receiver, messagetext)
        self.assertEqual(res1, "empty sender user")
        res2 = FriendMessage.add_friend_message(sender, "nulluser", messagetext)
        self.assertEqual(res2, "empty receiver user")
        result = FriendMessage.add_friend_message(sender, receiver, messagetext)
        self.assertEqual(result, "success")
        result = FriendMessage.add_friend_message(receiver, sender, replytext)
        self.assertEqual(result, "success")
        result = FriendMessage.add_friend_message(receiver, other, replytext)
        self.assertEqual(result, "empty friendship")
        result = FriendMessage.get_friend_messages(sender, receiver)
        self.assertTrue(result)
        result = FriendMessage.get_friend_messages(receiver, sender)
        self.assertTrue(result)

    def test_bad_user_get_friend_messages(self):
        sender = self.default_user["username"]
        receiver = self.d_user_two["username"]
        result = FriendMessage.get_friend_messages('badusername', receiver)
        self.assertEqual(result, "empty user1")
        result = FriendMessage.get_friend_messages(sender, 'badusername')
        self.assertEqual(result, "empty user2")
    
    
    def test_users_not_friends_get_friend_messages(self):
        sender = self.default_user["username"]
        receiver = self.d_user_three["username"]
        result = FriendMessage.get_friend_messages(sender, receiver)
        self.assertEqual(result, "empty friendship")

    def test_add_and_get_partyMessage(self):
        sender = self.default_user
        party = self.default_party
        res0 = PartyMessage.get_party_messages(party["party_id"])
        self.assertFalse(res0)
        messagetext = "hello"
        res = PartyMessage.add_party_message(party["party_id"], sender["username"], messagetext)
        self.assertEqual(res, "success")
        res2 = PartyMessage.add_party_message(party["party_id"], 'badusername', messagetext)
        self.assertEqual(res2, 'empty sender user')
        res3 = PartyMessage.add_party_message(party["party_id"], sender['username'], messagetext)
        result = PartyMessage.get_party_messages(party["party_id"])
        print('resutl from call to get_party_messages: ')
        print(result)
        self.assertTrue(len(result)==2)

"""
    def test_getRides(self):
        self.assertTrue(
                UberRide.getRides(self.default_user["user_id"])
        )
        self.assertFalse(UberRide.getRides(self.d_user_two["user_id"]))
        for ride in UberRide.getRides(self.default_user["user_id"]):
            self.assertTrue("UberRide" in repr(ride))
"""

"""
    def test_PartyMessages(self):
        self.assertTrue(
                PartyMessage(self.default_party["party_id"],self.default_user["user_id"],"2016-11-08 00:00:00","My Message")
        )

    def test_getPartyMessages(self):
        self.assertTrue(
                PartyMessage.get_party_messages(self.default_party["party_id"])
        )
"""
