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

def return_values_iter(values):
    values_iter = iter(values)
    def next_value(*args, **kwargs):
        return values_iter.next()
    return next_value

sample_conversation = dictobj(
    id=1,
    title="some title",
    slug="some_title",
    status="active",
    talker_name="me",
    listener_name="somebody",
    start_time="2012-12-12 08:00:00",
    start_time_since="3 days ago"
)

sample_message = dictobj(
    id=1,
    author="me",
    text="some text",
    type="listener",
    timestamp="2012-12-12 08:00:00",
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
        Database.return_value.conversations.get.return_value = dictobj(status="active")
        d = parse_json(self.app.get('/conversations/1/updates').data)
        assert d.conversation.status == "active"
        assert d.last_message_id == -1
        assert d.messages == []

    def test_updates(self, Database):
        Database.return_value.conversations.get.return_value = dictobj(sample_conversation)
        Database.return_value.messages.get_updates.return_value = [sample_message]
        d = parse_json(self.app.get('/conversations/1/updates').data)
        assert d.conversation.status == "active"
        assert d.last_message_id == 1
        assert len(d.messages) == 1
        assert d.messages == [sample_message]

    def test_poll_with_updates(self, Database):
        Database.return_value.conversations.get.return_value = dictobj(sample_conversation)
        Database.return_value.messages.has_updates.return_value = True
        d = self.app.get('/conversations/1/poll').data
        assert d == "updated!"

    def test_poll_no_updates(self, Database):
        Database.return_value.conversations.get.return_value = dictobj(sample_conversation)
        Database.return_value.messages.has_updates.side_effect = return_values_iter([False, False, True])
        with patch("time.sleep") as sleep:
            d = self.app.get('/conversations/1/poll').data
            assert d == "updated!"
            assert sleep.call_count == 2

    def test_atom(self, Database):
        Database.return_value.conversations.get_all.return_value = [sample_conversation]
        Database.return_value.messages.get_by_conversation.return_value = [sample_message]
        data = self.app.get('/atom').data
        assert "http://www.w3.org/2005/Atom" in data

    def test_conversation_atom(self, Database):
        Database.return_value.messages.get_by_conversation.return_value = [
            sample_message,
            sample_message,
        ]
        data = self.app.get('/conversations/1/atom').data
        assert "http://www.w3.org/2005/Atom" in data

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
