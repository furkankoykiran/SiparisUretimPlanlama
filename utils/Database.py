import sqlite3
import time

class Database:
    def __init__(self, database_path, timeout=5.0, max_retries=5, retry_delay=1.0):
        self.database_path = database_path
        self.timeout = timeout
        self.max_retries = max_retries  # Maksimum tekrar deneme sayısı
        self.retry_delay = retry_delay  # Her tekrar deneme arasında bekleme süresi (saniye)

    def connect(self):
        return sqlite3.connect(self.database_path, timeout=self.timeout, check_same_thread=False)

    def select(self, query, params=None):
        for attempt in range(self.max_retries):
            try:
                conn = self.connect()
                cursor = conn.cursor()
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                result = cursor.fetchall()
                conn.close()
                return result
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print(f"Database is locked, retrying... ({attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    raise e  # Diğer hatalar için normalde işleyişi boz
        raise sqlite3.OperationalError("Max retries reached: database is still locked.")

    def execute(self, query, params=None):
        for attempt in range(self.max_retries):
            try:
                conn = self.connect()
                cursor = conn.cursor()
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                conn.commit()
                conn.close()
                return
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    print(f"Database is locked, retrying... ({attempt + 1}/{self.max_retries})")
                    time.sleep(self.retry_delay)
                else:
                    raise e
        raise sqlite3.OperationalError("Max retries reached: database is still locked.")