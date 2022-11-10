import sqlite3
from config import DATABASE
from app import logger


class Storage:

    def __init__(self):
        self.__connection = sqlite3.connect(DATABASE, check_same_thread=False)
        self.__connection.row_factory = sqlite3.Row
        self.__cursor = self.__connection.cursor()

        with self.__connection:
            self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS storage (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT
                )
            """)

    def key_exists(self, key: str) -> bool:
        result = self.__cursor.execute(f"""
            SELECT * FROM storage WHERE key='{key}'
        """).fetchone()

        if result:
            return True

        return False

    def get_value(self, key: str) -> str | None:
        if not self.key_exists(key):
            return None

        result = self.__cursor.execute(f"""
            SELECT * FROM storage WHERE key='{key}'
        """).fetchone()

        return result["value"]

    def _get_row(self, key: str) -> dict[str, str] | None:
        if not self.key_exists(key):
            return None

        result = self.__cursor.execute(f"""
            SELECT * FROM storage WHERE key='{key}'
        """).fetchone()

        return {
            "id": result["id"],
            "key": result["key"],
            "value": result["value"]
        }

    def remove_key(self, key: str) -> None:
        if not self.key_exists(key):
            raise KeyError("строки с таким ключом не существует")

        self.__cursor.execute(f"""
            DELETE FROM storage WHERE key = '{key}';
        """)
        self.__connection.commit()

    def set_value(self, key: str, value: str):
        if self.key_exists(key):
            current_id = self._get_row(key)["id"]
            self.__cursor.execute(f"""
                REPLACE INTO storage (id, key, value) VALUES ('{current_id}', '{key}', '{value}')
            """)
            self.__connection.commit()
        else:
            self.__cursor.execute(f"""
                INSERT INTO storage (key, value) VALUES ('{key}', '{value}')
            """)
            self.__connection.commit()
