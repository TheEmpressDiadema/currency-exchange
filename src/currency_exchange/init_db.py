import os
import sqlite3


def create_directory(cwd: str, directory_name: str) -> None:
    if directory_name not in os.listdir(cwd):
        os.mkdir(os.path.join(cwd, directory_name))

def init_db(directory_name: str, db_name: str) -> None:
    cwd = os.getcwd()
    create_directory(cwd, directory_name)

    with sqlite3.connect(os.path.join(directory_name, db_name)) as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS currency(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL CHECK(LENGTH(code) = 3),
            name TEXT NOT NULL CHECK(LENGTH(name) >= 4 AND LENGTH(name) <= 30),
            sign TEXT NOT NULL CHECK(LENGTH(sign) <= 2 AND LENGTH(sign) >  0)
        );

        CREATE TABLE IF NOT EXISTS exchange_rate(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_currency_id INTEGER NOT NULL,
            target_currency_id INTEGER NOT NULL,
            rate DECIMAL(16, 6) NOT NULL,
            UNIQUE(base_currency_id, target_currency_id),
            CHECK(base_currency_id <> target_currency_id),
            FOREIGN KEY (base_currency_id) REFERENCES currency(id),
            FOREIGN KEY (target_currency_id) REFERENCES currency(id)
        )''')