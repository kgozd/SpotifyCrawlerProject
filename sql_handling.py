from sqlite3 import connect
from os import getcwd
from os.path import join
from api_requests import SpotifyAuthenticator, SpotifyRequester
from config import client_id, client_secret
from uuid import uuid4

import threading





class Database:
    def __init__(self):
        self.conn = None
        #self.sp_authenticator = SpotifyAuthenticator(client_id, client_secret)
        #self.sp_requester = SpotifyRequester(self.sp_authenticator.get_spotify_instance())
    def connect(self,db_path):
        self.conn = connect(db_path)
    
    
    def close(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def create_table(self, record_dict, table_to_create):
        self.table_to_create= table_to_create
        self.record_dict = record_dict
        self.conn.execute(f"DROP TABLE IF EXISTS {self.table_to_create}")
        
        query = self._generate_create_table_query(record_dict)
        self.conn.execute(query)
        self.conn.commit()
        print("Utworzono tabelę w bazie danych.")
    
    def add_records(self, record_dict):
        keys = list(record_dict.keys())
        values = [self._process_value(record_dict[key]) for key in keys]
        query = self._generate_insert_query(keys)
        id_value = str(uuid4())
        self.conn.execute(query, [id_value] + values)
        self.conn.commit()
        #print("Dodano rekord do bazy danych.")
    
    def _process_value(self, value):
        if isinstance(value, (list, dict, tuple, set)):
            return "brak_wartości"
        return value
    
    def _generate_create_table_query(self, record_dict):
        column_names = ", ".join([f"{key} TEXT" for key in record_dict.keys()])
        return f"CREATE TABLE IF NOT EXISTS {self.table_to_create} (ID TEXT PRIMARY KEY NOT NULL, {column_names});"
    
    def _generate_insert_query(self, keys):
        placeholders = ", ".join(["?" for _ in range(len(keys) + 1)])
        column_names = ", ".join(keys)
        return f"INSERT INTO {self.table_to_create} (ID, {column_names}) VALUES ({placeholders});"

    def create_av_table(self):
        target_table = f"av_{self.table_to_create}"
        self.conn.execute(f"DROP TABLE IF EXISTS {target_table}")

        # Pobierz listę nazw kolumn z tabeli źródłowej
        column_names = list(self.record_dict.keys())

        av_columns = [f"SUM({column}) / (SELECT COUNT(*) FROM {self.table_to_create}) AS {column}_av" for column in column_names]

        # Tworzenie pustej tabeli
        create_table_query = f"CREATE TABLE {target_table} AS SELECT {', '.join(av_columns)} FROM {self.table_to_create}"
        self.conn.execute(create_table_query)

        self.conn.commit()
        print("Utworzono tabelę z średnimi kolumnami.")



    def retrieve_records(self, table_name, column_to_retrieve, column_name, param_value):
            query = f"SELECT {column_to_retrieve} FROM {table_name} WHERE {column_name} = ?"
            cursor = self.conn.execute(query, (param_value,))
            record = cursor.fetchone()
            if record:
                return record[0]
            else:
                return None


















# def main():
#     current_dir = getcwd()  # Pobranie bieżącego katalogu
#     db_path = join(current_dir, 'baza_danych.db')
    
#     sp_authenticator = SpotifyAuthenticator(client_id, client_secret)
#     sp_requester = SpotifyRequester(sp_authenticator.get_spotify_instance())
    
#     album_id = "spotify:album:1GabBOxzyUPjkELZE0b3HS"
#     tracks = sp_requester.get_tracks_from_album(album_id)
    
#     first_track_uri = tracks[0]['uri']
#     first_track_stats = sp_requester.get_track_info(first_track_uri)
    
#     db = Database()
#     db.connect(db_path)
#     db.create_table(first_track_stats,)
    
#     for track in tracks:
#         track_stats = sp_requester.get_track_info(track['uri'])
#         db.add_records(track_stats)
    
#     db.close()


