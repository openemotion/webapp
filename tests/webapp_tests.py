# coding=utf8

import os
import sys
import json
import unittest
from datetime import datetime
from pyquery import PyQuery

sys.path.append('..')
os.environ['OPENEM_CONFIG'] = 'config.ut'
from webapp import app, db
from model import User, Conversation, Message

class Base(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.__enter__()
        db.drop_all()
        db.create_all()

        self.user1 = User('user1', '123456')
        self.user2 = User('user2', '123456')
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def tearDown(self):
        self.app_context.__exit__(None, None, None)

    def create_sample_conversation(self, title='some title'):
        self.conv = Conversation(self.user1, title)
        self.conv.messages.append(Message(self.user1, 'first message'))
        self.conv.messages.append(Message(self.user2, 'second message'))
        self.conv.messages.append(Message(self.user1, 'third message'))
        self.conv.messages.append(Message(self.user2, 'fourth message'))
        db.session.commit()

    def login(self, user):
        r = self.app.post('/login', data=dict(name=user.name, password='123456'), follow_redirects=True)
        assert r.status == '200 OK'

class ConversationsTests(Base):
    path = '/conversations'

    def test_no_conversations(self):
        r = self.app.get(self.path)
        d = PyQuery(r.data)
        assert len(d('.conversation_link')) == 0

    def test_one_conversation(self):
        self.create_sample_conversation()
        r = self.app.get(self.path)
        d = PyQuery(r.data)
        assert len(d('.conversation_link')) == 1
        assert d('.conversation_link > .title > a').attr('href') == '/conversations/1/some_title'
        assert d('.conversation_link > .title > a').html() == 'some title'

    def test_conversation_sorting(self):
        lastest = Conversation(self.user1, 'lastest', start_time=datetime(2013,1,1))
        Conversation(self.user1, 'last', start_time=datetime(2013,1,3))
        Conversation(self.user1, 'first', start_time=datetime(2013,1,1))
        Conversation(self.user1, 'middle', start_time=datetime(2013,1,2))
        lastest.update_time = datetime(2013,1,4)
        db.session.commit()

        r = self.app.get(self.path)
        d = PyQuery(r.data)
        assert len(d('.conversation_link')) == 4
        assert [e.text() for e in d('.conversation_link > .title > a').items()] == ['first', 'middle', 'last', 'lastest']

class IndexTests(ConversationsTests):
    path = '/'

    def test_logged_in(self):
        self.login(self.user1)
        r = self.app.get(self.path)
        d = PyQuery(r.data)
        assert  d('#login-links > a').eq(0).attr('href') == '/users/user1'

class AtomTests(Base):
    # /atom
    # /conversation/1/atom

    def test_atom(self):
        self.create_sample_conversation()
        data = self.app.get('/atom').data
        assert "http://www.w3.org/2005/Atom" in data

    def test_conversation_atom(self):
        self.create_sample_conversation()
        data = self.app.get('/conversations/1/atom').data
        assert "http://www.w3.org/2005/Atom" in data

class ConversationTests(Base):
    # /conversations/1/

    def setUp(self):
        super(ConversationTests, self).setUp()
        self.create_sample_conversation()

    def test_redirection(self):
        r = self.app.get('/conversations/1')
        assert r.location == 'http://localhost/conversations/1/'
        r = self.app.get('/conversations/1/')
        assert r.location == 'http://localhost/conversations/1/some_title'
        r = self.app.get('/conversations/1/incorrect_slug')
        assert r.location == 'http://localhost/conversations/1/some_title'
        r = self.app.get('/conversations/1/some_title')
        assert r.status == '200 OK'

    def test_not_found(self):
        r = self.app.get('/conversations/0/')
        assert r.status == '404 NOT FOUND'

    def test_pending(self):
        self.conv.status = Conversation.STATUS.PENDING
        db.session.commit()
        r = self.app.get('/conversations/1/some_title')
        d = PyQuery(r.data)
        assert d('.status').text() != ''

    def test_active(self):
        self.conv.status = Conversation.STATUS.ACTIVE
        db.session.commit()
        r = self.app.get('/conversations/1/some_title')
        d = PyQuery(r.data)
        assert not d('.status')

    def test_messages(self):
        r = self.app.get('/conversations/1/some_title')
        d = PyQuery(r.data)

        [e.text() for e in d('.message > .author').items()] == ['user1', 'user2', 'user1', 'user2']
        [e.text() for e in d('.message > .text').items()] == ['first message', 'second message', 'third message', 'fourth message']
        d('.message').eq(0).hasClass('talker')
        d('.message').eq(1).hasClass('listener')
        d('.message').eq(2).hasClass('talker')
        d('.message').eq(3).hasClass('listener')

class UpdatesTests(Base):
    # /convesations/1/updates
    def setUp(self):
        super(UpdatesTests, self).setUp()
        self.create_sample_conversation()

    def test_all(self):
        r = self.app.get('/conversations/1/updates')
        data = json.loads(r.data)
        assert data['conversation']['title'] == 'some title'
        assert len(data['messages']) == 4
        assert data['last_message_id'] == 4

    def test_partial(self):
        r = self.app.get('/conversations/1/updates?last_message_id=2')
        data = json.loads(r.data)
        assert data['conversation']['title'] == 'some title'
        assert len(data['messages']) == 2
        assert data['last_message_id'] == 4

    def test_logged_in(self):
        # login, only messages by other users should show
        self.login(self.user1)
        # get the updates (should only get new messages by other users)
        r = self.app.get('/conversations/1/updates')
        data = json.loads(r.data)

        assert data['conversation']['title'] == 'some title'
        assert len(data['messages']) == 2
        assert data['messages'][0]['text'] == 'second message'
        assert data['messages'][1]['text'] == 'fourth message'
        assert data['last_message_id'] == 4

class PostTests(Base):
    # /conversation/1/post [POST]
    
    def setUp(self):
        super(PostTests, self).setUp()
        self.create_sample_conversation()

    def test_not_logged_in(self):
        r = self.app.post('/conversations/1/post', follow_redirects=True)
        assert r.status == '403 FORBIDDEN'

    def test_bad_data(self):
        self.login(self.user1)
        r = self.app.post('/conversations/1/post', data=dict(foo='bar'), follow_redirects=True)
        assert r.status == '400 BAD REQUEST'

    def test_empty(self):
        self.login(self.user1)
        r = self.app.post('/conversations/1/post', data=dict(text=''), follow_redirects=True)
        assert r.status == '400 BAD REQUEST'

    def test_good_data(self):
        self.conv.update_time = datetime(2013,1,1)
        db.session.commit()

        self.login(self.user1)
        r = self.app.post('/conversations/1/post', data=dict(text='another message'), follow_redirects=True)
        assert r.status == '200 OK'
        r = self.app.get('/conversations/1/some_title')
        d = PyQuery(r.data)
        assert len(d('#history > .message')) == 5
        assert d('#history > .message > .text').eq(4).text() == 'another message'

        # make sure the conversation update_date was updated
        Conversation.query.get(self.conv.id).update_time != datetime(2013,1,1)

class NewConversationTests(Base):
    # /conversations/new

    def test_get_not_logged_in(self):
        r = self.app.get('/conversations/new')
        assert r.status == '403 FORBIDDEN'

    def test_get_logged_in(self):
        self.login(self.user1)
        r = self.app.get('/conversations/new')
        assert r.status == '200 OK'

    def test_post_not_logged_in(self):
        r = self.app.post('/conversations/new')
        assert r.status == '403 FORBIDDEN'

    def test_post(self):
        self.login(self.user1)
        r = self.app.post('/conversations/new', data=dict(message='new message', title='some title'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/conversations/1/'

        r = self.app.get('/conversations/1/some_title')
        d= PyQuery(r.data)
        assert len(d('#history > .message')) == 1
        assert d('#history > .message > .author').text() == 'user1'
        assert d('#history > .message > .text').text() == 'new message'
        assert d('h1').text() == 'some title'

    def test_post_empty_title(self):
        self.login(self.user1)
        r = self.app.post('/conversations/new', data=dict(message='new message', title=''))
        assert r.status == '400 BAD REQUEST'

    def test_post_empty_message(self):
        self.login(self.user1)
        r = self.app.post('/conversations/new', data=dict(message='', title='some title'))
        assert r.status == '400 BAD REQUEST'

class RegisterTests(Base):
    # /register
    def test_get(self):
        r = self.app.get('/register')
        assert r.status == '200 OK'

    def test_no_name(self):
        r = self.app.post('/register', data=dict(name='', password='', password2=''))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/register?error=no_name'

    def test_no_password(self):
        r = self.app.post('/register', data=dict(name='momo', password='', password2=''))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/register?name=momo&error=no_password'

    def test_no_password2(self):
        r = self.app.post('/register', data=dict(name='momo', password='123456', password2=''))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/register?name=momo&error=no_password2'

    def test_password_mismatch(self):
        r = self.app.post('/register', data=dict(name='momo', password='123456', password2='1234567'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/register?name=momo&error=password_mismatch'

    def test_existing_user(self):
        r = self.app.post('/register', data=dict(name='user1', password='123456', password2='123456'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/register?name=user1&error=user_exists'

    def test_good(self):
        r = self.app.post('/register', data=dict(name='momo', password='123456', password2='123456'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/'

    def test_unicode(self):
        r = self.app.post('/register', data=dict(name='אלי', password='אלי', password2='אלי'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/'

    def test_redirect(self):
        self.create_sample_conversation()
        r = self.app.post(
            '/register?goto=/conversations/1/post', 
            data=dict(name='momo', password='123456', password2='123456')
        )
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/conversations/1/post'

class LoginTests(Base):
    # /login
    def test_get(self):
        r = self.app.get('/login')
        assert r.status == '200 OK'

    def test_no_name(self):
        r = self.app.post('/login', data=dict(name='', password=''))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/login?error=no_name'

    def test_no_password(self):
        r = self.app.post('/login', data=dict(name='momo', password=''))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/login?name=momo&error=no_password'

    def test_no_user(self):
        r = self.app.post('/login', data=dict(name='momo', password='123456'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/login?name=momo&error=bad_password'

    def test_bad_password(self):
        momo = User('momo', '123456')
        db.session.add(momo)
        db.session.commit()
        r = self.app.post('/login', data=dict(name='momo', password='1234567'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/login?name=momo&error=bad_password'

    def test_good_login(self):
        momo = User('momo', '123456')
        db.session.add(momo)
        db.session.commit()
        r = self.app.post('/login', data=dict(name='momo', password='123456'))
        assert r.status == '302 FOUND'
        assert r.location == 'http://localhost/'

if __name__ == '__main__':
    import pytest
    pytest.main(['-s', '-v', __file__])