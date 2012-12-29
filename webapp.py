import re
import time
import urllib
import logging
from urlparse import urljoin
from datetime import datetime

import utils
from db import Database, Messages, parse_date

from flask import (Flask, render_template, request, g, session, redirect,
    url_for, abort, Markup, jsonify, escape)

from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)
app.config.from_object("config")
app.logger.addHandler(logging.FileHandler(app.config["LOGFILE"]))

@app.before_request
def before_request():
    g.db = Database(app.config["DATABASE"])

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route("/")
def main():
    conversations = g.db.conversations.get_all_with_unread(session.get("logged_in_user"))
    return render_template("main.html", conversations=conversations)

@app.route('/atom')
def main_feed():
    feed = AtomFeed(u'Open Emotion Conversations', feed_url=request.url, url=request.url_root)
    conversations = list(g.db.conversations.get_all())
    for conv in conversations:
        messages = list(g.db.messages.get_by_conversation(conv.id))
        feed.add(conv.title,
                 messages[0].text,
                 content_type='html',
                 author=conv.talker_name,
                 url=make_external('/conversations/%d' % conv.id),
                 updated=parse_date(messages[-1].timestamp),
                 published=parse_date(conv.start_time))
    return feed.get_response()

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

# @app.route("/contact")
# def contact():
#     return render_template("contact.html")

@app.route("/conversations")
def conversations():
    conversations = g.db.conversations.get_all_with_unread(session.get("logged_in_user"))
    return render_template("_conversation_list.html", conversations=conversations)

@app.route("/conversations/<int:id>/")
@app.route("/conversations/<int:id>/<slug>")
def conversation(id, slug=None):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    if slug != conversation.slug:
        return redirect(url_for("conversation", _external=True, id=id, slug=conversation.slug))

    update_visit_time(conversation)

    messages = list(g.db.messages.get_by_conversation(id))
    message_type = detect_user_message_type(conversation)
    return render_template("conversation.html", conversation=conversation, messages=messages, user_message_type=message_type)

@app.route("/conversations/<int:id>/atom")
def conversation_feed(id):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)
    feed = AtomFeed(conversation.title, feed_url=request.url, url=request.url_root)
    messages = list(g.db.messages.get_by_conversation(conversation.id))
    for message in messages:
        feed.add(message.text.splitlines()[0],
                 message.text,
                 content_type='html',
                 author=message.author,
                 url=request.url_root,
                 updated=parse_date(message.timestamp),
                 published=parse_date(message.timestamp))
    return feed.get_response()

@app.route("/conversations/<int:id>/updates")
def updates(id):
    # FIXME : factor out to get_conversation_or_404
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    last_message_id = int(request.args.get("last_message_id", -1, type=int))
    messages = list(g.db.messages.get_updates(id, session.get("logged_in_user"), last_message_id))
    last_message_id = messages[-1].id if messages else last_message_id

    update_visit_time(conversation)

    return jsonify(conversation=conversation, messages=messages, last_message_id=last_message_id)

@app.route("/conversations/<int:id>/post", methods=["POST"])
def post_message(id):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    if (conversation.talker_name != session["logged_in_user"] and
        conversation.status == g.db.conversations.STATUS_PENDING):
        g.db.conversations.update(conversation.id, g.db.conversations.STATUS_ACTIVE)

    update_visit_time(conversation)

    message_type = detect_user_message_type(conversation)
    g.db.messages.save(id, session["logged_in_user"], message_type, escape(request.form["text"]))
    g.db.conversations.update(conversation.id, update_time=datetime.utcnow())

    return ""

@app.route("/conversations/new", methods=["GET", "POST"])
def new_conversation():
    if not session["logged_in_user"]:
        abort(401)
    if request.method == "POST":
        id = g.db.conversations.save(session["logged_in_user"], request.form["title"])
        g.db.messages.save(id, session["logged_in_user"], g.db.messages.TYPE_TALKER, request.form["message"])
        return redirect(url_for("conversation", id=id))
    else:
        return render_template("new_conversation.html")

@app.route("/users/<name>/")
def user(name):
    user = g.db.users.get(name)
    conversations = g.db.conversations.get_by_talker_with_unread(name, session.get("logged_in_user"))
    return render_template("profile.html", user=user, conversations=conversations)

@app.route("/users/<name>/conversations")
def user_conversations(name):
    conversations = g.db.conversations.get_by_talker_with_unread(name, session.get("logged_in_user"))
    return render_template("_conversation_list.html", conversations=conversations)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if not name:
            return redirect(url_for("register", error="no_name", goto=request.args.get("goto")))
        if not password:
            return redirect(url_for("register", error="no_password", name=name, goto=request.args.get("goto")))
        if not password2:
            return redirect(url_for("register", error="no_password2", name=name, goto=request.args.get("goto")))
        try:
            existing = g.db.users.get(name)
        except KeyError:
            pass
        else:
            return redirect(url_for("register", error="user_exists", name=existing.name, goto=request.args.get("goto")))
        if password != password2:
            return redirect(url_for("register", error="password_mismatch", name=name, goto=request.args.get("goto")))
        password_hash = utils.encrypt_password(password.encode("utf8"), name.encode("utf8"))
        g.db.users.save(name, password_hash)
        session["logged_in_user"] = name
        return redirect(urldecode(request.args.get("goto", "")) or url_for("main"))
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        if not name:
            return redirect(url_for("login", error="no_name", goto=request.args.get("goto")))
        if not password:
            return redirect(url_for("login", error="no_password", name=name, goto=request.args.get("goto")))
        try:
            user = g.db.users.get(name)
        except KeyError:
            return redirect(url_for("login", error="bad_password", name=name, goto=request.args.get("goto")))
        password_hash = utils.encrypt_password(password, name)
        if user.password_hash != password_hash:
            return redirect(url_for("login", error="bad_password", name=name, goto=request.args.get("goto")))
        session["logged_in_user"] = request.form["name"]
        return redirect(urldecode(request.args.get("goto") or "") or url_for("main"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session["logged_in_user"] = None
    return redirect(urldecode(request.args.get("goto")) or url_for("main"))

@app.template_filter("urlencode")
def urlencode_filter(s):
    if isinstance(s, unicode):
        s = s.encode("utf8")
    return Markup(urllib.quote_plus(s))

@app.template_filter("multiline")
def multiline_filter(s):
    s = re.sub(r"(\r?\n)", "<br>", s)
    return Markup(s)

@app.template_filter("shorten")
def shorten_filter(s, maxlen=40):
    if len(s) < maxlen:
        return s
    else:
        return s[:maxlen-3] + "..."

def urldecode(s):
    if isinstance(s, unicode):
        s = s.encode("utf8")
    return urllib.unquote(s).decode("utf8")

def detect_user_message_type(conversation):
    user = session.get("logged_in_user")
    if user == conversation.talker_name:
        return g.db.messages.TYPE_TALKER
    else:
        return g.db.messages.TYPE_LISTENER

def make_external(url):
    return urljoin(request.url_root, url)

def update_visit_time(conversation):
    if session.get("logged_in_user"):
        g.db.visits.save(conversation.id, session.get("logged_in_user"), datetime.utcnow())

if __name__ == '__main__':
    # override configuration for development
    app.config.from_object("config_dev")
    app.run(host="0.0.0.0", threaded=True)
