CREATE TABLE IF NOT EXISTS accounts (
    discord_id INTEGER NOT NULL, 
    ic_id INTEGER NOT NULL, 
    linked_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS guilds (
    guild_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS colors (
    user_id INTEGER NOT NULL, 
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    color INTEGER NOT NULL, 
    upvotes INTEGER NOT NULL DEFAULT 1, 
    downvotes INTEGER NOT NULL DEFAULT 0, 
    created INTEGER NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    tag_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS color_tags (
    submission_id INTEGER NOT NULL, 
    tag_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS color_votes (
    user_id INTEGER NOT NULL, 
    submission_id INTEGER NOT NULL, 
    vote INTEGER NOT NULL
);
