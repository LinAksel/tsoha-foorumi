from db import db
import users

def get_topic_list():
    sql = "SELECT id, topic, sent_at FROM topics ORDER BY sent_at DESC LIMIT 10"
    result = db.session.execute(sql)
    return result.fetchall()

def send(topic):
    user_id = users.user_id()
    if user_id == 0 or len(topic) > 30 or len(topic) == 0:
        return False
    try:
        sql = "INSERT INTO topics (topic, sent_at) VALUES (:topic, NOW())"
        db.session.execute(sql, {"topic":topic})
        db.session.commit()
    except:
        return False
    return True