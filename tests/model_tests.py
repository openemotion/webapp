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

class Base(unittest.TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.rollback()

class UserTests(Base):
    def test_create(self):
        u = User('user1', '123456')
        db.session.add(u)
        db.session.commit()
        [user] = User.query.all()
        assert user is u
        assert user.id == 1
        assert datetime.utcnow() - user.create_time < timedelta(0, 1)

    def test_conversations_none(self):
        u = User('user1', '123456')
        assert list(u.conversations) == []

    def test_conversations_one(self):
        u = User('user1', '123456')
        c = Conversation(u, 'some title')
        assert list(u.conversations) == [c]

    def test_messages(self):
        user1 = User('user1', '123456')
        user2 = User('user2', '123456')
        c = Conversation(user1, 'some title')
        c.messages.append(Message(user1, 'first message'))
        c.messages.append(Message(user2, 'first message'))
        assert c.messages[0].type == 'talker'
        assert c.messages[1].type == 'listener'

    def test_unique_names(self):
        db.session.add(User('user1', '123456'))
        db.session.add(User('user1', '123456'))
        with self.assertRaises(db.IntegrityError):
            db.session.commit()

    def test_unread_conversations(self):
        user = User('user', '123456')
        conv1 = Conversation(user, 'first conversation')
        conv1.messages.append(Message(user, 'first conversation message'))
        conv2 = Conversation(user, 'second conversation')
        conv2.messages.append(Message(user, 'second conversation message'))
        db.session.add(user)
        db.session.commit()

        user.set_last_read_message(conv2, conv2.messages[-1].id)
        db.session.commit()

        assert len(conv1.get_unread_messages(user)) == 1
        assert len(conv2.get_unread_messages(user)) == 0

        conversations = user.get_unread_conversations()
        assert len(conversations) == 1
        assert conversations[0].title == 'first conversation'

    def test_unread_two_users(self):
        user1 = User('user1', '123456')
        user2 = User('user2', '123456')
        db.session.add_all([user1, user2])

        conv1 = Conversation(user1, "conversation A")
        conv1.messages.append(Message(user1, "conversation A message 1"))
        conv1.messages.append(Message(user2, "conversation A message 2"))
        conv1.messages.append(Message(user1, "conversation A message 3"))
        conv1.messages.append(Message(user2, "conversation A message 4"))

        conv2 = Conversation(user2, "conversation B")
        conv2.messages.append(Message(user2, "conversation B message 1"))
        conv2.messages.append(Message(user1, "conversation B message 2"))
        conv2.messages.append(Message(user2, "conversation B message 3"))
        conv2.messages.append(Message(user1, "conversation B message 4"))

        db.session.commit()

class UnreadTests(Base):
    def setUp(self):
        super(UnreadTests, self).setUp()
        self.user1 = User('self.user1', '123456')
        self.user2 = User('self.user2', '123456')
        self.conv = Conversation(self.user1, 'some title')
        self.conv.messages.append(Message(self.user2, 'first message'))
        self.conv.messages.append(Message(self.user2, 'second message'))
        self.conv.messages.append(Message(self.user1, 'third message'))
        self.conv.messages.append(Message(self.user2, 'fourth message'))
        db.session.add_all([self.user1, self.user2])
        db.session.commit()

    def test_all_unread(self):
        messages = self.conv.get_unread_messages(for_user=self.user1)
        assert len(messages) == 4
        messages = self.conv.get_unread_messages(for_user=self.user2)
        assert len(messages) == 4

    def test_no_unread(self):
        self.user1.set_last_read_message(self.conv, message_id=4)
        db.session.commit()
        messages = self.conv.get_unread_messages(for_user=self.user1)
        assert len(messages) == 0

    def test_some_unread(self):
        self.user1.set_last_read_message(self.conv, message_id=2)
        self.user1.set_last_read_message(self.conv, message_id=3)
        user1messages = self.conv.get_unread_messages(for_user=self.user1)
        user2messages = self.conv.get_unread_messages(for_user=self.user2)
        [m.text for m in user1messages] == ['third message', 'fourth message']
        [m.text for m in user2messages] == ['fourth message']

    def test_mark_read(self):
        self.conv.mark_read(self.user1)
        db.session.commit()
        user1messages = self.conv.get_unread_messages(for_user=self.user1)
        assert len(user1messages) == 0

# FIXME: add tests for model.Message
# FIXME: add tests for model.Conversation

if __name__ == '__main__':
    with app.app_context():
        import pytest
        pytest.main(['-s', '-v', __file__])