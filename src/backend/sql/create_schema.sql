DROP IF EXISTS persons, roles, admins, events;

-- SET foreign keys to be enforced
PRAGMA foreign_keys = ON;
-- define tables with foreign and primary keys
CREATE TABLE persons (
    person_id INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    card_id VARCHAR,
    created DATETIME,
    added_by INTEGER,
    role INTEGER,
    FOREIGN KEY role REFERENCES roles(role_id)
);

CREATE TABLE roles (
    role_id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(10),
    can_unlock INTEGER,
    can_manage INTEGER,
    can_access_history INTEGER
);

CREATE TABLE admins (
    admin_id INTEGER NOT NULL PRIMARY KEY,
    password VARCHAR,
    FOREIGN KEY admin_id REFERENCES persons(person_id)
);

CREATE TABLE events (
    event_id INTEGER NOT NULL PRIMARY KEY,
    event VARCHAR(10),
    time DATETIME,
    user INTEGER
);
