CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    admin BOOLEAN,
    password TEXT
);

CREATE TABLE messages
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE userinfo
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    about TEXT,
    info TEXT
);

CREATE TABLE favouritemessages
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages
);

CREATE TABLE topicideas
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    topic TEXT UNIQUE,
    sent_at TIMESTAMP
);

CREATE TABLE topics
(
    id SERIAL PRIMARY KEY,
    topic TEXT UNIQUE,
    sent_at TIMESTAMP
);

CREATE TABLE flags
(
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages,
    user_id INTEGER REFERENCES users,
    content TEXT UNIQUE,
    sent_at TIMESTAMP
);

CREATE TABLE messagetopics
(
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    message_id INTEGER REFERENCES messages ON DELETE CASCADE
);

