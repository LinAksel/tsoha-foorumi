from db import db
import users

def get_topic_list():
    sql = "SELECT T.id, T.topic, U.username, T.sent_at FROM topics T, users U WHERE T.user_id=U.id ORDER BY T.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(topic):
    user_id = users.user_id()
    if user_id == 0 or len(topic) > 30:
        return False
    try:
        sql = "INSERT INTO topics (topic, user_id, sent_at) VALUES (:topic, :user_id, NOW())"
        db.session.execute(sql, {"topic":topic, "user_id":user_id})
        db.session.commit()
    except:
        return False
    return True