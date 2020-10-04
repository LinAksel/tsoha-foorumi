from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username,password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return [False, 'Käyttäjätunnusta "' + username + '" ei löydy!', 'Kirjoitiko tunnuksen oikein?']
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = username
            return [True]
        else:
            return [False, 'Salasana on väärä!', '']

def logout():
    del session["user_id"]

def register(username,password,passwordconf):
    if password != passwordconf:
        return [False, 'Salasanat eivät täsmää!', 'Tarkista salasanan oikeinkirjoitus']
    if(len(username) < 3):
        return [False, 'Käyttäjänimi on liian lyhyt!', 'Minimipituus kolme merkkiä']
    if(len(password) < 6):
        return [False, 'Salasana on liian lyhyt!', 'Minimipituus kuusi merkkiä']
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,FALSE)"
        db.session.execute(sql, {"username":username,"password":hash_value})
        db.session.commit()
    except:
        return [False, 'Käyttäjänimi on varattu!', 'Kokeile toista käyttäjänimeä']
    return login(username,password)

def user_id():
    return session.get("user_id",0)
    
def username():
    return session.get("username", 0)