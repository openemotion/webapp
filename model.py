import re
from datetime import datetime
from contextlib import contextmanager
from flask.ext.sqlalchemy import SQLAlchemy

import utils

db = SQLAlchemy()

class Jsonable(object):
    def __json__(self):
        # put all data members into json representation
        return dict((k,v) for (k,v) in self.__dict__.iteritems() if not k.startswith('_sa_'))

class User(db.Model, Jsonable):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    create_time = db.Column(db.DateTime)

    def __init__(self, name, password, create_time=None):
        self.name = name
        self.password_hash = utils.encrypt_password(password, name)
        self.create_time = datetime.utcnow()

    def __repr__(self):
        return "<User('%s')>" % (self.name)

    @classmethod
    def get(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_or_404(cls, name):
        return cls.query.filter_by(name=name).first_or_404()

    @property
    def create_time_since(self):
        return utils.prettydate(self.create_time)

class Conversation(db.Model, Jsonable):
    __tablename__ = 'conversations'

    class STATUS(object):
        PENDING = 'pending'
        ACTIVE = 'active'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, index=True)
    update_time = db.Column(db.DateTime, index=True)
    title = db.Column(db.String)
    status = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    owner = db.relationship('User', backref=db.backref('conversations', lazy='dynamic'))

    def __init__(self, owner, title, status=STATUS.PENDING, start_time=None):
        self.owner = owner
        self.title = title
        self.status = status
        self.start_time = start_time or datetime.utcnow()
        self.update_time = self.start_time

    def __repr__(self):
        return '<Conversation(%d)>' % (self.id)

    @property
    def start_time_since(self):
        return utils.prettydate(self.start_time)

    @property
    def update_time_since(self):
        return utils.prettydate(self.update_time)

    @property
    def slug(self):
        return re.compile('\W+', re.UNICODE).sub('_', self.title)

    @property
    def unread(self):
        return ''

    def get_first_message(self):
        return self.messages.first()

    def get_updated_messages(self, last_message_id, for_user=None):
        q = self.messages.filter(Message.id > last_message_id)
        if for_user:
            q = q.filter(Message.author_id != for_user.id)
        return q.all()

class Message(db.Model, Jsonable):
    __tablename__ = 'messages'

    class TYPE(object):
        TALKER = 'talker'
        LISTENER = 'listener'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    text = db.Column(db.String)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), index=True)
    conversation = db.relationship('Conversation', 
        backref=db.backref('messages', order_by=timestamp, lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    author = db.relationship('User')

    def __init__(self, author, text, timestamp=None):
        self.author = author
        self.text = text
        self.timestamp = timestamp or datetime.utcnow()

    def __repr__(self):
        return '<Message (%d)>' % (self.id)

    def __json__(self):
        data = super(Message, self).__json__()
        data['author'] = self.author.name
        data['type'] = self.type
        return data

    @property
    def type(self):
        if not self.conversation:
            raise ValueError('message not connected to conversation')

        if self.author is self.conversation.owner:
            return Message.TYPE.TALKER
        else:
            return Message.TYPE.LISTENER


@contextmanager
def temp_db_context(uri, echo=False):
    from flask import Flask
    app = Flask('dummy')
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_ECHO'] = echo
    db.init_app(app)
    with app.app_context():
        yield db

def add_sql_errors(db):
    """
    Adds exception classes from SQLAlchemy to the SQLAlchemy objects
    so we can catch SQL exceptions easily with i.e. except db.IntegrityError.
    """
    import sqlalchemy.exc
    for name in dir(sqlalchemy.exc):
        cls = getattr(sqlalchemy.exc, name)
        if isinstance(cls, type) and name.endswith('Error'):
            setattr(db, name, getattr(sqlalchemy.exc, name))
add_sql_errors(db)

if __name__ == '__main__':
    with temp_db_context('sqlite:///:memory:') as db:
        db.create_all()
