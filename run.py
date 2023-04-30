from window import Tk, MainView
from api_requests import  SpotifyAuthenticator, SpotifyAnalyzer
from config import client_id, client_secret
from json import dumps
class Application:
    def main(self):
        """
        root = Tk()
        root.title('Page Switcher')
        root.geometry('600x500')
        main_view = MainView(root)
        main_view.pack(fill='both', expand=True)
        root.mainloop()
        """
        
        authenticator = SpotifyAuthenticator(client_id, client_secret)

        spotify_instance = authenticator.get_spotify_instance()
        analyzer = SpotifyAnalyzer(spotify_instance)

        artist_name  = "Coldplay" #input("Podaj nazwę artysty: ")
        artist_id = analyzer.get_artist_id(artist_name)
        
        
         
        if artist_id:
            #artist_info = analyzer.get_artist_info(artist_id)

            #print(f"\nArtist info:\n{dumps(artist_info, indent=4)}")

            albums = analyzer.get_all_albums(artist_id)
            print("\nAlbums:")
            analyzer.display_albums(albums)
            album_choice = input("\nEnter album number to display its tracks: ")
            
            album_uri = albums[int(album_choice) - 1]['uri']
            tracks = analyzer.get_tracks_from_album(album_uri)
            print(f"\nTracks from album '{albums[int(album_choice) - 1]['name']}':")
            analyzer.display_tracks(tracks)
            selected_track_index = int(input('Enter track number: ')) - 1
            track_uri = tracks[selected_track_index]['uri']
            analyzer.get_track_info(track_uri)


        else:
            print("\nArtist not found. Program terminated.")




        """
          album_info = analyzer.get_album_info('Rockstart do zachodu słońca')
        print(album_info)
        
        artist_info = analyzer.get_artist_info(artist_id)
        print(artist_info)
        



        track_info = analyzer.get_track_info('Morgan')
        print(track_info)

        
        
        
        
        
        """
    


if __name__=="__main__":
    app = Application()
    app.main()      

