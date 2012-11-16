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
        if not name.strip():
            return redirect(url_for("register", goto=request.args.get("goto"), error="no_name"))
        if g.db.users.exists(name):
            return redirect(url_for("register", goto=request.args.get("goto"), error="user_exists"))
        token = utils.generate_token()
        user_id = g.db.users.save(name, token)
        login_url = url_for("login", _external=True, user_id=user_id, token=token)
        with open("static/login_urls.html", "wa") as f:
            f.write("<a href=%(login_url)s>%(login_url)s</a>" % locals())
        session["logged_in_user"] = name
        return redirect(url_for("post_register", login_url=login_url, goto=request.args.get("goto")))
        # return render_template("post_register.html", login_url=login_url)
    else:
        return render_template("register.html")

@app.route("/post_register")
def post_register():
    login_url = request.args.get("login_url")
    goto = request.args.get("goto")
    if not login_url:
        abort(403)
    return render_template("post_register.html", login_url=login_url, goto=goto)

@app.route("/login")
def login():
    user_id = request.args.get("user_id")
    token = request.args.get("token")
    try:
        user = g.db.users.get_safe(user_id, token)
    except KeyError:
        return render_template("login.html", error="bad_password")
    session["logged_in_user"] = user.name
    return redirect(url_for("main"))

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
