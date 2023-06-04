#my libraries
from page import Page, Labele,ListWithItems, CustomMessage
from sql_handling import Database
#additional libraries
from tkinter import(
    Frame, Entry, Listbox,  END, 
    BooleanVar,  ttk, VERTICAL, 
     SINGLE, Y,LEFT, RIGHT
) 
from customtkinter import(
     CTkButton, CTkEntry,
     CTkLabel,  CTkImage,CTkFrame
)  
 
from io import BytesIO
from PIL import  Image
from urllib.request import urlopen
from os.path import  join, dirname
from spotipy.exceptions import SpotifyException
from threading import Thread
from time import sleep




class Page1(Page):
  
    def __init__(self, parent):
        super().__init__(parent, "Page 1")
        self.parent = parent
        self.my_labels1 = Labele(self)
        
        self.PopUpBox = CustomMessage(self)
        self.db = Database()
        self.current_dir = dirname(__file__)

        self.db_path = join(self.current_dir, 'scdb.db')
        self.artist_stats_widget1 = None
        self.artist_stats_widget2 = None
        self.albums_stats_widget1 = None
        self.tracks_stats_widget1 = None
        self.create_widgets()
        
        

        
    def create_widgets(self):            
        self.listboxes_frame = CTkFrame(self, bg_color='#242424',fg_color="#242424", corner_radius=5, height = 20)
        self.listboxes_frame.grid(row=0, column=1, rowspan=8, padx=(100, 20), pady=(10,0),sticky="wsne")

        self.artist_entry = CTkEntry(self.listboxes_frame,font=("Arial", 18), height=40,  placeholder_text="Wpisz Nazwę Artysty", fg_color="#2b2b2b", placeholder_text_color="#f0f0f0", text_color="white")
        self.artist_entry.grid(row=0, column=1,  padx=(25, 0), pady=(15, 5),  sticky="nsew")
        self.artist_entry.grid_columnconfigure(0, weight=1)  

        self.buttons_frame = CTkFrame(self, bg_color='#242424',fg_color="#242424", corner_radius=5, height = 20)
        self.buttons_frame.grid(row=0, column=3, columnspan=2, padx=(70, 20), pady=(15,0), sticky="wsne")


        self.button_to_request = CTkButton(self.buttons_frame, text="Pobierz dane ",font=("Arial", 18,'bold'), height=40, width =20 ,fg_color="#4ddf5d",
                                           text_color="#000000", command=self.enter_artist_name,  hover_color="#3bac47")
        self.button_to_request.grid(row=0, column=3, padx=(20, 0), pady=(10, 5), sticky="nswe", columnspan=1)
        self.button_to_request.grid_columnconfigure(0, weight=1) 

        

        self.button_to_save_to_db = CTkButton(self.buttons_frame, text="Zapisz do bazy",font=("Arial", 18,'bold'), height=40, width =20, fg_color="#4ddf5d",
                                           text_color="#000000", command=self.run_in_thread_create_db,  hover_color="#3bac47", text_color_disabled= "#111111")
        self.button_to_save_to_db.grid(row=0, column=4, padx=(20, 0), pady=(10, 5),sticky="nesw", columnspan=1)
        self.button_to_save_to_db.grid_columnconfigure(0, weight=1)
       

        self.progress = ttk.Progressbar(self.buttons_frame, mode='determinate')

      

        self.artist_info_label = self.my_labels1.create_label("Informacje o Artyście",   row=1, column=3, padx=(40, 20), pady=(5, 10), columnspan=3, sticky="new")
        self.artist_image_label = self.my_labels1.create_label("",   row=2, column=3, padx=(40, 20), pady=(5, 10), sticky="nw")
        self.album_info_label = self.my_labels1.create_label("Informacje o Albumie",   row=3, column=3, padx=(40, 20), pady=(5, 10), columnspan=3, sticky="new")
        self.album_cover_label = self.my_labels1.create_label("",   row=4, column=3, padx=(40, 20), pady=(5, 10), columnspan=1, sticky="nw")
        self.tracks_info_label = self.my_labels1.create_label("Informacje o Utworze",   row=5, column=3, padx=(40, 20), pady=(5, 5), columnspan=3, sticky="nsew")
       
        self.db_saving_label= self.my_labels1.create_label("",   row=4, column=8, padx=(20, 20), pady=(5, 5))


       
        self.track_stats_frame = CTkFrame(self, bg_color='#242424',fg_color="#242424", corner_radius=5)
        self.track_stats_frame.grid(row=6, column=3, columnspan=3, padx=(20, 20))


        self.albums_listbox_label = CTkLabel(self.listboxes_frame,text= "Albumy", font=("Arial", 20, 'bold'),  text_color="#f0f0f0"     )
        self.albums_listbox_label.grid(row=1, column=1, padx=(0, 0), pady=(5, 5), columnspan=1,sticky="nsew")        
        

        
        self.albums_listbox = Listbox(self.listboxes_frame, font=("Arial", 13), width=40, height=8, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d",
                                      highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.albums_listbox.grid(row=3, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew",rowspan=1)
        self.albums_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self.listboxes_frame)
        scrollbar_frame.grid(row=3, column=2, padx=(0, 0), pady=(0, 0), sticky="ns",rowspan=1)
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_albums = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.albums_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_albums.pack(fill=Y, side=LEFT)
        self.albums_listbox.configure(yscrollcommand=scrollbar_albums.set)

        self.tracks_listbox_label = CTkLabel(self.listboxes_frame,text= "Utwory", font=("Arial", 20, 'bold'),  text_color="#f0f0f0"     )
        self.tracks_listbox_label.grid(row=4, column=1, padx=(5, 5), pady=(10, 5), columnspan=1,sticky="nsew")  
        

        self.tracks_listbox = Listbox(self.listboxes_frame, font=("Arial", 13), width=40, height=20, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d",
                                      highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.tracks_listbox.grid(row=8, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew")
        self.tracks_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self.listboxes_frame)
        scrollbar_frame.grid(row=8, column=2, padx=(0, 0), pady=(0, 0), sticky="ns")
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_tracks = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.tracks_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_tracks.pack(fill=Y, side=RIGHT)
        self.tracks_listbox.configure(yscrollcommand=scrollbar_tracks.set)

        

        self.button_clicked = BooleanVar()
        self.button_clicked.set(False)
        self.press_enter = Entry(self)  
        self.press_enter.bind_all("<Return>", self.enter_artist_name)
        self.albums_listbox.bind("<<ListboxSelect>>", self.show_albums)
        self.tracks_listbox.bind("<<ListboxSelect>>", self.show_track_info)
        
   
   
    def enter_artist_name(self, *args):
        try: 
            artist_name = self.artist_entry.get()       

            artist_id = self.sp_requester.get_artist_id(artist_name)
            self.artist_id = artist_id
            self.button_clicked.set(True)
            artist_stats= self.sp_requester.get_artist_info(artist_id)
            artist_name = artist_stats.get('name')
            artist_image_url = artist_stats.get('image_url')
            artist_followers = artist_stats.get('followers')
            try:
                artist_genres = f'{artist_stats.get("genres").pop(0)}, {artist_stats.get("genres").pop(0)}'
            except IndexError:
                try:
                    artist_genres = f'{artist_stats.get("genres").pop(0)}'
                except IndexError:
                    artist_genres = "Brak danych"

            if self.artist_stats_widget1 is not None:
                self.artist_stats_widget1.clear_list()
            else:
                self.artist_stats_widget1 = ListWithItems(self)
                self.artist_stats_widget1.grid(row=2, column=4, padx=(5, 5), pady=(5, 5), columnspan=1, sticky="nw")
            self.artist_stats_widget1.clear_list()
            self.artist_stats_widget1.add_list_item("Nazwa Artysty", artist_name)
            self.artist_stats_widget1.add_list_item("Obserwujący", artist_followers)
            try:
                self.artist_stats_widget1.add_list_item("Gatunki", artist_genres)
            except UnboundLocalError:
                pass
            self.insert_albums_to_listbox()

            self.show_artist_image_from_url(artist_image_url)
        except SpotifyException:
            self.PopUpBox.show_custom_error_message(self.current_dir,"Błąd","Najpierw wprowadź nazwę artysty!","error_icon" )

    def insert_albums_to_listbox(self):

        albums = self.sp_requester.get_all_albums(self.artist_id)
        self.albums= albums
        albums_names =  set([album['name'] for album in albums])
        self.albums_listbox.delete(0, END)
        for album in albums_names:
            self.albums_listbox.insert(END, album)

       
    def show_albums(self, event):
        try:

            selected_album_index = self.albums_listbox.curselection()[0]
            selected_album_name = self.albums_listbox.get(selected_album_index)
            selected_album = [album for album in self.albums if album['name'] == selected_album_name][0]
            album_id = selected_album['uri']
            self.album_id = album_id

            self.insert_tracks_to_listbox() 
            album_stats = self.sp_requester.get_album_info(album_id)
            album_cover_url = album_stats.get('image_url')
            album_name = album_stats.get('name')
            self.album_total_tracks = album_stats.get('total_tracks')
            album_release_date = album_stats.get('release_date')

            if self.albums_stats_widget1 is not None:
                self.albums_stats_widget1.clear_list()
            else:
                self.albums_stats_widget1 = ListWithItems(self)
                self.albums_stats_widget1.grid(row=4, column=4,padx=(5,5), pady=(5, 5),columnspan=1,sticky="nw")
            self.albums_stats_widget1.add_list_item("Nazwa Albumu", album_name)
            self.albums_stats_widget1.add_list_item("Liczba Utworów", self.album_total_tracks)
            self.albums_stats_widget1.add_list_item("Data wydania", album_release_date)

            self.show_album_cover_from_url(album_cover_url)  
     
        except:
            pass
    
        
    def insert_tracks_to_listbox(self):
        self.albums_tracks_info = self.sp_requester.get_tracks_from_album(self.album_id)
        self.tracks_listbox.delete(0, END)
        for track in self.albums_tracks_info:
            self.tracks_listbox.insert(END, track['name'])

        
    def run_in_thread_create_db(self):
        Thread(target=self.creating_db).start()

    def start_saving(self):
        self.button_to_save_to_db.configure(state="disabled")  
        
        self.progress.grid(row=0, column=5, columnspan=1, padx=10, pady=10)  


        self.button_to_save_to_db.configure(text="Trwa zapisywanie...")   

        for i in range(101):
            self.progress['value'] = i 
            self.update()  
            sleep(0.05)


        self.progress.grid_remove() 



        self.after(1000)
    
       
        self.button_to_save_to_db.configure(text="Zapisz do bazy",state="normal")  
        self.PopUpBox.show_custom_error_message(self.current_dir,"Komunikat","Informacje o albumie zapisane","save_icon" )

    def creating_db(self):
        try:
            first_track_uri = self.albums_tracks_info[0]['uri']
        
            first_track_stats = self.sp_requester.get_track_info(first_track_uri)
        
            self.db.connect(self.db_path)
            table_name = "SPotify"
            self.db.create_table(first_track_stats,table_name )
            Thread(target=self.start_saving).start()

            for track in self.albums_tracks_info:
                track_stats = self.sp_requester.get_track_info(track['uri'])
                self.db.add_records(track_stats ) 

            self.db.create_avarages_table()


        except AttributeError:
            self.PopUpBox.show_custom_error_message(self.current_dir,"Błąd","Wybierz album przed pobraniem danych","error_icon" )


    def show_track_info(self, event):
        try: 
            selected_track_index = self.tracks_listbox.curselection()[0]
            selected_track_name = self.tracks_listbox.get(selected_track_index)
            tracks = self.sp_requester.get_tracks_from_album(self.album_id)
            selected_track = [track for track in tracks if track['name'] == selected_track_name][0]
            track_id = selected_track['uri']
            track_stats = self.sp_requester.get_track_info(track_id)
            track_duration = f'{track_stats.get("duration_mins")} minuty'
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
                self.tracks_stats_widget1 = ListWithItems(self.track_stats_frame)
                self.tracks_stats_widget2 = ListWithItems(self.track_stats_frame)
            self.tracks_stats_widget1.grid(row=8, column=4,padx=(20,15), pady=(10, 10),columnspan=1,sticky="nw")
            self.tracks_stats_widget2.grid(row=8, column=5,padx=(5,5), pady=(10, 10),columnspan=1,sticky="nw")

            self.tracks_stats_widget1.add_list_item("Czas trwania", track_duration)
            self.tracks_stats_widget1.add_list_item("Taneczność", track_danceability)
            self.tracks_stats_widget1.add_list_item("Energia", track_energy)
            self.tracks_stats_widget1.add_list_item("Głośność", track_loudness)
            self.tracks_stats_widget1.add_list_item("Tempo", track_tempo)

            self.tracks_stats_widget2.add_list_item("Mówność", track_speechiness)
            self.tracks_stats_widget2.add_list_item("Akustyczność", track_acousticness)
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

    