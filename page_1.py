#my libraries
from page import Page, Labele,ListWithItems

#additional libraries
from tkinter import(
    Frame, Label, Button, Tk, 
    Entry, Listbox, Canvas, END, 
    BooleanVar, Scrollbar, ttk, VERTICAL, 
     SINGLE, Y,LEFT, RIGHT
) 
from customtkinter import(
    CTkScrollbar, CTkTabview, CTkButton, CTkEntry,
    CTkScrollableFrame,
    CTkTextbox, CTkLabel, CTkFont, CTkImage,CTkFrame,CTk
)  
from io import BytesIO
from PIL import ImageTk, Image, ImageDraw
from urllib.request import urlopen
from functools import partial






    





class Page1(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 1")
        self.parent = parent
        self.my_labels = Labele(self)
        self.artist_stats_widget1 = None
        self.artist_stats_widget2 = None
        self.albums_stats_widget1 = None
        self.tracks_stats_widget1 = None
        self.create_widgets()
    def create_widgets(self):            

        self.artist_entry = CTkEntry(self,font=("Arial", 18), height=40, width=50,  placeholder_text="Wpisz Nazwę Artysty")
        self.artist_entry.grid(row=0, column=1,  padx=(25, 0), pady=(15, 5),  sticky="nsew")
        self.artist_entry.grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

            
        self.button_to_request = CTkButton(self, text="Pobierz dane ",font=("Arial", 18,'bold'), height=40,fg_color="#4ddf5d",
                                           text_color="#000000", command=self.enter_artist_name,  hover_color="#3bac47")
        self.button_to_request.grid(row=0, column=3, padx=(20, 0), pady=(15, 5), sticky="nsew", columnspan=1)
        self.button_to_request.grid_columnconfigure(0, weight=1) 
     

        self.artist_info_label = self.my_labels.create_label("Informacje o Artyście",   row=1, column=3, padx=(40, 20), pady=(5, 10), columnspan=3, sticky="new")
        self.artist_image_label = self.my_labels.create_label("Wybierz artystę",   row=2, column=3, padx=(40, 20), pady=(20, 10), sticky="nw")
        self.album_info_label = self.my_labels.create_label("Informacje o Albumie",   row=3, column=3, padx=(40, 20), pady=(10, 10), columnspan=3, sticky="new")
        self.album_cover_label = self.my_labels.create_label("Wybierz album",   row=4, column=3, padx=(40, 20), pady=(10, 10), columnspan=1, sticky="nw")
        self.tracks_info_label = self.my_labels.create_label("Informacje o Utworze",   row=7, column=3, padx=(40, 20), pady=(5, 5), columnspan=3, sticky="nsew")
        self.albums_listbox_label = self.my_labels.create_label("Albumy",   row=1, column=1, padx=(20, 20), pady=(5, 5))
        self.tracks_listbox_label = self.my_labels.create_label("Utwory",   row=7, column=1, padx=(20, 20), pady=(5, 5))



       
        
        self.albums_listbox = Listbox(self, font=("Arial", 12), width=40, height=15, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d", highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.albums_listbox.grid(row=2, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew",rowspan=3)
        self.albums_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self)
        scrollbar_frame.grid(row=2, column=2, padx=(0, 0), pady=(0, 0), sticky="ns",rowspan=4)
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_albums = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.albums_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_albums.pack(fill=Y, side=LEFT)
        self.albums_listbox.configure(yscrollcommand=scrollbar_albums.set)


      

        self.tracks_listbox = Listbox(self, font=("Arial", 12), width=40, height=15, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d", highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.tracks_listbox.grid(row=8, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew")
        self.tracks_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self)
        scrollbar_frame.grid(row=8, column=2, padx=(0, 0), pady=(0, 0), sticky="ns")
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_tracks = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.tracks_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_tracks.pack(fill=Y, side=RIGHT)
        self.tracks_listbox.configure(yscrollcommand=scrollbar_tracks.set)

        

        self.button_clicked = BooleanVar()
        self.button_clicked.set(False)
        self.albums_listbox.bind("<<ListboxSelect>>", self.show_albums)
        self.tracks_listbox.bind("<<ListboxSelect>>", self.show_track_info)
    
    
   
    def enter_artist_name(self):
        artist_name = self.artist_entry.get()
        artist_id = self.sp_analyzer.get_artist_id(artist_name)
        self.artist_id = artist_id
        self.button_clicked.set(True)
        artist_stats= self.sp_analyzer.get_artist_info(artist_id)
        artist_image_url = artist_stats.get('image_url')
        artist_followers = artist_stats.get('followers')
        artist_genres = f'{artist_stats.get("genres").pop(0)}, {artist_stats.get("genres").pop(0)}'
  
        if self.artist_stats_widget1 is not None:
            self.artist_stats_widget1.clear_list()
        else:
            self.artist_stats_widget1 = ListWithItems(self)
            self.artist_stats_widget1.grid(row=2, column=4, padx=(5, 5), pady=(10, 10), columnspan=1, sticky="nw")
        self.artist_stats_widget1.clear_list()
        self.artist_stats_widget1.add_list_item("Nazwa Artysty", artist_name)
        self.artist_stats_widget1.add_list_item("Obserwujący", artist_followers)
        self.artist_stats_widget1.add_list_item("Gatunki", artist_genres)
        self.insert_albums_to_listbox()

        self.show_artist_image_from_url(artist_image_url)


    def insert_albums_to_listbox(self):

        albums = self.sp_analyzer.get_all_albums(self.artist_id)
        self.albums= albums
        albums_names =  set([album['name'] for album in albums])
        self.albums_listbox.delete(0, END)
        for album in albums_names:
            self.albums_listbox.insert(END, album)
  

    def show_albums(self, event):
        try:

            selected_album_index = self.albums_listbox.curselection()[0]
            selected_album_name = self.albums_listbox.get(selected_album_index)
            #print(albums_names)
            selected_album = [album for album in self.albums if album['name'] == selected_album_name][0]
            album_id = selected_album['uri']
            self.album_id = album_id
            #self.print_track_info(track_info)
            #self.sp_analyzer.display_tracks(tracks) 
            self.insert_tracks_to_listbox() 
            album_stats = self.sp_analyzer.get_album_info(album_id)
            album_cover_url = album_stats.get('image_url')
            album_name = album_stats.get('name')
            album_total_tracks = album_stats.get('total_tracks')
            album_release_date = album_stats.get('release_date')




            if self.albums_stats_widget1 is not None:
                self.albums_stats_widget1.clear_list()
            else:
                self.albums_stats_widget1 = ListWithItems(self)
                self.albums_stats_widget1.grid(row=4, column=4,padx=(5,5), pady=(10, 10),columnspan=1,sticky="nw")
            self.albums_stats_widget1.add_list_item("Nazwa Albumu", album_name)
            self.albums_stats_widget1.add_list_item("Liczba Utworów", album_total_tracks)
            self.albums_stats_widget1.add_list_item("Data wydania", album_release_date)

            self.show_album_cover_from_url(album_cover_url)       
        except:
            pass
    
        
    def insert_tracks_to_listbox(self):
        tracks = self.sp_analyzer.get_tracks_from_album(self.album_id)
        tracks_list_length = len(tracks)
        self.tracks_listbox.delete(0, END)
        for track in tracks:
            self.tracks_listbox.insert(END, track['name'])
        print(tracks_list_length)    

    def track_selection(self, event):
        selected_track_index = self.tracks_listbox.curselection()[0]
        selected_track_name = self.tracks_listbox.get(selected_track_index)
        tracks = self.sp_analyzer.get_tracks_from_album(self.selected_album['uri'])
        selected_track = [track for track in tracks if track['name'] == selected_track_name][0]
        self.show_track_info(selected_track)
       

    def show_track_info(self, event):
        try: 
            selected_track_index = self.tracks_listbox.curselection()[0]
            selected_track_name = self.tracks_listbox.get(selected_track_index)
            tracks = self.sp_analyzer.get_tracks_from_album(self.album_id)
            selected_track = [track for track in tracks if track['name'] == selected_track_name][0]
            track_id = selected_track['uri']
            
            track_stats = self.sp_analyzer.get_track_info(track_id)
            track_duration = f'{track_stats.get("duration minutes")} minuty'
            track_danceability = track_stats.get('danceability')
            track_energy = track_stats.get('energy')
            track_loudness = track_stats.get('loudness')
            track_tempo = track_stats.get('tempo')
            track_speechiness = track_stats.get('speechiness')
            track_acousticness = track_stats.get('acousticness')
            track_instrumentalness = track_stats.get('instrumentalness')
            track_liveness = track_stats.get('liveness')
            track_valence = track_stats.get('valence')
            
            if (self.tracks_stats_widget1 and self.tracks_stats_widget2) is not None:
                self.tracks_stats_widget1.clear_list()
                self.tracks_stats_widget2.clear_list()
            else:
                self.tracks_stats_widget1 = ListWithItems(self)
                self.tracks_stats_widget2 = ListWithItems(self)
            self.tracks_stats_widget1.grid(row=8, column=4,padx=(5,5), pady=(10, 10),columnspan=1,sticky="nw")
            self.tracks_stats_widget2.grid(row=8, column=5,padx=(5,5), pady=(10, 10),columnspan=1,sticky="nw")

            self.tracks_stats_widget1.add_list_item("Czas trwania", track_duration)
            self.tracks_stats_widget1.add_list_item("Taneczność", track_danceability)
            self.tracks_stats_widget1.add_list_item("Energia", track_energy)
            self.tracks_stats_widget1.add_list_item("Głośność", track_loudness)
            self.tracks_stats_widget1.add_list_item("Tempo", track_tempo)

            self.tracks_stats_widget2.add_list_item("Mówność", track_speechiness)
            self.tracks_stats_widget2.add_list_item("Aksutyczność", track_acousticness)
            self.tracks_stats_widget2.add_list_item("Instrumentalność", track_instrumentalness)
            self.tracks_stats_widget2.add_list_item("Żywiołowość", track_liveness)
            self.tracks_stats_widget2.add_list_item("Pozytywne nastawienie", track_valence)



        except:
            pass
        

    def show_album_cover_from_url(self, album_cover_url,  width=115, height=115):

        album_cover_data = urlopen(album_cover_url).read()
        album_cover = Image.open(BytesIO(album_cover_data))
        photo = CTkImage(album_cover, size=(width, height))
        self.album_cover_label.configure(image=photo,text = "")

    def show_artist_image_from_url(self, artist_image_url,  width=115, height=115):
        artist_image_url = urlopen(artist_image_url).read()
        album_image = Image.open(BytesIO(artist_image_url))
        photo = CTkImage(album_image, size=(width, height))
        self.artist_image_label.configure(image=photo, text="")

    