# coding=utf8
from flask import escape
import datetime

class dictobj(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def prettydate(d):
    """
    Converts a date into an estimate of how long has passed.
    Assumes d and the system date are in the same time zone
    (usually GMT).
    Note that the result is in Hebrew.
    """
    diff = datetime.datetime.utcnow() - d
    s = diff.seconds
    if diff.days == 1:
        return u"יום"
    elif diff.days == 2:
        return u"יומיים"
    elif diff.days > 2:
        return u"{} ימים".format(diff.days)
    elif s < 15:
        return u"כמה שניות"
    elif s < 120:
        return u"כדקה"
    elif s < 3600:
        return u"{} דקות".format(s / 60)
    elif s < 3600 * 1.5:
        return u"כשעה"
    elif s < 3600 * 2.5:
        return u"כשעתיים"
    else:
        return u"{} שעות".format(s / 3600)

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
