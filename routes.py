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
    message = ""
    if topics.sendsuggestion(content):
        message="Ehdotuksesi on lähetetty ylläpidolle!"
    else:
        message="Aihetta on jo ehdotettu!"
    return render_template("newtopic.html", message=message)

@app.route("/<previous>/<identifier>/deletemessage/<int:m_id>", methods=["post"])
def deletemessage(m_id, previous, identifier):
    messages.delete_message(m_id)
    return redirect('/' + str(previous) + '/' + str(identifier))

@app.route("/profile/<username>")
def profile(username):
    getuser = users.username()
    if username == getuser:
        list = messages.get_users_messages(users.user_id())
        return render_template("profile.html", user=username, messages=list)
    else:
        return render_template("topic.html", messages=[('Sinulla ei ole oikeutta nähdä tätä profiilisivua!',)], name=username)

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
        return render_template("newmessage.html", t_id=topic_id, message="Viestisi on liian pitkä tai tyhjä!", additional="Viestin maksimipituus on  500 merkkiä")

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