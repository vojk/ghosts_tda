DROP TABLE IF EXISTS trenink;

CREATE TABLE trenink
(
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    dates           DATE   NOT NULL,
    timeInMinutes   DOUBLE NOT NULL,
    programmingLang TEXT   NOT NULL,
    rating          INT    NOT NULL,
    description     TEXT   NOT NULL,
    programmer      TEXT   NOT NULL
);