from sqlite3 import connect
from os.path import dirname, join, abspath

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = connect(self.db_path)

    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def create_table(self, liczba_kolumn):
        self.conn.execute("DROP TABLE IF EXISTS SpotifyCrawler")

        query = self._generate_create_table_query(liczba_kolumn)
        self.conn.execute(query)
        self.conn.commit()
        print("Utworzono tabelę w bazie danych.")

    def add_records(self, liczba_kolumn):
        for i in range(1, liczba_kolumn + 1):
            values = (i,) + tuple(f"Wiersz {i}-Kolumna {j}" for j in range(1, liczba_kolumn + 1))
            query = self._generate_insert_query(liczba_kolumn)
            self.conn.execute(query, values)
        self.conn.commit()
        print("Dodano rekordy do bazy danych.")

    def _generate_create_table_query(self, liczba_kolumn):
        column_names = ", ".join([f"Column{j} TEXT" for j in range(1, liczba_kolumn + 1)])
        return f"CREATE TABLE IF NOT EXISTS SpotifyCrawler (ID INT PRIMARY KEY NOT NULL, {column_names});"

    def _generate_insert_query(self, liczba_kolumn):
        placeholders = ", ".join(["?" for _ in range(liczba_kolumn + 1)])
        column_names = ", ".join([f"Column{j}" for j in range(1, liczba_kolumn + 1)])
        return f"REPLACE INTO SpotifyCrawler (ID, {column_names}) VALUES ({placeholders});"


if __name__ == "__main__":
    current_dir = dirname(abspath(__file__))
    db_path = join(current_dir, 'baza_danych.db')

    db = Database(db_path)
    db.connect()

    liczba_kolumn = 20

    db.create_table(liczba_kolumn)
    db.add_records(liczba_kolumn)

    db.close()
