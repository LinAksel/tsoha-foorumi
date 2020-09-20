CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    admin BOOLEAN,
    password TEXT
);
CREATE TABLE userinfo (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    key TEXT,
    val TEXT
);
CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    topic TEXT UNIQUE,
    sent_at TIMESTAMP
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TIMESTAMP
);
CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    about TEXT,
    created_at TIMESTAMP
);
CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls,
    choice TEXT
);
CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices,
    sent_at TIMESTAMP
);
    


