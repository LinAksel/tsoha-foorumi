from db import db
import users

def get_topic_list():
    sql = """SELECT T.id, T.topic, COUNT(*) AS maara FROM topics T 
             JOIN messagetopics MT ON MT.topic_id=T.id 
             GROUP BY T.topic, T.id 
             ORDER BY maara DESC LIMIT 10"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_full_topic_list():
    sql = """SELECT T.id, T.topic
             FROM topics T
             ORDER BY T.topic"""
    result = db.session.execute(sql)
    return result.fetchall()

def get_topic_name(topic_id):
    sql = """SELECT topic
             FROM topics
             WHERE topics.id=:topic_id"""
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def send(topic):
    if len(topic) > 40:
        return [False, 'Aihe on liian pitkä!']
    if len(topic) < 3:
        return [False, 'Aihe on liian lyhyt!']
    try:
        sql = """INSERT INTO topics (topic, sent_at) 
                 VALUES (:topic, NOW())"""
        db.session.execute(sql, {"topic":topic})
        db.session.commit()
    except:
        return [False, 'Aihe on jo olemassa!']
    return [True, 'Aiheen luonti onnistui!']

def sendsuggestion(topic, user_id):
    if len(topic) > 40:
        return [False, 'Ehdotus on liian pitkä!']
    if len(topic) < 3:
        return [False, 'Ehdotus on liian lyhyt!']
    try:
        sql = """INSERT INTO topicideas (user_id, topic, sent_at)
                 VALUES (:user_id, :topic, NOW())"""
        db.session.execute(sql, {"user_id":user_id, "topic":topic})
        db.session.commit()
    except:
        return [False, 'Aihetta on jo ehdotettu!']
    return [True, 'Ehdotuksesti on lähetetty ylläpidolle!']