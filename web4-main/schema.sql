CREATE TABLE IF NOT EXISTS role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS user_account (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL, 
    hashed_password VARCHAR(32) NOT NULL, -- MD5 produces 32-character hashes
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50), 
    role_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

INSERT INTO role (name, description) VALUES ('admin', 'Администратор');
INSERT INTO role (name, description) VALUES ('user', 'Пользователь');

-- Hashing passwords using MD5
INSERT INTO user_account (username, hashed_password, first_name, middle_name, role_id)
VALUES ('admin', 'password123', 'admin', NULL, 1);

INSERT INTO user_account (username, hashed_password, first_name, middle_name, role_id)
VALUES ('user1', 'password456', 'user1', NULL, 2);

INSERT INTO user_account (username, hashed_password, first_name, middle_name, role_id)
VALUES ('user2', 'password789', 'user2', NULL, 2);
