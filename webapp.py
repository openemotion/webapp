import sqlite3
from flask import Flask, render_template, request, g

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
    return render_template("conversation.html")

@app.route("/profile/<id>")
def profile(id):
    return render_template("profile.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run()