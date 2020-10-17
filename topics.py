from db import db
import users

def get_topic_list():
    sql = "SELECT T.id, T.topic, COUNT(*) AS maara FROM topics T LEFT JOIN messagetopics MT ON MT.topic_id = T.id GROUP BY T.topic, T.id ORDER BY maara DESC LIMIT 10"
    result = db.session.execute(sql)
    return result.fetchall()

def get_full_topic_list():
    sql = "SELECT T.id, T.topic FROM topics T ORDER BY T.topic"
    result = db.session.execute(sql)
    return result.fetchall()

def get_topic_name(topic_id):
    sql = "SELECT topic FROM topics WHERE topics.id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
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

def sendsuggestion(topic):
    user_id = users.user_id()
    if user_id == 0 or len(topic) > 30 or len(topic) == 0:
        return False
    try:
        sql = "INSERT INTO topicideas (user_id, topic, sent_at) VALUES (:user_id, :topic, NOW())"
        db.session.execute(sql, {"user_id":user_id, "topic":topic})
        db.session.commit()
    except:
        return False
    return True