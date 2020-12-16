CREATE TABLE "User" (
        user_id INTEGER NOT NULL,
        username VARCHAR,
        PRIMARY KEY (id),
        UNIQUE (username)
)
CREATE TABLE wallets (
        owner_id INTEGER,
        user_id INTEGER NOT NULL,
        name VARCHAR,
        uah INTEGER,
        PRIMARY KEY (user_id),
        FOREIGN KEY(owner_id) REFERENCES "User" (user_id)
)




























CREATE TABLE transactions (
	user_id INTEGER NOT NULL,
	comment VARCHAR,
	amount INTEGER,
	PRIMARY KEY (user_id)
	FOREIGN KEY(from_wallet) REFERENCES Wallets(user_id)
	FOREIGN KEY(to_wallet) REFERENCES Wallets(user_id)

)
