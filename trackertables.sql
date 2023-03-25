CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT,
    age TEXT,
    hash TEXT
);

CREATE TABLE timestables (
    user_id TEXT NOT NULL,
    twoXPoints INTEGER,
    threeXPoints INTEGER,
    fourXPoints INTEGER,
    fiveXPoints INTEGER,
    sixXPoints INTEGER,
    sevenXPoints INTEGER,
    eightXPoints INTEGER,
    nineXPoints INTEGER,
    tenXPoints INTEGER,
    elevenXPoints INTEGER,
    twelveXPoints INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE spelling (
    user_id TEXT NOT NULL,
    threeLettPoints INTEGER,
    fourLettPoints INTEGER,
    fiveLettPoints INTEGER,
    sixLettPoints INTEGER,
    sevenLettPoints INTEGER,
    eightLettPoints INTEGER,
    nineLettPoints INTEGER,
    tenLettPoints INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);


SELECT SUM(twoXPoints + threeXPoints + fourXPoints + fiveXPoints + sixXPoints + sevenXPoints + eightXPoints + nineXPoints + tenXPoints + elevenXPoints + twelveXPoints)
    FROM timestables
    WHERE user_id = 13;

SELECT SUM(threeLettPoints + fourLettPoints + fiveLettPoints + sixLettPoints + sevenLettPoints + eightLettPoints + nineLettPoints + tenLettPoints)
    AS total
    FROM spelling
    WHERE user_id = 13;