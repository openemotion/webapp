import urllib
import utils
from db import Database

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

@app.route("/c/<int:id>/", methods=["GET", "POST"])
@app.route("/c/<int:id>/<slug>", methods=["GET", "POST"])
def conversation(id, slug=None):
    try:
        conv = g.db.conversations.get(id)
        if slug is None:
            return redirect(url_for("conversation", id=id, slug=conv.slug))

        if request.method == "POST" and conv.status == g.db.conversations.STATUS_PENDING:
            g.db.conversations.update(conv.id, g.db.conversations.STATUS_ACTIVE, session["logged_in_user"])
            return redirect(url_for("conversation", id=id, slug=conv.slug))
        else:
            messages = list(g.db.messages.get_by_conversation(id))
            return render_template("conversation.html", conversation=conv, messages=messages)
    except KeyError:
        return abort(404)

@app.route("/c/<int:id>/updates")
def updates(id):
    try:
        after_id = int(request.args.get("after_id", 0))
    except ValueError:
        after_id = 0
    messages = []
    last_message_id = -1
    for msg in g.db.messages.get_updates(id, session["logged_in_user"], after_id):
        messages.append(dict(id=msg.id, author=msg.author, text=msg.text))
        last_message_id = msg.id
    conversation = g.db.conversations.get(id)
    return jsonify(status=conversation.status, messages=messages, last_message_id=last_message_id)

@app.route("/c/<int:id>/post", methods=["POST"])
def message(id):
    g.db.messages.save(id, session["logged_in_user"], request.form["text"])
    return ""

@app.route("/c/new", methods=["GET", "POST"])
def new_conversation():
    if not session["logged_in_user"]:
        abort(401)
    if request.method == "POST":
        id = g.db.conversations.save(session["logged_in_user"], request.form["title"])
        g.db.messages.save(id, session["logged_in_user"], request.form["message"])
        return redirect(url_for("conversation", id=id))
    else:
        return render_template("new_conversation.html")

@app.route("/profile/<name>")
def profile(name):
    user = g.db.users.get(name)
    conversations = g.db.conversations.get_by_talker(name)
    return render_template("profile.html", user=user, conversations=conversations)

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

if __name__ == '__main__':
    app.run(host="0.0.0.0")
