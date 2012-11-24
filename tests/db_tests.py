import sys
import unittest
sys.path.append("..")
from db import Database
from utils import dictobj

class DbTests(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.init()
        assert list(self.db.conversations.get_all()) == []
        self.db.conversations.save("eli", "some conversation")

    def test_load(self):
        conversations = list(self.db.conversations.get_all())
        assert len(conversations) == 1
        assert conversations[0].id == 1
        assert conversations[0].status == u"pending"
        assert conversations[0].slug == u"some_conversation"
        assert conversations[0].title == u"some conversation"
        assert conversations[0].talker_name == u"eli"
        assert conversations[0].listener_name == None

    def test_update(self):
        self.db.conversations.update(1, "active", "moshe")
        conversations = list(self.db.conversations.get_all())
        assert len(conversations) == 1
        assert conversations[0].id == 1
        assert conversations[0].status == u"active"
        assert conversations[0].slug == u"some_conversation"
        assert conversations[0].title == u"some conversation"
        assert conversations[0].talker_name == u"eli"
        assert conversations[0].listener_name == u"moshe"

    def test_update_not_found(self):
        # FIXME: should probably raise an exception
        self.db.conversations.update(2, "active", "moshe")

    def test_get(self):
        conv = self.db.conversations.get(1)
        assert conv.id == 1
        assert conv.status == u"pending"
        assert conv.slug == u"some_conversation"
        assert conv.title == u"some conversation"
        assert conv.talker_name == u"eli"
        assert conv.listener_name == None

    def test_get_not_found(self):
        with self.assertRaises(KeyError):
            self.db.conversations.get(2)

    def test_get_by_talker(self):
        self.db.conversations.save("moshe", "some other conversation")
        assert len(list(self.db.conversations.get_by_talker("eli"))) == 1
        assert len(list(self.db.conversations.get_by_talker("moshe"))) == 1
        assert len(list(self.db.conversations.get_by_talker("shaul"))) == 0

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
