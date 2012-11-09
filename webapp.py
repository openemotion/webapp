from db import Database
from flask import Flask, render_template, request, g, session, redirect, url_for, abort

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
        return render_template("conversation.html", conversation=conv)
    except KeyError:
        return abort(404)

@app.route("/c/new", methods=["GET", "POST"])
def new_conversation():
    if not session["logged_in"]:
        abort(401)
    if request.method == "POST":
        g.db.conversations.save(session["user"], request.form["title"], request.form["message"])
        return redirect(url_for("main"))
    else:
        return render_template("new_conversation.html")

@app.route("/profile/<id>")
def profile(id):
    return render_template("profile.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["logged_in"] = True
        session["user"] = request.form["name"]
        return redirect(url_for("main"))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    session["user"] = None
    return redirect(url_for("main"))

if __name__ == '__main__':
    app.run()