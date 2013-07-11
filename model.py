import re
from datetime import datetime
from contextlib import contextmanager
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm.collections import attribute_mapped_collection

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
    unread = db.relationship('Unread', collection_class=attribute_mapped_collection('conversation_id'))

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

    @classmethod
    def get_current(cls):
        from flask import session
        return cls.get(session.get('logged_in_user'))

    def set_last_read_message(self, conv, message_id):
        Unread.set(self.id, conv.id, message_id)

    def get_unread_conversations(self):
        result = []
        conversations = db.session.query(Conversation, db.func.max(Message.id)).join(Message).group_by(Conversation.id)
        conversations = conversations.order_by(Conversation.update_time.desc()).all()
        unread = db.session.query(Unread).filter(Unread.user_id == self.id)
        last_read_message_ids = dict((ur.conversation_id, ur.last_read_message_id) for ur in unread)
        for conv, last_message_id in conversations:
            if last_message_id > last_read_message_ids.get(conv.id, 0):
                result.append(conv)
        return result

    def get_my_unread_conversations(self):
        result = []
        for conv in self.get_unread_conversations():
            if conv.owner_id == self.id:
                result.append(conv)
        return result

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
        return '<Conversation(%s)>' % (self.id)

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
    def read_class(self):
        return '' if self.get_unread_messages(User.get_current()).count() else 'read'

    @property
    def unread_messages(self):
        return self.get_unread_messages(User.get_current(), include_last_read=True)

    def get_first_message(self):
        return self.messages.first()

    def get_last_message(self):
        return db.session.query(Message).filter_by(conversation_id=self.id).order_by(Message.id.desc()).first()

    def get_updated_messages(self, last_message_id, for_user=None):
        q = self.messages.filter(Message.id > last_message_id)
        if for_user:
            q = q.filter(Message.author_id != for_user.id)
        return q.all()

    def get_unread_messages(self, for_user, include_last_read=False):
        unread = Unread.get(for_user.id, self.id)
        last_read_message_id = unread.last_read_message_id if unread else 0
        if include_last_read:
            # return the last read message as well
            return self.messages.filter(Message.id >= last_read_message_id)
        else:
            return self.messages.filter(Message.id > last_read_message_id)

    def mark_read(self, user):
        if user:
            Unread.set(user.id, self.id, self.get_last_message().id)

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.update_time.desc()).all()

class Message(db.Model, Jsonable):
    __tablename__ = 'messages'

    class TYPE(object):
        TALKER = 'talker'
        LISTENER = 'listener'

    id = db.Column(db.Integer, primary_key=True)
    post_time = db.Column(db.DateTime, index=True)
    text = db.Column(db.String)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), index=True)
    conversation = db.relationship('Conversation', 
        backref=db.backref('messages', order_by=post_time, lazy='dynamic'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    author = db.relationship('User')

    def __init__(self, author, text, post_time=None):
        self.author = author
        self.text = text
        self.post_time = post_time or datetime.utcnow()

    def __repr__(self):
        return '<Message (%s)>' % (self.id)

    def __json__(self):
        data = super(Message, self).__json__()
        data['author'] = self.author.name
        data['type'] = self.type
        data['unescaped_text'] = self.unescaped_text
        return data

    @property
    def type(self):
        if not self.conversation:
            raise ValueError('message not connected to conversation')

        if self.author is self.conversation.owner:
            return Message.TYPE.TALKER
        else:
            return Message.TYPE.LISTENER

    @property
    def post_time_since(self):
        return utils.prettydate(self.post_time)

    @property
    def read_class(self):
        return '' if self.is_unread_by(User.get_current()) else 'read'

    @property
    def unescaped_text(self):
        return utils.unescape(self.text)

    def is_unread_by(self, user):
        unread = Unread.get(user.id, self.conversation_id)
        return unread is None or self.id > unread.last_read_message_id

class Unread(db.Model, Jsonable):
    __tablename__ = 'unread'
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'conversation_id'), {})

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), index=True)
    last_read_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), index=True)

    def __init__(self, user_id, conversation_id):
        self.user_id = user_id
        self.conversation_id = conversation_id

    def __repr__(self):
        return '<Unread (user=%s, conversation=%s, message=%s)>' % \
            (self.user_id, self.conversation_id, self.last_read_message_id)

    @classmethod
    def get(cls, user_id, conversation_id):
        return cls.query.filter_by(user_id=user_id, conversation_id=conversation_id).first()

    @classmethod
    def set(cls, user_id, conversation_id, last_read_message_id):
        unread = cls.get(user_id, conversation_id)
        if unread is None:
            unread = cls(user_id, conversation_id)
            db.session.add(unread)
        unread.last_read_message_id = last_read_message_id

@contextmanager
def temp_db_context(uri='sqlite:///:memory:', echo=False):
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
