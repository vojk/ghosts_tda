CREATE TABLE "records"
(
    "id"              INTEGER,
    "dates"           DATE NOT NULL,
    "timeInMinutes"   INT  NOT NULL,
    "programmingLang" TEXT NOT NULL,
    "rating"          INT  NOT NULL,
    "description"     TEXT NOT NULL,
    "programmer"      TEXT NOT NULL,
    "programmerId"    INT  NOT NULL,
    PRIMARY KEY ("id" AUTOINCREMENT)
);

CREATE TABLE "categories"
(
    "id"          INTEGER,
    "category"    TEXT NOT NULL,
    "color"       TEXT NOT NULL,
    "description" TEXT NOT NULL,
    PRIMARY KEY ("id" AUTOINCREMENT)
);

CREATE TABLE "users"
(
    "id"        INTEGER NOT NULL,
    "username"  TEXT    NOT NULL,
    "firstname" TEXT    NOT NULL,
    "lastname"  TEXT    NOT NULL,
    "password"  TEXT    NOT NULL,
    "email"     TEXT    NOT NULL,
    "role"      TEXT    NOT NULL,
    PRIMARY KEY ("id" AUTOINCREMENT)
);

CREATE TABLE categories
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT NOT NULL,
    color       TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE categories_records
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    record_id   INTEGER,
    FOREIGN KEY (record_id) REFERENCES records (id),
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
)