import re
import os
import sqlite3
from datetime import datetime
import utils

root_dir = os.path.dirname(__file__)

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def format_date(d):
    return datetime.strftime(d, "%Y-%m-%d %H:%M:%S")

class Database(object):
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.conversations = Conversations(self)
        self.users = Users(self)
        self.messages = Messages(self)
        self.visits = Visits(self)

    def init(self):
        self.connection.cursor().executescript(open(os.path.join(root_dir, "sql/schema.sql")).read())

    def close(self):
        self.connection.close()

class Conversations(object):
    __fields__ = ["id", "start_time", "update_time", "talker_name", "title", "status"]
    __select__ = "select %s from conversations " % ", ".join(__fields__)

    STATUS_PENDING = "pending"
    STATUS_ACTIVE = "active"

    def __init__(self, db):
        self.db = db
        self.connection = db.connection

    def _make_obj(self, *args):
        obj = utils.dictobj(zip(self.__fields__, args))
        if not obj.update_time:
            obj.update_time = obj.start_time
        #FIXME: parse dates start_time and update_time
        obj.start_time_since = utils.prettydate(parse_date(obj.start_time))
        obj.update_time_since = utils.prettydate(parse_date(obj.update_time))
        obj.slug = re.compile("\W+", re.UNICODE).sub("_", obj.title)
        obj.unread = ""
        return obj

    def get_all(self):
        cmd = self.__select__ + "order by coalesce(update_time, start_time) desc"
        cur = self.connection.execute(cmd)
        for row in cur:
            yield self._make_obj(*row)

    def get_by_talker(self, name):
        cmd = self.__select__ + "where talker_name = ? order by coalesce(update_time, start_time) desc"
        cur = self.connection.execute(cmd, [name])
        for row in cur:
            yield self._make_obj(*row)

    def get_all_with_unread(self, current_user):
        return self._get_with_unread(self.get_all(), current_user)

    def get_by_talker_with_unread(self, talker_name, current_user):
        return self._get_with_unread(self.get_by_talker(talker_name), current_user)

    def _get_with_unread(self, conversations, current_user):
        visits = self.db.visits.get_dict_by_user(current_user)
        for conv in conversations:
            if current_user:
                if (not visits.get(conv.id) or (parse_date(conv.update_time or conv.start_time) > visits.get(conv.id))):
                    conv.unread = "unread"
            yield conv

    def get(self, id):
        cmd = self.__select__ + "where id = ?"
        cur = self.connection.execute(cmd, [id])
        for row in cur:
            return self._make_obj(*row)
        raise KeyError("no conversation with id %s" % id)

    def save(self,  talker_name, title):
        cur = self.connection.execute("insert into conversations (talker_name, title, status) values (?, ?, ?)",
            [talker_name, title, self.STATUS_PENDING])
        self.connection.commit()
        return cur.lastrowid

    def update(self, id, status=None, update_time=None):
        values = {}
        if status:
            values["status"] = status
        if update_time:
            values["update_time"] = format_date(update_time)
        fields = ", ".join("%s = ?"  % n for n in values.keys())
        self.connection.execute("update conversations set %s where id = ?" % fields,
            values.values() + [id])
        self.connection.commit()

class Messages(object):
    __fields__ = ["id", "conversation_id", "timestamp", "author", "type", "text"]
    __select__ = "select %s from messages " % ", ".join(__fields__)

    TYPE_TALKER = "talker"
    TYPE_LISTENER = "listener"

    def __init__(self, db):
        self.db = db
        self.connection = db.connection

    def _make_obj(self, *args):
        obj = utils.dictobj(zip(self.__fields__, args))
        obj.timestamp_since = utils.prettydate(parse_date(obj.timestamp))
        return obj

    def get_by_conversation(self, conversation_id):
        cmd = self.__select__ + "where conversation_id = ? order by timestamp"
        cur = self.connection.execute(cmd, [conversation_id])
        for row in cur:
            yield self._make_obj(*row)

    def get_first(self, conversation_id):
        for obj in self.get_by_conversation(conversation_id):
            return obj
        raise KeyError("no messages for convesation with id %s" % conversation_id)

    def get_updates(self, conversation_id, current_user, after_message_id):
        if not current_user:
            current_user = ""
        cmd = self.__select__ + "where conversation_id = ? and author <> ? and id > ? order by timestamp"
        cur = self.connection.execute(cmd, [conversation_id, current_user, after_message_id])
        for row in cur:
            yield self._make_obj(*row)

    def has_updates(self, conversation_id, current_user, after_message_id):
        cmd = "select count(*) from messages where conversation_id = ? and author <> ? and id > ?"
        cur = self.connection.execute(cmd, [conversation_id, current_user or "", after_message_id])
        row = cur.fetchone()
        return row[0] != 0

    def save(self, conversation_id, author, type, text):
        cur = self.connection.execute("insert into messages (conversation_id, author, type, text) values (?, ?, ?, ?)",
            [conversation_id, author, type, text])
        self.connection.commit()
        return cur.lastrowid

class Users(object):
    def __init__(self, db):
        self.db = db
        self.connection = db.connection

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

class Visits(object):
    def __init__(self, db):
        self.db = db
        self.connection = db.connection

    def _make_obj(self, conversation_id, user, visit_date):
        obj = utils.dictobj()
        obj.conversation_id = conversation_id
        obj.user = user
        obj.visit_date = parse_date(visit_date)
        return obj

    def get_by_user(self, user):
        cmd = "select conversation_id, user, visit_date from visits where user = ?"
        cur = self.connection.execute(cmd, [user])
        for row in cur:
            yield self._make_obj(*row)

    def get_dict_by_user(self, user):
        visits = {}
        for visit in self.get_by_user(user):
            visits[visit.conversation_id] = visit.visit_date
        return visits

    def save(self, conversation_id, user, visit_date):
        cur = self.connection.execute("replace into visits (conversation_id, user, visit_date) values (?, ?, ?)",
            [conversation_id, user, format_date(visit_date)])
        self.connection.commit()
