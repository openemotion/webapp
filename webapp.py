import utils
from db import Database
from flask import Flask, render_template, request, g, session, redirect, url_for, abort, Markup

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
        if conv.status == g.db.conversations.STATUS_ACTIVE:
            messages = g.db.messages.get_by_conversation(id)
            return render_template("active_conversation.html", conversation=conv, messages=messages)
        else: # conv.status == g.db.conversations.STATUS_PENDING:
            if request.method == "POST":
                g.db.conversations.update(conv.id, g.db.conversations.STATUS_ACTIVE, session["logged_in_user"])
                return redirect(url_for("conversation", id=id, slug=conv.slug))
            else:
                conv.first_message = g.db.messages.get_first(conv.id).text
                return render_template("pending_conversation.html", conversation=conv)
    except KeyError:
        return abort(404)

@app.route("/c/<int:id>/history")
def history(id):
    messages = g.db.messages.get_by_conversation(id)
    return render_template("messages.html", messages=messages)

@app.route("/c/<int:id>/post", methods=["POST"])
def message(id):
    g.db.messages.save(id, session["logged_in_user"], request.form["text"])
    return ""

@app.route("/c/new", methods=["GET", "POST"])
def new_conversation():
    if not session["logged_in_user"]:
        abort(401)
    if request.method == "POST":
        g.db.conversations.save(session["logged_in_user"], request.form["title"], request.form["message"])
        return redirect(url_for("main"))
    else:
        return render_template("new_conversation.html")

@app.route("/profile/<id>")
def profile(id):
    return render_template("profile.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    #FIXME: should redirect and not render a template according to http://en.wikipedia.org/wiki/Post/Redirect/Get
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        password2 = request.form["password2"]
        if not name:
            return render_template("register.html", error={"type":"no_name"})
        if not password:
            return render_template("register.html", error={"type":"no_password", "name": name})
        if not password2:
            return render_template("register.html", error={"type":"no_password2", "name": name})
        try:
            existing = g.db.users.get(name)
        except KeyError:
            pass
        else:
            return render_template("register.html", error={"type":"user_exists", "user":existing.name})

        if password != password2:
            return render_template("register.html", error={"type":"password_mismatch", "name": name})
        password_hash = utils.encrypt_password(password.encode("utf8"), name.encode("utf8"))
        g.db.users.save(name, password_hash)
        session["logged_in_user"] = name
        return redirect(url_for("main"))
    else:
        return render_template("register.html", error={})

@app.route("/login", methods=["GET", "POST"])
def login():
    #FIXME: should redirect and not render a template according to http://en.wikipedia.org/wiki/Post/Redirect/Get
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        if not name:
            return render_template("login.html", error={"type":"no_name"})
        if not password:
            return render_template("login.html", error={"type":"no_password"})
        try:
            user = g.db.users.get(name)
        except KeyError:
            return render_template("login.html", error={"type":"bad_name", "name" : name})
        password_hash = utils.encrypt_password(password, name)
        if user.password_hash != password_hash:
            return render_template("login.html", error={"type":"bad_password", "name" : name})
        session["logged_in_user"] = request.form["name"]
        return redirect(url_for("main"))
    else:
        return render_template("login.html", error={})

@app.route("/logout")
def logout():
    session["logged_in_user"] = None
    return redirect(url_for("main"))

if __name__ == '__main__':
    app.run()