from db import db
import users

def get_message_list(topic_id):
    sql = "SELECT M.content, M.sent_at FROM messages M, messagetopics MT WHERE MT.topic_id=:topic_id AND M.id = MT.message_id ORDER BY M.sent_at"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def send(content, topic_id):
    user_id = users.user_id()
    if user_id == 0 or len(content) > 500 or len(content) == 0:
        return False
    try:
        sql = "INSERT INTO messages (user_id, content, sent_at) VALUES (:user_id, :content, NOW())"
        db.session.execute(sql, {"user_id":user_id, "content":content})
        db.session.commit()
        sql = "SELECT M.id FROM messages M WHERE M.content=:content AND M.user_id=:user_id"
        result = db.session.execute(sql, {"content":content, "user_id":user_id})
        M_id = result.fetchall()[0]
        sql = "INSERT INTO messagetopics (topic_id, message_id) VALUES (:topic_id, :message_id)"
        db.session.execute(sql, {"topic_id":topic_id, "message_id":M_id})
        db.session.commit()
    except:
        return False
    return True