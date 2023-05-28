from sqlite3 import connect
from os import getcwd
from os.path import join
from api_requests import SpotifyAuthenticator, SpotifyRequester
from config import client_id, client_secret
import uuid


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
    
    def create_table(self, record_dict):
        self.conn.execute("DROP TABLE IF EXISTS SpotifyCrawler")
        
        query = self._generate_create_table_query(record_dict)
        self.conn.execute(query)
        self.conn.commit()
        print("Utworzono tabelę w bazie danych.")
    
    def add_records(self, record_dict):
        keys = list(record_dict.keys())
        values = [self._process_value(record_dict[key]) for key in keys]
        query = self._generate_insert_query(keys)
        id_value = str(uuid.uuid4())
        self.conn.execute(query, [id_value] + values)
        self.conn.commit()
        #print("Dodano rekord do bazy danych.")
    
    def _process_value(self, value):
        if isinstance(value, (list, dict, tuple, set)):
            return "brak_wartości"
        return value
    
    def _generate_create_table_query(self, record_dict):
        column_names = ", ".join([f"{key} TEXT" for key in record_dict.keys() if key != 'uuid'])
        return f"CREATE TABLE IF NOT EXISTS SpotifyCrawler (ID TEXT PRIMARY KEY NOT NULL, {column_names});"
    
    def _generate_insert_query(self, keys):
        placeholders = ", ".join(["?" for _ in range(len(keys) + 1)])
        column_names = ", ".join(keys)
        return f"INSERT INTO SpotifyCrawler (ID, {column_names}) VALUES ({placeholders});"

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


