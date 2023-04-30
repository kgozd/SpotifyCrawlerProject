from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from config import client_id, client_secret
from json import dumps

class SpotifyAuthenticator:
    def __init__(self, client_id, client_secret):
        self.client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    
    def get_spotify_instance(self):
        return Spotify(client_credentials_manager=self.client_credentials_manager)

    

class SpotifyAnalyzer:
    def __init__(self, spotify_instance):
        self.sp = spotify_instance


    def get_artist_id(self, artist_name):
        result = self.sp.search(artist_name, limit=1, type='artist')
        if result['artists']['items']:
            artist = result['artists']['items'][0]
      
            id_artysty = artist['id']
            
            return  id_artysty
        
    def get_artist_info(self, id_artysty):
        artist = self.sp.artist(id_artysty)
        dict = {
        'name': artist['name'],
        'genres': artist['genres'],
        'popularity': artist['popularity'],
        'followers': artist['followers']['total'],
        'image_url': artist['images'][0]['url'] if artist['images'] else None,
        'artist_id': artist['id']
        }
        print(dumps(dict, indent=4))

        return None
    def get_album_info(self, album_name):
        result = self.sp.search(album_name, limit=1, type='album')
        if result['albums']['items']:
            album = result['albums']['items'][0]
            dict= {
                'name': album['name'], 
                'type': album['album_type'],
                'total_tracks': album["total_tracks"],
                'uri': album['uri'],
                'release_date': album["release_date"],
                'artists': [artist['name'] for artist in album['artists']],
                'external_urls': album['external_urls']['spotify'],
                #'images': album['images'],
                'image_url': album['images'][0]['url'] if album['images'] else None,

            }
            
            print(dumps(dict, indent=4))

        return None
    
    def get_all_albums(self, artist_id):
        albums = []
        results = self.sp.artist_albums(artist_id, album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return [{
            'name': album['name'],
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'uri': album['uri']

        } for album in albums ]

    def get_track_info(self, track_name):
        result = self.sp.search(track_name, limit=10, type='track')
        if result['tracks']['items']:
            track = result['tracks']['items'][0]
            track_id = track['id']
            audio_features = self.sp.audio_features(track_id)[0]
            dict =  {
                'album_name': track['album']['name'], # nazwa albumu, na którym jest utwór
                'album_release_date': track['album']['release_date'], # data wydania albumu
                'artist_name': track['artists'][0]['name'], # nazwa pierwszego wykonawcy utworu
                'artist_genres': self.sp.artist(track['artists'][0]['id'])['genres'], # gatunki muzyczne wykonawcy
                'name': track['name'], 
                'duration': track['duration_ms']/60000,\
                'popularity': track['popularity'],
                'danceability': audio_features['danceability'], # wskaźnik taneczności utworu
                'energy': audio_features['energy'], # wskaźnik energiczności utworu
                'key': audio_features['key'], # tonacja utworu
                'loudness': audio_features['loudness'], # głośność utworu w decybelach
                'mode': audio_features['mode'], # tryb tonacji utworu (0 - minor, 1 - major)
                'speechiness': audio_features['speechiness'], # wskaźnik ilości mowy w utworze
                'acousticness': audio_features['acousticness'], # wskaźnik akustyczności utworu
                'instrumentalness': audio_features['instrumentalness'], # wskaźnik instrumentalności utworu
                'liveness': audio_features['liveness'], # wskaźnik nastrajania publiczności podczas nagrania
                'valence': audio_features['valence'], # wskaźnik pozytywnego nastawienia w utworze
                'tempo': audio_features['tempo'], # tempo utworu w uderzeniach na minutę
                'preview_url': track['preview_url'], # adres URL do fragmentu utworu do odsłuchania
                'external_urls': track['external_urls'], # zewnętrzne adresy URL związane z utworem
                #'available_markets': track['available_markets'] # kraje, w których utwór jest dostępny
            }
    
          
            print(dumps(dict, indent=4))
        return None

authenticator = SpotifyAuthenticator(client_id, client_secret)
