from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = """SELECT password, id, admin
             FROM users
             WHERE username=:username"""
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return [False, 'Käyttäjätunnusta "' + username + '" ei löydy!', 'Kirjoitiko tunnuksen oikein?']
    if check_password_hash(user[0],password):
        session["user_id"] = user[1]
        session["username"] = username
        session["admin"] = user[2]
        return [True]
    return [False, 'Salasana on väärä!', '']

def logout():
    try:
        del session["user_id"]
        del session["username"]
        del session["admin"]
    except:
        return ['Olet jo kirjautunut ulos!']

def register(username,password,passwordconf):
    if password != passwordconf:
        return [False, 'Salasanat eivät täsmää!', 'Tarkista salasanan oikeinkirjoitus']
    if(len(username) < 3):
        return [False, 'Käyttäjänimi on liian lyhyt!', 'Minimipituus kolme merkkiä']
    if(len(password) < 6):
        return [False, 'Salasana on liian lyhyt!', 'Minimipituus kuusi merkkiä']
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username,password,admin)
                 VALUES (:username,:password,1)"""
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return [False, 'Käyttäjänimi on varattu!', 'Kokeile toista käyttäjänimeä']
    return login(username,password)

def add_info(user_id, about, info):
    sql = """INSERT INTO userinfo (user_id, about, info)
             VALUES (:user_id, :about, :info)"""
    db.session.execute(sql, {"user_id":user_id,"about":about,"info":info})
    db.session.commit()

def update_info(info_id, about, info):
    sql = """UPDATE userinfo 
             SET about=:about, info=:info
             WHERE id=:info_id"""
    db.session.execute(sql, {"about":about,"info":info,"id":info_id})
    db.session.commit()

def user_id():
    return session.get("user_id",0)
    
def username():
    return session.get("username", 0)

def admin():
    return session.get("admin", 0)