import re
import sqlite3
from datetime import datetime
import utils

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

class Database(object):
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.conversations = Conversations(self.connection)
        self.users = Users(self.connection)
        self.messages = Messages(self.connection)

    def close(self):
        self.connection.close()

class Conversations(object):
    STATUS_PENDING = "pending"
    STATUS_ACTIVE = "active"

    def __init__(self, connection):
        self.connection = connection

    def _make_obj(self, id, start_time, talker_name, listener_name, title, status):
        obj = utils.dictobj()
        obj.id = id
        obj.start_time = parse_date(start_time)
        obj.talker_name = talker_name
        obj.listener_name = listener_name
        obj.title = title
        obj.status = status
        obj.start_time_since = utils.prettydate(obj.start_time)
        obj.slug = re.compile("\W+", re.UNICODE).sub("_", obj.title)
        return obj

    def get_all(self):
        cmd = "select id, start_time, talker_name, listener_name, title, status from conversations order by start_time desc"
        cur = self.connection.execute(cmd)
        for row in cur:
            yield self._make_obj(*row)

    def get_by_talker(self, name):
        cmd = "select id, start_time, talker_name, listener_name, title, status from conversations where talker_name = ? order by start_time desc"
        cur = self.connection.execute(cmd, [name])
        for row in cur:
            yield self._make_obj(*row)

    def get(self, id):
        cmd = "select id, start_time, talker_name, listener_name, title, status from conversations where id = ?"
        cur = self.connection.execute(cmd, [id])
        for row in cur:
            return self._make_obj(*row)
        raise KeyError("no conversation with id %s" % id)

    def save(self,  talker_name, title):
        cur = self.connection.execute("insert into conversations (talker_name, title, status) values (?, ?, ?)",
            [talker_name, title, self.STATUS_PENDING])
        self.connection.commit()
        return cur.lastrowid

    def update(self, id, status, listener_name):
        self.connection.execute("update conversations set status = ?, listener_name = ? where id = ?",
            [status, listener_name, id])
        self.connection.commit()

class Messages(object):
    def __init__(self, connection):
        self.connection = connection

    def _make_obj(self, conversation_id, id, timestamp, author, text):
        obj = utils.dictobj()
        obj.conversation_id = conversation_id
        obj.id = id
        obj.timestamp = parse_date(timestamp)
        obj.author = author
        obj.text = text
        return obj

    def get_by_conversation(self, conversation_id):
        cmd = "select conversation_id, id, timestamp, author, text from messages where conversation_id = ? order by timestamp"
        cur = self.connection.execute(cmd, [conversation_id])
        for row in cur:
            yield self._make_obj(*row)

    def get_first(self, conversation_id):
        for obj in self.get_by_conversation(conversation_id):
            return obj
        raise KeyError("no messages for convesation with id %s" % conversation_id)

    def get_updates(self, conversation_id, current_user, after_message_id):
        # FIXME: may not work with current_user == None
        cmd = "select conversation_id, id, timestamp, author, text from messages "\
              "where conversation_id = ? and author <> ? and id > ? order by timestamp"
        cur = self.connection.execute(cmd, [conversation_id, current_user, after_message_id])
        for row in cur:
            yield self._make_obj(*row)

    def save(self, conversation_id, author, text):
        cur = self.connection.execute("insert into messages (conversation_id, author, text) values (?, ?, ?)",
            [conversation_id, author, text])
        self.connection.commit()
        return cur.lastrowid

class Users(object):
    def __init__(self, connection):
        self.connection = connection

    def _make_obj(self, name, password_hash, create_time):
        obj = utils.dictobj()
        obj.name = name
        obj.password_hash = password_hash
        obj.create_time = parse_date(create_time)
        obj.create_time_since = utils.prettydate(obj.create_time)
        return obj

    def get(self, name):
        cmd = "select name, password_hash, create_time from users where name = ?"
        cur = self.connection.execute(cmd, [name])
        for row in cur:
            return self._make_obj(*row)
        raise KeyError("no user with name %s" % name)

    def save(self, name, password_hash):
        cur = self.connection.execute("insert into users (name, password_hash) values (?, ?)",
            [name, password_hash])
        self.connection.commit()
        return cur.lastrowid
