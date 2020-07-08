import sqlite3
import hashlib


class DBController:
    def __init__(self):
        self._conn = sqlite3.connect('main.db')
        self._curs = self._conn.cursor()

    def validateUser(self, name, password):
        name = hashlib.md5(name.encode('UTF-8'))
        password = hashlib.md5(password.encode('UTF-8'))
        name = name.digest()
        password = password.digest()

    def __del__(self):
        self._conn.commit()
        self._conn.close()
