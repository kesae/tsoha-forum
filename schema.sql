CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE COLLATE "fi-FI-x-icu",
    password TEXT,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS boards (
    id SERIAL PRIMARY KEY,
    title TEXT UNIQUE COLLATE "fi-FI-x-icu",
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
    title TEXT COLLATE "fi-FI-x-icu",
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
    title TEXT UNIQUE COLLATE "fi-FI-x-icu",
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