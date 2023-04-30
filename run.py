from window import *
from api_requests import  *

class Application:
    def main(self):
        root = Tk()
        root.title('Page Switcher')
        root.geometry('600x500')
        
        main_view = MainView(root)
        main_view.pack(fill='both', expand=True)
        
        spotify_instance = authenticator.get_spotify_instance()
        analyzer = SpotifyAnalyzer(spotify_instance)

    
        artist_id = analyzer.get_artist_id('Steez83')
        print(artist_id)
        
        artist_info = analyzer.get_artist_info(artist_id)
        print(artist_info)
        
        all_albums = list(analyzer.get_all_albums(artist_id))
        for album in all_albums: print(album)

        
        album_info = analyzer.get_album_info('Rockstart do zachodu słońca')
        print(album_info)
        """



        #track_info = analyzer.get_track_info('Młody Książe')
        #print(track_info)

        #root.mainloop()
        """







if __name__=="__main__":
    app = Application()
    app.main()      

