import re
import sqlite3
from datetime import datetime
import utils

class dictobj(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Database(object):
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.conversations = Conversations(self.connection)
        self.users = Users(self.connection)

    def close(self):
        self.connection.close()

class Conversations(object):
    def __init__(self, connection):
        self.connection = connection

    def _make_obj(self, id, start_time, author, title, first_message):
        obj = dictobj()
        obj.id = id
        obj.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        obj.author = author
        obj.title = title
        obj.first_message = first_message
        obj.start_time_since = utils.prettydate(obj.start_time)
        obj.slug = re.compile("\W+", re.UNICODE).sub("_", obj.title)
        return obj

    def get_all(self):
        cmd = "select id, start_time, author, title, first_message from conversations order by id desc"
        cur = self.connection.execute(cmd)
        for row in cur:
            yield self._make_obj(*row)

    def get(self, id):
        cmd = "select id, start_time, author, title, first_message from conversations where id = ?"
        cur = self.connection.execute(cmd, [id])
        for row in cur:
            return self._make_obj(*row)
        raise KeyError("no conversation with id %s" % id)

    def save(self, author, title, first_message):
        self.connection.execute("insert into conversations (author, title, first_message) values (?, ?, ?)",
            [author, title, first_message])
        self.connection.commit()

class Users(object):
    def __init__(self, connection):
        self.connection = connection

    def _make_obj(self, id, name, password_hash):
        obj = dictobj()
        obj.id = id
        obj.name = name
        obj.password_hash = password_hash
        return obj

    def get_all(self):
        pass

    def get(self, id):
        pass

    def save(self, author, title, first_message):
        pass

