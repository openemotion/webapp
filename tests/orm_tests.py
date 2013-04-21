import sys
import unittest
from datetime import datetime
sys.path.append('..')

from orm import Database

class DbTests(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')
        self.db.init()

class UserTests(DbTests):
    def test_save_get(self):
        user_id = self.db.users.save('eli', '12345678a')
        assert user_id == 1
        user = self.db.users.get('eli')
        assert user.name == 'eli'
        # FIXME: should be equal to hash, not to password
        # assert user.password_hash == utils.encrypt_password('eli', '12345678')
        assert user.password_hash == '12345678a'

    def test_get_not_found(self):
        with self.assertRaises(KeyError):
            self.db.users.get('eli')

    def test_save_existing(self):
        # duplicates are allowed
        # FIXME: duplicates should not be allowed
        uid1 = self.db.users.save('eli', '12345678a')
        uid2 = self.db.users.save('eli', '12345678b')
        assert uid1 == 1
        assert uid2 == 2

class ConversationTests(DbTests):
    def test_save_get(self):
        conv_id = self.db.conversations.save('eli', 'something to talk about')
        assert conv_id == 1
        conv = self.db.conversations.get(1)
        assert conv.id == 1
        assert conv.talker_name == 'eli'
        assert conv.title == 'something to talk about'
        assert conv.status == 'pending'

    def test_get_not_found(self):
        with self.assertRaises(KeyError):
            self.db.users.get(1)

    def test_save_existing(self):
        # duplicates are allowed
        cid1 = self.db.conversations.save('eli', 'something to talk about')
        cid2 = self.db.conversations.save('eli', 'something to talk about')
        assert cid1 == 1
        assert cid2 == 2

    def test_get_all_empty(self):
        convs = self.db.conversations.get_all()
        assert list(convs) == []

    def test_get_all(self):
        cid1 = self.db.conversations.save('eli', 'something to talk about')
        cid2 = self.db.conversations.save('moshe', 'something else to talk about')
        convs = self.db.conversations.get_all()
        convs = list(convs)
        assert len(convs) == 2
        assert convs[0].id == cid1
        assert convs[0].talker_name == 'eli'
        assert convs[0].title == 'something to talk about'
        assert convs[1].id == cid2
        assert convs[1].talker_name == 'moshe'
        assert convs[1].title == 'something else to talk about'

    def test_get_by_talker(self):
        cid1 = self.db.conversations.save('eli', 'something to talk about')
        cid2 = self.db.conversations.save('moshe', 'something else to talk about')
        convs = self.db.conversations.get_by_talker('moshe')
        convs = list(convs)
        assert len(convs) == 1
        assert convs[0].id == cid2
        assert convs[0].talker_name == 'moshe'
        assert convs[0].title == 'something else to talk about'

    def test_get_by_talker_not_found(self):
        convs = self.db.conversations.get_by_talker('moshe')
        convs = list(convs)
        assert len(convs) == 0

    def test_update_status(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.conversations.update(cid, status='active')
        conv = self.db.conversations.get(cid)
        assert conv.status == 'active'

    def test_update_update_time(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.conversations.update(cid, update_time=datetime(2013, 1, 1))
        conv = self.db.conversations.get(cid)
        # FIXME: should return a datetime object
        assert conv.update_time == '2013-01-01 00:00:00.000000'
        assert conv.status == 'pending'

    def test_update_both(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.conversations.update(cid, status='active', update_time=datetime(2013, 1, 1))
        conv = self.db.conversations.get(cid)
        assert conv.update_time == '2013-01-01 00:00:00.000000'
        assert conv.status == 'active'

    def test_update_not_found(self):
        # FIXME: should raise an error if not found
        # with self.assertRaises(KeyError):
        self.db.conversations.update(1, status='active', update_time=datetime(2013, 1, 1))

    # def get_all_with_unread(self, current_user):
    # def get_by_talker_with_unread(self, talker_name, current_user):

class MessageTests(DbTests):
    def test_get_by_conversation_not_found(self):
        messages = self.db.messages.get_by_conversation(1)
        messages = list(messages)
        assert messages == []

    def test_get_by_conversation(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        mid = self.db.messages.save(cid, 'eli', 'talker', 'something to say')
        messages = self.db.messages.get_by_conversation(cid)
        messages = list(messages)
        assert mid == 1
        assert len(messages) == 1
        assert messages[0].author == 'eli'
        assert messages[0].text == 'something to say'
        assert messages[0].conversation_id == cid
        assert messages[0].timestamp != None

    def test_get_first(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.messages.save(cid, 'eli', 'talker', 'first message')
        self.db.messages.save(cid, 'eli', 'talker', 'second message')
        message = self.db.messages.get_first(cid)
        assert message.author == 'eli'
        assert message.text == 'first message'
        assert message.timestamp != None

    def test_get_first_not_found(self):
        with self.assertRaises(KeyError):
            message = self.db.messages.get_first(1)

    def test_get_updates(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        mid = self.db.messages.save(cid, 'eli', 'talker', 'first message')
        self.db.messages.save(cid, 'moshe', 'listener', 'second message')

        updates = self.db.messages.get_updates(cid, 'eli', mid)
        updates = list(updates)
        assert len(updates) == 1
        assert updates[0].author == 'moshe'
        assert updates[0].text == 'second message'

    def test_get_updates_all(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.messages.save(cid, 'eli', 'talker', 'first message')
        self.db.messages.save(cid, 'moshe', 'listener', 'second message')
        self.db.messages.save(cid, 'eli', 'talker', 'third message')

        updates = list(self.db.messages.get_updates(cid, None, 0))
        messages = list(self.db.messages.get_by_conversation(cid))
        assert updates == messages

    def test_get_updates_none(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.messages.save(cid, 'eli', 'talker', 'first message')
        self.db.messages.save(cid, 'moshe', 'listener', 'second message')
        mid = self.db.messages.save(cid, 'eli', 'talker', 'third message')

        updates = list(self.db.messages.get_updates(cid, None, mid))
        assert len(updates) == 0

    def test_has_updates(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        mid = self.db.messages.save(cid, 'eli', 'talker', 'first message')
        self.db.messages.save(cid, 'moshe', 'listener', 'second message')

        assert self.db.messages.has_updates(cid, 'eli', mid)

    def test_has_updates_none(self):
        cid = self.db.conversations.save('eli', 'something to talk about')
        self.db.messages.save(cid, 'eli', 'talker', 'first message')
        mid = self.db.messages.save(cid, 'moshe', 'listener', 'second message')

        assert not self.db.messages.has_updates(cid, 'eli', mid)

if __name__ == '__main__':
    unittest.main()
