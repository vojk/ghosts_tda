CREATE TABLE "records"
(
    "id"              INTEGER,
    "dates"           DATE NOT NULL,
    "timeInMinutes"   INT  NOT NULL,
    "programmingLang" TEXT NOT NULL,
    "rating"          INT  NOT NULL,
    "description"     TEXT NOT NULL,
    "user_id"         INT  NOT NULL,
    PRIMARY KEY ("id" AUTOINCREMENT)
);

CREATE TABLE "users"
(
    "id"        INTEGER NOT NULL,
    "username"  TEXT,
    "firstname" TEXT,
    "lastname"  TEXT,
    "password"  TEXT,
    "email"     TEXT,
    "role"      TEXT,
    PRIMARY KEY ("id" AUTOINCREMENT)
);

INSERT INTO "users" (username, password, role)
VALUES ("admin", "123456", "admin");

CREATE TABLE "categories"
(
    "id"          INTEGER,
    "category"    TEXT NOT NULL,
    "color"       TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "user_id"     INT  NOT NULL,
    PRIMARY KEY ("id" AUTOINCREMENT)
);


CREATE TABLE categories_records
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    record_id   INTEGER,
    user_id     INTEGER,
    FOREIGN KEY (record_id) REFERENCES records (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);