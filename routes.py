from app import app
from flask import render_template, request, redirect
import topics, users, messages

@app.route("/")
def index():
    list = topics.get_topic_list()
    return render_template("index.html", topics=list)

@app.route("/newtopic")
def newtopic():
    return render_template("newtopic.html")

@app.route("/sendtopic", methods=["post"])
def sendtopic():
    content = request.form["content"]
    if topics.send(content):
        return redirect("/")
    else:
        return render_template("newtopic.html", message="Aiheen luominen ei onnistunut!")

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
        okei = users.login(username, password)
        if okei[0]:
            return redirect("/")
        else:
            return render_template("login.html", message=okei[1], additional=okei[2])

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
        passwordconf = request.form["passwordconf"]
        okei = users.register(username, password, passwordconf)
        if okei[0]:
            return redirect("/")
        else:
            return render_template("register.html",message=okei[1],additional=okei[2])