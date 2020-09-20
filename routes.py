from app import app
from flask import render_template, request, redirect
import topics, users, messages

@app.route("/")
def index():
    list = topics.get_topic_list()
    return render_template("index.html", topics=list)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["post"])
def send():
    content = request.form["content"]
    if topics.send(content):
        return redirect("/")
    else:
        return render_template("new.html", message="Aiheen luominen ei onnistunut!")

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    user_id = users.user_id()
    list = messages.get_message_list(topic_id)
    if user_id == 0:
        return redirect("/")
    else:
        return render_template("topic.html", messages=list)

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")