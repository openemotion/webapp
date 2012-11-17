import sys
import unittest
from mock import patch
import flask
sys.path.append("..")
import webapp
from utils import dictobj
from pyquery import PyQuery

@patch("webapp.Database")
class WebAppTestCase(unittest.TestCase):

    def setUp(self):
        webapp.app.config["DATABASE"] = ":memory:"
        webapp.app.config["TESTING"] = True
        self.app = webapp.app.test_client()

    def test_empty(self, db):
        pq = PyQuery(self.app.get('/').data)
        assert 0 == len(pq(".conversation_link"))

    def test_one_conversation(self, db):
        db.return_value.conversations.get_all.return_value = [dict(id=1, title="some title")]
        pq = PyQuery(self.app.get('/').data)
        assert 1 == len(pq(".conversation_link"))
        assert "some title" == pq(".title > a").html()

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
