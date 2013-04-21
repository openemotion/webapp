import re
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm.exc import NoResultFound

import utils

class Model(object):
    def __json__(self):
        return dict((k,v) for (k,v) in self.__dict__.iteritems() if not k.startswith('_sa_'))

Session = sessionmaker()
Base = declarative_base(cls=Model)

# FIXME: change api to classmethods on model classes (User, Conversation, etc.)
# FIXME: set up creation and initializion of database (i.e. initdb script)
# FIXME: use Flask-SQLAlchemy

# FIXME: remove formatting function for db
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

def parse_date(s):
    if "." not in s:
        s += ".000000"
    return datetime.strptime(s, DATE_FORMAT)

def format_date(d):
    return datetime.strftime(d, DATE_FORMAT)

class Database(object):
    def __init__(self, filename):
        self.engine = create_engine('sqlite:///%s' % filename)
        # FIXME: session definition should be elsewhere
        self.session = Session(bind=self.engine)

        self.users = Users(self)
        self.conversations = Conversations(self)
        self.messages = Messages(self)

    def init(self):
        Base.metadata.create_all(self.engine)

    def close(self):
        pass

# =================================================================================================

class Collection(object):
    def __init__(self, db):
        self.db = db

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    # FIXME: name should be unique
    name = Column(String)
    password_hash = Column(String)
    create_time = Column(DateTime)

    def __init__(self, name, password_hash, create_time):
        self.name = name
        # FIXME: encrypt password here, not outside
        # self.password_hash = utils.encrypt_password(password, self.name)
        self.password_hash = password_hash
        self.create_time = create_time

    def __repr__(self):
        return "<User('%s')>" % (self.name)

class Users(Collection):
    def get(self, name):
        try:
            return self.db.session.query(User).filter_by(name=name).one()
        except NoResultFound:
            raise KeyError("no user with name %s" % name)

    def save(self, name, password_hash):
        user = User(name, password_hash, datetime.now())
        self.db.session.add(user)
        # FIXME: what about transactions?
        self.db.session.commit()
        return user.id

class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    _update_time = Column(DateTime, name='update_time')
    # FIXME: use the user_id and a foreign key here
    talker_name = Column(String)
    title = Column(String)
    status = Column(String)

    def __init__(self, talker_name, title):
        self.talker_name = talker_name
        self.title = title
        self.status = Conversations.STATUS_PENDING
        self.start_time = datetime.now()

    def __repr__(self):
        return "<Conversation(%d)>" % (self.id)

    @property
    def update_time(self):
        if self._update_time:
            return self._update_time.strftime(DATE_FORMAT)
        else:
            return self.start_time.strftime(DATE_FORMAT)

    @update_time.setter
    def update_time(self, value):
        self._update_time = value

    @property
    def start_time_since(self):
        return utils.prettydate(self.start_time)

    @property
    def update_time_since(self):
        if self._update_time:
            time = self._update_time
        else:
            time = self.start_time
        return utils.prettydate(time)

    @property
    def slug(self):
        return re.compile('\W+', re.UNICODE).sub('_', self.title)

    @property
    def unread(self):
        return ''

class Conversations(Collection):
    STATUS_PENDING = "pending"
    STATUS_ACTIVE = "active"

    def get(self, id):
        try:
            return self.db.session.query(Conversation).filter_by(id=id).one()
        except NoResultFound:
            raise KeyError("no conversation with id %d" % id)

    def save(self, talker_name, title):
        # FIXME: pull up into base class
        conv = Conversation(talker_name, title)
        self.db.session.add(conv)
        # FIXME: what about transactions?
        self.db.session.commit()
        return conv.id

    def get_all(self):
        return self.db.session.query(Conversation)

    def get_by_talker(self, talker_name):
        return self.db.session.query(Conversation).filter_by(talker_name=talker_name)

    def get_all_with_unread(self, current_user):
        # FIXME: this is a stub
        return self.get_all()

    def get_by_talker_with_unread(self, talker_name, current_user):
        # FIXME: this is a stub
        return self.get_all()

    def update(self, id, status=None, update_time=None):
        try:
            conv = self.db.session.query(Conversation).filter_by(id=id).one()
        except NoResultFound:
            pass
            # FIXME: raise error when the object to update wasn't found
            # raise KeyError("no conversation with id %d" % id)
        else:
            if status:
                conv.status = status
            if update_time:
                conv.update_time = update_time
            # FIXME: what about transactions?
            self.db.session.commit()

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    timestamp = Column(DateTime)

    # FIXME: convert to a relationship?
    author = Column(String)
    type = Column(String)
    text = Column(String)

    # conversation = relationship('Conversation', backref=backref('messages', order_by=timestamp))

    def __init__(self, conversation_id, author, type, text):
        self.conversation_id = conversation_id
        self.author = author
        self.type = type
        self.text = text

    def __repr__(self):
        return '<Message (%d)>' % (self.id)

class Messages(Collection):
    TYPE_TALKER = "talker"
    TYPE_LISTENER = "listener"

    def get_by_conversation(self, conversation_id):
        return self.db.session.query(Message).filter_by(conversation_id=conversation_id)

    def get_first(self, conversation_id):
        message = self.db.session.query(Message).filter_by(conversation_id=conversation_id).first()
        if message is None:
            raise KeyError("no messages for conversation with id %d" % conversation_id)
        else:
            return message

    def get_updates(self, conversation_id, current_user, after_message_id):
        return self.db.session.query(Message).filter(Message.author != current_user).filter(Message.id > after_message_id)

    def has_updates(self, conversation_id, current_user, after_message_id):
        return self.get_updates(conversation_id, current_user, after_message_id).count() > 0

    def save(self, conversation_id, author, type, text):
        msg = Message(conversation_id, author, type, text)
        msg.timestamp = datetime.now()
        self.db.session.add(msg)
        # FIXME: what about transactions?
        self.db.session.commit()
        return msg.id
