import sys
import unittest
sys.path.append("..")
from db import Database, parse_date
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

    def test_update(self):
        self.db.conversations.update(1, "active")
        conversations = list(self.db.conversations.get_all())
        assert len(conversations) == 1
        assert conversations[0].id == 1
        assert conversations[0].status == u"active"
        assert conversations[0].slug == u"some_conversation"
        assert conversations[0].title == u"some conversation"
        assert conversations[0].talker_name == u"eli"

    def test_update_not_found(self):
        # FIXME: should probably raise an exception
        self.db.conversations.update(2, "active")

    def test_update_update_time(self):
        self.db.conversations.update(1, update_time=parse_date("2012-12-22 08:00:00"))
        conversations = list(self.db.conversations.get_all())
        assert len(conversations) == 1
        assert conversations[0].update_time == u"2012-12-22 08:00:00"
        assert conversations[0].status == u"pending"

    def test_get(self):
        conv = self.db.conversations.get(1)
        assert conv.id == 1
        assert conv.status == u"pending"
        assert conv.slug == u"some_conversation"
        assert conv.title == u"some conversation"
        assert conv.talker_name == u"eli"

    def test_get_not_found(self):
        with self.assertRaises(KeyError):
            self.db.conversations.get(2)

    def test_get_by_talker(self):
        self.db.conversations.save("moshe", "some other conversation")
        assert len(list(self.db.conversations.get_by_talker("eli"))) == 1
        assert len(list(self.db.conversations.get_by_talker("moshe"))) == 1
        assert len(list(self.db.conversations.get_by_talker("shaul"))) == 0

class VisitTests(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.init()

    def test(self):
        assert 0 == len(list(self.db.visits.get_by_user('eli')))
        self.db.visits.save(1, 'eli', parse_date("2012-12-22 08:00:00"))
        assert 1 == len(list(self.db.visits.get_by_user('eli')))
        self.db.visits.save(1, 'eli', parse_date("2012-12-22 08:10:00"))
        assert 1 == len(list(self.db.visits.get_by_user('eli')))
        self.db.visits.save(2, 'eli', parse_date("2012-12-22 08:10:00"))
        assert 2 == len(list(self.db.visits.get_by_user('eli')))

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
