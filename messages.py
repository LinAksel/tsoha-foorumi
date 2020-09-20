from db import db
import users

def get_message_list(topic_id):
    sql = "SELECT M.content, M.sent_at FROM messages M WHERE M.topic_id=:topic_id ORDER BY M.sent_at"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()