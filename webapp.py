import sqlite3
from flask import Flask, render_template, request, g, session, redirect, url_for

app = Flask(__name__)
app.config.from_object("config")

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/c/<id>")
def conversation(id):
    if id == "new":
        return render_template("new_share.html")
    return render_template("conversation.html")

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