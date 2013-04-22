import re
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy

import utils

db = SQLAlchemy()

class User(db.Model, utils.Jsonable):
    __tablename__ = 'users'

    # FIXME: name should be unique

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password_hash = db.Column(db.String)
    create_time = db.Column(db.DateTime)

    def __init__(self, name, password_hash):
        self.name = name
        # FIXME: encrypt password here, not outside
        # self.password_hash = utils.encrypt_password(password, self.name)
        self.password_hash = password_hash
        self.create_time = datetime.now()
        db.session.add(self)

    def __repr__(self):
        return "<User('%s')>" % (self.name)

class Conversation(db.Model, utils.Jsonable):
    __tablename__ = 'conversations'

    STATUS_PENDING = 'pending'
    STATUS_ACTIVE = 'active'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    title = db.Column(db.String)
    status = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', backref=db.backref('conversations'))

    def __init__(self, owner, title):
        self.owner = owner
        self.title = title
        self.status = self.STATUS_PENDING
        self.start_time = datetime.now()
        db.session.add(self)

    def __repr__(self):
        return '<Conversation(%d)>' % (self.id)

    @property
    def start_time_since(self):
        return utils.prettydate(self.start_time)

    @property
    def update_time_since(self):
        return utils.prettydate(self.update_time or self.start_time)

    @property
    def slug(self):
        return re.compile('\W+', re.UNICODE).sub('_', self.title)

    @property
    def unread(self):
        return ''

class Message(db.Model, utils.Jsonable):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    text = db.Column(db.String)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))
    conversation = db.relationship('Conversation', backref=db.backref('messages'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User')

    def __init__(self, conversation, author, text):
        self.conversation = conversation
        self.author = author
        self.text = text
        db.session.add(self)

    def __repr__(self):
        return '<Message (%d)>' % (self.id)

    @property
    def type(self):
        if self.author is self.conversation.owner:
            return 'talker'
        else:
            return 'listener'

if __name__ == '__main__':
    from flask import Flask
    app = Flask('dummy')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_ECHO'] = 'True'
    db.init_app(app)
    with app.app_context():
        db.create_all()