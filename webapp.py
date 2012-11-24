import time
import urllib
import utils
from db import Database, Messages

from flask import (Flask, render_template, request, g, session, redirect,
    url_for, abort, Markup, jsonify)

app = Flask(__name__)
app.config.from_object("config")

@app.before_request
def before_request():
    g.db = Database(app.config["DATABASE"])

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route("/")
def main():
    conversations = g.db.conversations.get_all()
    return render_template("main.html", conversations=conversations)

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/conversations")
def conversations():
    conversations = g.db.conversations.get_all()
    return render_template("_conversation_list.html", conversations=conversations)

@app.route("/conversations/<int:id>/")
@app.route("/conversations/<int:id>/<slug>")
def conversation(id, slug=None):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    if slug != conversation.slug:
        return redirect(url_for("conversation", id=id, slug=conversation.slug))

    messages = list(g.db.messages.get_by_conversation(id))
    message_type = detect_user_message_type(conversation)
    return render_template("conversation.html", conversation=conversation, messages=messages, user_message_type=message_type)

@app.route("/conversations/<int:id>/facilitate", methods=["POST"])
def facilitate(id):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    if conversation.status == g.db.conversations.STATUS_PENDING:
        g.db.conversations.update(conversation.id, g.db.conversations.STATUS_ACTIVE, session["logged_in_user"])

    return redirect(url_for("conversation", id=id, slug=conversation.slug))

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

    return jsonify(conversation=conversation, messages=messages, last_message_id=last_message_id)

# FIXME: long polling doesn't work for updating the conversation status
# FIXME: when client disconnects due to timeout, we get a broken pipe error in the console
@app.route("/conversations/<int:id>/poll")
def poll(id):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    last_message_id = int(request.args.get("last_message_id", -1, type=int))
    while True:
        has_updates = g.db.messages.has_updates(id, session.get("logged_in_user"), last_message_id)
        if has_updates:
            break
        time.sleep(0.5)

    return "updated!"

@app.route("/conversations/<int:id>/post", methods=["POST"])
def post_message(id):
    try:
        conversation = g.db.conversations.get(id)
    except KeyError:
        return abort(404)

    message_type = detect_user_message_type(conversation)
    g.db.messages.save(id, session["logged_in_user"], message_type,request.form["text"])

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

@app.route("/user/<name>/")
def user(name):
    user = g.db.users.get(name)
    conversations = g.db.conversations.get_by_talker(name)
    return render_template("user.html", user=user, conversations=conversations)

@app.route("/user/<name>/conversations")
def user_conversations(name):
    conversations = g.db.conversations.get_by_talker(name)
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
        return redirect(urldecode(request.args.get("goto")) or url_for("main"))
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
        return redirect(urldecode(request.args.get("goto")) or url_for("main"))
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

def urldecode(s):
    if isinstance(s, unicode):
        s = s.encode("utf8")
    return urllib.unquote(s).decode("utf8")

def detect_user_message_type(conversation):
    user = session.get("logged_in_user")
    if user == conversation.listener_name:
        return g.db.messages.TYPE_LISTENER
    elif user == conversation.talker_name:
        return g.db.messages.TYPE_TALKER
    else:
        return g.db.messages.TYPE_OTHER

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True)
