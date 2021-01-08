CREATE TABLE "Head" (
        head_id INTEGER NOT NULL,
        headname VARCHAR,
        PRIMARY KEY (head_id),
        UNIQUE (headname),
        wid SERIAL NOT NULL,
        uah INTEGER
)
CREATE TABLE wallets (
        user_id INTEGER NOT NULL,
        name VARCHAR,
        uah BIGINT,
        owner_uid INTEGER,
        PRIMARY KEY (user_id),
        UNIQUE (name),
        FOREIGN KEY(owner_uid) REFERENCES "User" (user_id)
)


CREATE TABLE "User" (
        user_id INTEGER NOT NULL,
        username VARCHAR,
        PRIMARY KEY (id),
        password VARCHAR NOT NULL,
        p_uah INTEGER,
        family_uah INTEGER,
        UNIQUE (username),
        wid SERIAL NOT NULL,
        owner_uid INTEGER,
        PRIMARY KEY (wid),
        FOREIGN KEY(owner_uid) REFERENCES Head (wid)
)




CREATE TABLE transactions (
        amount BIGINT,
        user_id INTEGER NOT NULL,
        from_wallet_wid INTEGER,
        to_wallet_wid INTEGER,
        PRIMARY KEY (user_id),
        FOREIGN KEY(from_wallet_wid) REFERENCES wallets (user_id),
        FOREIGN KEY(to_wallet_wid) REFERENCES wallets (user_id)
)



























