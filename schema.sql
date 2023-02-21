DROP TABLE IF EXISTS hackers;

DROP TABLE IF EXISTS skills;

CREATE TABLE hackers (
    id INTEGER,
    name TEXT,
    company TEXT,
    email TEXT,
    phone TEXT
);

CREATE TABLE skills (
    skill TEXT,
    rating INTEGER,
    hacker INTEGER
    -- UNIQUE(skill, hacker)
);

CREATE UNIQUE INDEX idx ON skills (skill, hacker);