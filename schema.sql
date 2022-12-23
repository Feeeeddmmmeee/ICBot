DROP TABLE IF EXISTS color_tags;
DROP TABLE IF EXISTS colors;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS color_votes;

CREATE TABLE IF NOT EXISTS accounts (
    discord_id INTEGER, 
    ic_id INTEGER, 
    linked_at INTEGER
);

CREATE TABLE IF NOT EXISTS guilds (
    guild_id INTEGER
);

CREATE TABLE IF NOT EXISTS colors (
    user_id INTEGER, 
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    color INTEGER, 
    upvotes INTEGER DEFAULT 1, 
    downvotes INTEGER DEFAULT 0, 
    created INTEGER,
    name TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    tag_name TEXT
);

CREATE TABLE IF NOT EXISTS color_tags (
    submission_id INTEGER, 
    tag_id INTEGER
);

CREATE TABLE IF NOT EXISTS color_votes (
    user_id INTEGER, 
    submission_id INTEGER, 
    vote INTEGER
);