# coding=utf8
import json
from datetime import datetime
from prettydate import prettydate
from flask import escape, current_app, request

class dictobj(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def encrypt_password(password, salt):
    """
    Creates a password hash.
    """
    import sha
    s = sha.new()
    s.update(bytes(password))
    s.update(bytes(salt))
    return s.hexdigest()

def bytes(s):
    """
    Makes sure a string is in bytes.
    """
    if isinstance(s, unicode):
        return s.encode("utf8")
    return s

def text2p(text):
    """
    Converts a block of text into HTML paragraphs.
    """
    text = escape(text)
    return "\n".join(("<p>%s</p>" % l) if l else "<br>" for l in text.splitlines())

def jsonify(*args, **kwargs):
    """
    A replacement for Flask's jsonify that handles datetime objects
    and allows customized serialization with __json__ methods on objects.
    """
    class ObjectEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, '__json__'):
                return obj.__json__()
            if isinstance(obj, datetime):
                return obj.isoformat()
            return json.JSONEncoder.default(self, obj)

    return current_app.response_class(
        json.dumps(
            dict(*args, **kwargs),
            indent=None if request.is_xhr else 2,
            cls=ObjectEncoder
        ), 
        mimetype='application/json',
    )


class Jsonable(object):
    def __json__(self):
        return dict((k,v) for (k,v) in self.__dict__.iteritems() if not k.startswith('_sa_'))
