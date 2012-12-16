# coding=utf8
from flask import escape
import datetime
from urlparse import urljoin
from prettydate import prettydate

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

def extract_title(text, maxlen=40):
    title = text.splitlines()[0].split(".")[0]
    if len(title) > maxlen:
        title = title[:maxlen-3] + "..."
    return title

