import sys
import unittest
from datetime import datetime, timedelta
from flask import Flask

sys.path.append('..')
from model import db, User, Conversation, Message

app = Flask('dummy')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
# app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)

class UserTests(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()

    def test_create(self):
        u = User('eli', '12345678')
        db.session.commit()
        [user] = User.query.all()
        assert user is u
        assert user.id == 1
        assert datetime.now() - user.create_time < timedelta(0, 1)

    def test_conversations_none(self):
        u = User('eli', '12345678')
        assert u.conversations == []

    def test_conversations_one(self):
        u = User('eli', '12345678')
        c = Conversation(u, 'some title')
        assert u.conversations == [c]

    def test_messages(self):
        eli = User('eli', '12345678')
        moshe = User('moshe', '87654321')
        c = Conversation(eli, 'some title')
        m1 = Message(c, eli, 'first message')
        m2 = Message(c, moshe, 'first message')
        assert m1.type == 'talker'
        assert m2.type == 'listener'
        assert c.messages == [m1, m2]
        assert m1.conversation == c
        assert m2.conversation == c

if __name__ == '__main__':
    with app.app_context():
        import pytest
        pytest.main(["-s", __file__])