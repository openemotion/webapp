# coding=utf8

import datetime
def prettydate(d):
    diff = datetime.datetime.utcnow() - d
    s = diff.seconds
    if diff.days > 7 or diff.days < 0:
        return d.strftime("%d %b %y")
    elif diff.days == 1:
        return u"לפני יום"
    elif diff.days == 2:
        return u"לפני יומיים"
    elif diff.days > 2:
        return u"לפני {} ימים".format(diff.days)
    elif s < 15:
        return u"הרגע"
    elif s < 90:
        return u"לפני כדקה"
    elif s < 3600:
        return u"לפני {} דקות".format(s/60)
    elif s < 3600*1.5:
        return u"לפני כשעה"
    elif s < 3600*2.5:
        return u"לפני כשעתיים"
    else:
        return u"לפני {} שעות".format(s/3600)