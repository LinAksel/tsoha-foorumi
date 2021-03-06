from db import db
import users

def get_message_list(topic_id):
    sql = """SELECT M.content, U.username, M.id, M.user_id,
             EXTRACT(YEAR FROM AGE(NOW(), M.sent_at)),
             EXTRACT(MONTH FROM AGE(NOW(), M.sent_at)),
             EXTRACT(DAY FROM AGE(NOW(), M.sent_at)),
             EXTRACT(HOUR FROM AGE(NOW(), M.sent_at)),
             EXTRACT(MINUTE FROM AGE(NOW(), M.sent_at))
             FROM users U, messages M, messagetopics MT, topics T
             WHERE MT.topic_id=T.id AND MT.message_id=M.id AND T.id=:topic_id AND M.user_id=U.id 
             ORDER BY M.sent_at DESC"""
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_flagged_message_list():
    sql = """SELECT M.content, U.username, M.id,
             EXTRACT(YEAR FROM AGE(NOW(), M.sent_at)),
             EXTRACT(MONTH FROM AGE(NOW(), M.sent_at)),
             EXTRACT(DAY FROM AGE(NOW(), M.sent_at)),
             EXTRACT(HOUR FROM AGE(NOW(), M.sent_at)),
             EXTRACT(MINUTE FROM AGE(NOW(), M.sent_at))
             FROM users U, messages M, flags F
             WHERE F.message_id=M.id AND U.id=M.user_id 
             ORDER BY M.sent_at DESC"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_m_user_id(message_id):
    sql = """SELECT user_id
             FROM messages
             WHERE id=:message_id"""
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()

def get_message(message_id):
    sql = """SELECT content, user_id
             FROM messages
             WHERE id=:message_id"""
    result = db.session.execute(sql, {"message_id":message_id})
    return result.fetchone()

def get_users_messages(user_id):
    sql = """SELECT M.content, DATE_TRUNC('second', M.sent_at), T.topic, M.id
             FROM users U, messages M, messagetopics MT, topics T
             WHERE MT.topic_id = T.id AND MT.message_id = M.id AND M.user_id = U.id AND U.id=:user_id 
             ORDER BY M.sent_at DESC"""
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def delete_message(message_id):
    sql = """DELETE FROM messages MT 
             WHERE MT.id=:message_id"""
    db.session.execute(sql, {"message_id":message_id})
    db.session.commit()

def update_message(message_id, content):
    sql = """UPDATE messages 
            SET content=:content
            WHERE id=:message_id"""
    db.session.execute(sql, {"content":content,"message_id":message_id})
    db.session.commit()

def send(content, topic_id, user_id):
    if len(content) > 500:
        return [False, 'Viesti on liian pitkä!', 'Maksimimäärä on 500 merkkiä']
    if len(content) < 2:
        return [False, 'Viesti on liian lyhyt!', 'Minimipituus on kaksi merkkiä']
    try:
        sql = "INSERT INTO messages (user_id, content, sent_at) VALUES (:user_id, :content, NOW())"
        db.session.execute(sql, {"user_id":user_id, "content":content})
        db.session.commit()
        sql = "SELECT id FROM messages WHERE content=:content"
        result = db.session.execute(sql, {"content":content})
        M_id = result.fetchall()[0][0]
        sql = "INSERT INTO messagetopics (topic_id, message_id) VALUES (:topic_id, :message_id)"
        db.session.execute(sql, {"topic_id":topic_id, "message_id":M_id})
        db.session.commit()
    except:
        return [False, 'Viestin lähettäminen epäonnistui!', 'Oletko kirjautunut sisään?']
    return [True, 'Viestin lähettäminen onnistui!', '']

def flag(message_id, user_id):
    sql = """INSERT INTO flags (message_id, user_id)
             VALUES (:message_id, :user_id)"""
    db.session.execute(sql, {"message_id":message_id,"user_id":user_id})
    db.session.commit()