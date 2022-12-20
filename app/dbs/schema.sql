DROP TABLE IF EXISTS trenink;

CREATE TABLE trenink (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dates DATE NOT NULL,
    timeInMinutes DOUBLE NOT NULL,
    programmingLang TEXT NOT NULL,
    rating INT NOT NULL,
    description TEXT NOT NULL

);