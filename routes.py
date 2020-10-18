from app import app
from flask import render_template, request, redirect, abort
import topics, users, messages

error_redirect = 'Muistathan sivuston säännöt ja ohjeet?'

@app.route("/")
def index():
    list = topics.get_topic_list()
    return render_template("index.html", topics=list)

@app.route("/topics")
def fulltopics():
    list = topics.get_full_topic_list()
    return render_template("topics.html", topics=list)

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route("/newtopic")
def newtopic():
    user_id = users.user_id()
    if user_id == 0:
        return render_template("rules.html", message='Kirjaudu sisään lähettääksesi ehdotuksia!', additional=error_redirect)
    return render_template("newtopic.html")

@app.route("/flagged/messages")
def flagged():
    admin = users.admin()
    if admin == 0:
       return render_template("rules.html", message='Sinulla ei ole oikeutta selata raportoituja viestejä!', additional=error_redirect)
    list = messages.get_flagged_message_list()
    return render_template("flagged.html", messages=list)

@app.route("/sendtopic", methods=["post"])
def sendtopic():
    if users.token() != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/newtopic")
    message = topics.sendsuggestion(content, user_id)
    return render_template("newtopic.html", message=message[1])

@app.route("/flag/<int:message_id>", methods=["post"])
def flagmessage(message_id):
    if users.token() != request.form["csrf_token"]:
        abort(403)
    user_id = users.user_id()
    if user_id == 0:
        return render_template("rules.html", message="Kirjaudu sisään raportoidaksesi viestejä!", additional=error_redirect)
    messages.flag(message_id, user_id)
    list = topics.get_topic_list()
    return render_template("index.html", topics=list, message='Kiitos raportoinnista!', additional='Ylläpito käsittelee viestin mahdollisimman pian')

@app.route("/<previous>/<identifier>/deletemessage/<int:m_id>", methods=["post"])
def deletemessage(m_id, previous, identifier):
    m_user_id = messages.get_m_user_id(m_id)
    user_id = users.user_id()
    admin = users.admin()
    if user_id != m_user_id[0] and admin < 2:
        return render_template("rules.html", message='Sinulla ei ole oikeutta poistaa viestiä!', additional=error_redirect)
    messages.delete_message(m_id)
    return redirect("/" + str(previous) + "/" + str(identifier))

@app.route("/profile/<username>/addinfo")
def addinfo(username):
    user_id = users.user_id()
    s_username = users.username()
    if user_id == 0 or s_username != username:
        return render_template("rules.html", message='Sinulla ei ole oikeutta lisätä tietoa tähän profiiliin!', additional=error_redirect)
    return render_template("addinfo.html", username=username)

@app.route("/profile/<username>/addinfo/send", methods=["post"])
def sendinfo(username):
    if users.token() != request.form["csrf_token"]:
        abort(403)
    user_id = users.user_id()
    s_username = users.username()
    if user_id == 0 or s_username != username:
        return render_template("rules.html", message='Sinulla ei ole oikeutta lisätä tietoa tähän profiiliin!', additional=error_redirect)
    about = request.form["about"]
    info = request.form["info"]
    users.add_info(user_id, about, info)
    return redirect("/profile/" + str(username))

@app.route("/profile/<username>/editinfo/<int:info_id>")
def editinfo(username, info_id):
    user_id = users.user_id()
    s_username = users.username()
    if user_id == 0 or s_username != username:
        return render_template("rules.html", message='Sinulla ei ole oikeutta muokata tämän profiilin tietoja!', additional=error_redirect)
    user_info = users.get_info(info_id)
    return render_template("editinfo.html", username=username, about=user_info[0], info=user_info[1], info_id=info_id)

@app.route("/profile/<username>/editinfo/<int:info_id>/send", methods=["post"])
def submiteditinfo(username, info_id):
    if users.token() != request.form["csrf_token"]:
        abort(403)
    user_id = users.user_id()
    s_username = users.username()
    if user_id == 0 or s_username != username:
        return render_template("rules.html", message='Sinulla ei ole oikeutta muokata tämän profiilin tietoja!', additional=error_redirect)
    about = request.form["about"]
    info = request.form["info"]
    users.update_info(info_id, about, info)
    return redirect("/profile/" + str(username))

@app.route("/profile/<username>/editinfo/<int:info_id>/delete", methods=["post"])
def deleteinfo(username, info_id):
    user_id = users.user_id()
    s_username = users.username()
    if user_id == 0 or s_username != username:
        return render_template("rules.html", message='Sinulla ei ole oikeutta muokata tämän profiilin tietoja!', additional=error_redirect)
    users.delete_info(info_id)
    return redirect("/profile/" + str(username))

@app.route("/profile/<username>")
def profile(username):
    getuser = users.username()
    admin = users.admin()
    if username != getuser and admin == 0:
        return render_template("rules.html", message='Sinulla ei ole oikeutta nähdä profiilisivua!', additional=error_redirect)
    user_id = users.user_id_db(username)[0]
    own_messages = messages.get_users_messages(user_id)
    own_info = users.get_all_info(user_id)
    return render_template("profile.html", user=username, messages=own_messages, infos=own_info)

@app.route("/<previous>/<identifier>/editmessage/<int:message_id>")
def editmessage(message_id, previous, identifier):
    m_content = messages.get_message(message_id)
    user_id = users.user_id()
    admin = users.admin()
    if user_id != m_content[1] and admin == 0:
        return render_template("rules.html", message='Sinulla ei ole oikeutta muokata viestiä!', additional=error_redirect)
    return render_template("editmessage.html", messagecontent=m_content[0], m_id=message_id)

@app.route("/<previous>/<identifier>/editmessage/<int:message_id>/send", methods=["post"])
def sendeditmessage(message_id, previous, identifier):
    if users.token() != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    m_user_id = messages.get_m_user_id(message_id)
    user_id = users.user_id()
    admin = users.admin()
    if user_id != m_user_id[0] and admin == 0:
        return render_template("rules.html", message='Sinulla ei ole oikeutta muokata viestiä!', additional=error_redirect) 
    messages.update_message(message_id, content)
    return redirect('/' + str(previous) + '/' + str(identifier))

@app.route("/topic/<int:topic_id>")
def topic(topic_id):
    user_id = users.user_id()
    topicname = topics.get_topic_name(topic_id)[0][0]
    if user_id == 0:
        return render_template("rules.html", message='Kirjaudu sisään nähdäksesi aiheiden viestejä!', additional=error_redirect) 
    list = messages.get_message_list(topic_id)
    return render_template("topic.html", messages=list, t_id=topic_id, name=topicname)

@app.route("/topic/<int:topic_id>/newmessage")
def newmessage(topic_id):
    user_id = users.user_id()
    if user_id == 0:
        return render_template("rules.html", message='Kirjaudu sisään lähettääksesi viestejä!', additional=error_redirect)
    return render_template("newmessage.html", t_id=topic_id)

@app.route("/topic/<int:topic_id>/sendmessage", methods=["post"])
def sendmessage(topic_id):
    if users.token() != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    user_id = users.user_id()
    if user_id == 0:
        return redirect("/topic/" + str(topic_id) + "/newmessage")
    sql_report = messages.send(content, topic_id, user_id)
    if sql_report[0]:
        return redirect('/topic/' + str(topic_id))
    return render_template("newmessage.html", t_id=topic_id, message=sql_report[1], additional=sql_report[2])

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql_report = users.login(username, password)
        if sql_report[0]:
            return redirect("/")
        return render_template("login.html", message=sql_report[1], additional=sql_report[2])
    return render_template("login.html")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get","post"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        passwordconf = request.form["passwordconf"]
        sql_report = users.register(username, password, passwordconf)
        if sql_report[0]:
            return redirect("/")
        else:
            return render_template("register.html",message=sql_report[1],additional=sql_report[2])
    return render_template("register.html")