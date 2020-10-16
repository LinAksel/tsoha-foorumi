from db import db
import users

def get_message_list(topic_id):
    sql = """SELECT M.content, U.username, M.id, M.user_id 
             FROM users U, messages M, messagetopics MT, topics T
             WHERE MT.topic_id = T.id AND MT.message_id = M.id AND T.id=:topic_id AND M.user_id = U.id 
             ORDER BY M.sent_at DESC"""
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_users_messages(user_id):
    sql = """SELECT M.content, M.sent_at, T.topic, M.id
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
    user_id = users.user_id()
    sql = "SELECT user_id FROM messages WHERE id=:message_id"
    result = db.session.execute(sql, {"message_id":message_id})
    U_id = result.fetchall()[0][0]
    if user_id != U_id:
        return False
    try:
        sql = "UPDATE messages SET content=:content, sent_at = NOW() WHERE user_id=:user_id AND message_id=:message_id"
        db.session.execute(sql, {"content":content,"user_id":user_id,"message_id":message_id})
        db.session.commit()
    except:
        return False
    return True

def send(content, topic_id):
    user_id = users.user_id()
    if user_id == 0 or len(content) > 500 or len(content) == 0:
        return False
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
        return False
    return True