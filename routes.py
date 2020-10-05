from app import app
from flask import render_template, request, redirect, abort
import topics, users, messages

ip_ban_list = ['']

@app.before_request
def block_method():
    ip = request.environ.get('REMOTE_ADDR')
    if ip in ip_ban_list:
        abort(403)

@app.route("/")
def index():
    list = topics.get_topic_list()
    return render_template("index.html", topics=list)

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route("/newtopic")
def newtopic():
    return render_template("newtopic.html")

@app.route("/sendtopic", methods=["post"])
def sendtopic():
    content = request.form["content"]
    if topics.sendsuggestion(content):
        return redirect("/")
    else:
        return render_template("newtopic.html", message="Aihetta on jo ehdotettu!")

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    user_id = users.user_id()
    list = messages.get_message_list(topic_id)
    topicname = topics.get_topic_name(topic_id)[0][0]
    if user_id == 0:
        return render_template("topic.html", messages=[('Sinun tulee olla kirjautunut sisään nähdäksesi aiheiden viestit!',)], name=topicname)
    else:
        return render_template("topic.html", messages=list, t_id=topic_id, name=topicname)

@app.route("/topic/<int:topic_id>/newmessage")
def newmessage(topic_id):
    return render_template("newmessage.html", t_id=topic_id)

@app.route("/topic/<int:topic_id>/sendmessage", methods=["post"])
def sendmessage(topic_id):
    content = request.form["content"]
    if messages.send(content, topic_id):
        return redirect('/topic/' + str(topic_id))
    else:
        return redirect("/")

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