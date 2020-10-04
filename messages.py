from db import db
import users

def get_message_list(topic_id):
    sql = "SELECT M.content FROM messages M, messagetopics MT, topics T WHERE MT.topic_id = T.id AND MT.message_id = M.id AND T.id=:topic_id ORDER BY M.sent_at"
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
        sql = "SELECT id FROM messages WHERE content=:content"
        result = db.session.execute(sql, {"content":content})
        M_id = result.fetchall()[0][0]
        sql = "INSERT INTO messagetopics (topic_id, message_id) VALUES (:topic_id, :message_id)"
        db.session.execute(sql, {"topic_id":topic_id, "message_id":M_id})
        db.session.commit()
    except:
        return False
    return True