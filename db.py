import sqlite3
from datetime import datetime
import utils

class Database(object):
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)

    def get_conversations(self):
        cmd = "select id, start_time, author, title, first_message from conversations order by id desc"
        cur = self.connection.execute(cmd)
        for row in cur:
            conv = dict(zip(["id", "start_time", "author", "title", "first_message"], row))
            d = datetime.strptime(conv["start_time"], "%Y-%m-%d %H:%M:%S")
            conv["start_time_since"] = utils.prettydate(d)
            conv["slug"] = conv["title"].replace(" ", "_")
            yield conv

    def get_conversation(self, id):
        cmd = "select id, author, title, first_message from conversations where id = ?"
        cur = self.connection.execute(cmd, [id])
        for row in cur:
            return dict(zip(["id", "author", "title", "first_message"], row))
        else:
            return None

    def store_conversation(self, author, title, first_message):
        self.connection.execute("insert into conversations (author, title, first_message) values (?, ?, ?)",
            [author, title, first_message])
        self.connection.commit()

    def close(self):
        self.connection.close()
