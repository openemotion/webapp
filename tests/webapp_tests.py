import sys
import unittest
from mock import patch
import flask
sys.path.append("..")
import webapp
from utils import dictobj
from pyquery import PyQuery
import json

def parse_json(text):
    return json.loads(text, object_hook=dictobj)

sample_conversation = dictobj(
    id=1,
    title="some title",
    slug="some_title",
    status="active",
    talker_name="me",
    listener_name="somebody",
    start_time_since="3 days ago"
)

sample_message = dictobj(
    id=1,
    author="me",
    text="some text"
)

@patch("webapp.Database")
class MainTests(unittest.TestCase):
    def setUp(self):
        webapp.app.config["DATABASE"] = ":memory:"
        webapp.app.config["TESTING"] = True
        self.app = webapp.app.test_client()

    def test_empty(self, Database):
        d = PyQuery(self.app.get('/').data)
        assert 0 == len(d(".conversation_link"))

    def test_one_conversation(self, Database):
        Database.return_value.conversations.get_all.return_value = [sample_conversation]
        d = PyQuery(self.app.get('/').data)
        assert 1 == len(d(".conversation_link"))
        assert "some title" == d(".title > a").html()

    def test_no_updates(self, Database):
        Database.return_value.conversations.get.return_value.status = "active"
        d = parse_json(self.app.get('/c/1/updates').data)
        assert d.status == "active"
        assert d.last_message_id == -1
        assert d.messages == []

    def test_updates(self, Database):
        Database.return_value.conversations.get.return_value = dictobj(sample_conversation)
        Database.return_value.messages.get_updates.return_value = [sample_message]
        d = parse_json(self.app.get('/c/1/updates').data)
        assert d.status == "active"
        assert d.last_message_id == 1
        assert len(d.messages) == 1
        assert d.messages == [sample_message]

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
