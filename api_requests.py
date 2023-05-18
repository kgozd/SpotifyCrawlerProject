from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
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
            return  artist['id']
            
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
        #print(dumps(dict, indent=4))
        return dict
   
    def get_album_info(self, album_uri):
        album = self.sp.album(album_uri)
        dict= {
            'name': album['name'], 
            'type': album['album_type'],
            'total_tracks': album["total_tracks"],
            'uri': album['uri'],
            'release_date': album["release_date"],
            'artists': [artist['name'] for artist in album['artists']],
            'external_urls': album['external_urls']['spotify'],
            'images': album['images'],
            'image_url': album['images'][0]['url'] if album['images'] else None,
        }
        #print(dumps(dict, indent=4))
        return dict
       
    def get_all_albums(self, artist_id):
        albums = []
        results = self.sp.artist_albums(artist_id, album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums
    """
    def display_albums(self, albums):
        album_names = []
        for i, album in enumerate(albums):
            if album['name'] not in album_names:
                album_names.append(album['name'])
                return f"{len(album_names)}. {album['name']} ({album['release_date']})"
    """    
    
    def get_tracks_from_album(self, album_uri):
        tracks = []
        results = self.sp.album_tracks(album_uri)
        tracks.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks
    
    """  
    def display_tracks(self, tracks):
        for i, track in enumerate(tracks):
            time_in_minutes = round(track['duration_ms']/60000,2)
            print(f"{i + 1}. {track['name']} ({time_in_minutes} min)")
    """     
    
    def get_track_info(self, track_uri):
        track = self.sp.track(track_uri)
        audio_features = self.sp.audio_features(track_uri)[0]
        dict = ({
            'album_name': track['album']['name'], # nazwa albumu, na którym jest utwór
            'album_release_date': track['album']['release_date'], # data wydania albumu
            'artist_name': track['artists'][0]['name'], # nazwa pierwszego wykonawcy utworu
            'artist_genres': self.sp.artist(track['artists'][0]['id'])['genres'], # gatunki muzyczne wykonawcy
            'name': track['name'], 
            'duration minutes': round(track['duration_ms']/60000,2),
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
        })
        #print(dumps(dict, indent=4))
        return dict

    """        
    def get_all_albums(self, artist_id):
        albums = []
        results = self.sp.artist_albums(artist_id, album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        
        # Print list of albums and allow user to choose which album to view details
        print("Albums:")
        for i, album in enumerate(albums):
            print(f"{i+1}. {album['name']} ({album['release_date']})")
        album_choice = input("Choose an album (enter the number): ")
        
        # Get details of chosen album
        chosen_album = albums[int(album_choice)-1]
        album_dict = {
            'name': chosen_album['name'],
            'release_date': chosen_album['release_date'],
            'total_tracks': chosen_album['total_tracks'],
            'uri': chosen_album['uri']
        }
        print(dumps(album_dict, indent=4))
        """
          
        
