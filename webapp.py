import re
import urllib
import logging
from urlparse import urljoin
from datetime import datetime

import utils

from flask import (Flask, render_template, request, g, session, redirect,
    url_for, abort, Markup, escape)

from werkzeug.contrib.atom import AtomFeed

# FIXME: main list doesn't show talker name links

app = Flask(__name__)
app.config.from_object("config")
app.logger.addHandler(logging.FileHandler(app.config["LOGFILE"]))

import model
db = model.db
db.init_app(app)

@app.route("/")
def main():
    conversations = model.Conversation.query.all()
    return render_template("main.html", conversations=conversations)

@app.route('/atom')
def main_feed():
    feed = AtomFeed(u'Open Emotion Conversations', feed_url=request.url, url=request.url_root)
    for conv in model.Conversation.query:
        messages = list(conv.messages)
        feed.add(conv.title,
                 messages[0].text,
                 content_type='html',
                 author=conv.owner.name,
                 url=make_external('/conversations/%d' % conv.id),
                 updated=messages[-1].timestamp,
                 published=conv.start_time)
    return feed.get_response()

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/conversations")
def conversations():
    conversations = model.Conversation.query.all()
    return render_template("_conversation_list.html", conversations=conversations)

@app.route("/conversations/<int:id>/")
@app.route("/conversations/<int:id>/<slug>")
def conversation(id, slug=None):
    conversation = model.Conversation.query.get_or_404(id)
    if slug != conversation.slug:
        return redirect(url_for("conversation", _external=True, id=id, slug=conversation.slug))
    update_visit_time(conversation)
    user_message_type = detect_user_message_type(conversation)
    return render_template("conversation.html", conversation=conversation, messages=list(conversation.messages), user_message_type=user_message_type)

@app.route("/conversations/<int:id>/atom")
def conversation_feed(id):
    conversation = model.Conversation.query.get_or_404(id)
    feed = AtomFeed(conversation.title, feed_url=request.url, url=request.url_root)
    for message in conversation.messages:
        feed.add (
            message.text.splitlines()[0],
            message.text,
            content_type='html',
            author=message.author.name,
            url=request.url_root,
            updated=message.timestamp,
            published=message.timestamp
        )
    return feed.get_response()

@app.route("/conversations/<int:id>/updates")
def updates(id):
    conversation = model.Conversation.query.get_or_404(id)
    last_message_id = int(request.args.get("last_message_id", -1, type=int))
    messages = conversation.get_updated_messages(get_current_user(), last_message_id)
    last_message_id = messages[-1].id if messages else last_message_id
    update_visit_time(conversation)
    return utils.jsonify(conversation=conversation, messages=messages, last_message_id=last_message_id)

@app.route("/conversations/<int:id>/post", methods=["POST"])
def post_message(id):
    conv = model.Conversation.query.get_or_404(id)
    user = get_current_user()

    if (conv.owner != user and conv.status == model.Conversation.STATUS.PENDING):
        conv.status = model.Conversation.STATUS.ACTIVE

    update_visit_time(conv)

    # FIXME: perhaps we should add the message to the conversation explicitly
    # conv.messages.append(Message(user, escape(request.form["text"])))
    model.Message(conv, user, escape(request.form["text"]))
    conversation.update_time = datetime.utcnow()

    db.session.commit()

    return ""

@app.route("/conversations/new", methods=["GET", "POST"])
def new_conversation():
    if not session["logged_in_user"]:
        abort(401)
    if request.method == "POST":
        conv = model.Conversation(get_current_user(), request.form["title"])
        db.session.commit()
        return redirect(url_for("conversation", id=conv.id))
    else:
        return render_template("new_conversation.html")

@app.route("/users/<name>/")
def user(name):
    user = model.User.get_or_404(name)
    return render_template("profile.html", user=user, conversations=user.conversations)

@app.route("/users/<name>/conversations")
def user_conversations(name):
    user = model.User.get_or_404(name)
    return render_template("_conversation_list.html", conversations=user.conversations)

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
        existing = model.User.query.filter_by(name=name).first()
        if existing:
            return redirect(url_for("register", error="user_exists", name=existing.name, goto=request.args.get("goto")))
        if password != password2:
            return redirect(url_for("register", error="password_mismatch", name=name, goto=request.args.get("goto")))

        user = model.User(name, password.encode("utf8"))
        db.session.add(user)
        db.session.commit()

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
        user = model.User.query.filter_by(name=name).first()
        if not user:
            app.logger.info("no user")
            # app.logger.error("%s %s %s %s" % (user.password_hash, password_hash, password.encode("utf8"), name.encode("utf8")))
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

def make_external(url):
    return urljoin(request.url_root, url)

def update_visit_time(conversation):
    return
    # FIXME: restore visit management
    # FIXME: logged_in_user should hold the user id, not name


def detect_user_message_type(conversation):
    if session.get("logged_in_user") == conversation.owner.name:
        return model.Message.TYPE.TALKER
    else:
        return model.Message.TYPE.LISTENER

def get_current_user():
    return model.User.get_or_404(session["logged_in_user"])

if __name__ == '__main__':
    # override configuration for development
    app.config.from_object("config_dev")
    app.run(host="0.0.0.0", threaded=True)
