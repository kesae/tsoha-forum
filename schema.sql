CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS boards (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    access_group INTEGER
        REFERENCES groups (id)
        ON DELETE SET NULL;
);
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
        REFERENCES users (id)
        ON DELETE CASCADE,
    title TEXT,
    board_id INTEGER
        REFERENCES boards (id)
        ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER
        REFERENCES users (id)
        ON DELETE CASCADE,
    content TEXT,
    topic_id INTEGER
        REFERENCES topics (id)
        ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    edited_at TIMESTAMPTZ
);
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE,
    description TEXT
);
CREATE TABLE IF NOT EXISTS memberships (
    group_id INTEGER NOT NULL
        REFERENCES groups (id)
        ON DELETE CASCADE,
    user_id INTEGER NOT NULL
        REFERENCES users (id)
        ON DELETE CASCADE,
    CONSTRAINT primary_key
        PRIMARY KEY (group_id, user_id)
);