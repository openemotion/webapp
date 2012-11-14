# coding=utf8

import urllib
import utils
from db import Database

from flask import (Flask, render_template, request, g, session, redirect, url_for, abort, Markup, jsonify)
from flask.ext.wtf import Form, TextField, PasswordField, RecaptchaField, validators
from werkzeug.security import generate_password_hash, check_password_hash

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
            messages = g.db.messages.get_by_conversation(id)
            return render_template("conversation.html", conversation=conv, messages=messages)
    except KeyError:
        return abort(404)

@app.route("/c/<int:id>/history")
def history(id):
    try:
        after_id = int(request.args.get("after_id", 0))
    except ValueError:
        after_id = 0
    messages = []
    last_id = 0
    for msg in g.db.messages.get_by_conversation(id):
        if msg.id > after_id:
            messages.append(dict(author=msg.author, text=msg.text))
        last_id = msg.id
    conv = g.db.conversations.get(id)
    return jsonify(messages=messages, last_id=last_id, status=conv.status)

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

class RegistrationForm(Form):
    username = TextField(u"שם בדוי", [validators.Required(message=u"איך אפשר בלי שם?")])
    password = PasswordField(u"סיסמא", [validators.Required(message=u"איך אפשר בלי סיסמא?"), validators.EqualTo("confirm", message=u"הסיסמאות צריכות להיות זהות")])
    confirm = PasswordField(u"שוב סיסמא", [validators.Required(message=u"איך אפשר בלי להתעצבן?")])

    def validate(self):
        if not super(Form, self).validate():
            return False
        if g.db.users.exists(self.username.data):
            self.username.errors.append(u"מישהו כבר נרשם עם השם הזה")
            return False
        return True

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # FIXME: use standard werkezeug password hashing
        password_hash = generate_password_hash(form.password.data.encode("utf8"))
        g.db.users.save(form.username.data, password_hash)
        session["logged_in_user"] = form.username.data
        return redirect(urldecode(request.args.get("goto")) or url_for("main"))
    return render_template("register.html", form=form)


# FIXME: use a WTF form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        if not name:
            return redirect(url_for("login", error="no_name"))
        if not password:
            return redirect(url_for("login", error="no_password", name=name))
        try:
            user = g.db.users.get(name)
        except KeyError:
            return redirect(url_for("login", error="bad_password", name=name))
        if check_password_hash(password.encode("utf8"), user.password_hash):
            return redirect(url_for("login", error="bad_password", name=name))
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

def urldecode(s):
    if isinstance(s, unicode):
        s = s.encode("utf8")
    return urllib.unquote(s).decode("utf8")

if __name__ == '__main__':
    app.run()
