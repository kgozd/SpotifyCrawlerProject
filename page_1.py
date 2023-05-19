#my libraries
from page import Page

#additional libraries
from tkinter import(
    Frame, Label, Button, Tk, 
    Entry, Listbox, Canvas, END, 
    BooleanVar, Scrollbar, ttk, VERTICAL, 
     SINGLE, Y,LEFT, RIGHT
) 
from customtkinter import(
    CTkScrollbar, CTkTabview, CTkButton, CTkEntry,
    set_appearance_mode,set_default_color_theme, CTkScrollableFrame,
    CTkTextbox, CTkLabel, CTkFont, CTkImage 
)  
from io import BytesIO
from PIL import ImageTk, Image, ImageDraw
from urllib.request import urlopen
from functools import partial










class Page1(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 1")
        self.parent = parent
        self.create_widgets()
       
    def create_widgets(self):
       
        self.artist_entry = CTkEntry(self,font=("Arial", 18), height=40,  placeholder_text="Wpisz Nazwę Artysty")
        self.artist_entry.grid(row=0, column=1,  padx=(20, 0), pady=(10, 10),  sticky="nsew")
        self.artist_entry.grid_columnconfigure(0, weight=1)  # configure grid of individual tabs


        self.button_to_request = CTkButton(self, text="Pobierz infromacje o artyście ",font=("Arial", 18), height=40, fg_color="#4ddf5d",text_color="#000000", command=self.enter_artist_name,  hover_color="#3bac47" )
        self.button_to_request.grid(row=0, column=3, padx=(20, 0), pady=(10, 10), sticky="nsew")
        self.button_to_request.grid_columnconfigure(0, weight=1) 

        
        self.artist_info_label = CTkLabel(self, text="Informacje o Artyście", font=CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.artist_info_label.grid(row=1, column=3, padx=(40,20), pady=(20, 10), columnspan=2, sticky="nsew")

        
        self.artist_image_label = CTkLabel(self, text="", font=CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.artist_image_label.grid(row=2, column=3, padx=(40,20), pady=(20, 10), columnspan=2, sticky="new")


        self.album_info_label = CTkLabel(self, text="Informacje o Albumie", font=CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.album_info_label.grid(row=1, column=4, padx=(120,20), pady=(20, 10), columnspan=2, sticky="nsew")


        self.album_cover_label = CTkLabel(self, text="", font=CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.album_cover_label.grid(row=2, column=4, padx=(120,20), pady=(20, 10), columnspan=2, sticky="new")


        self.albums_listbox_label = CTkLabel(self, text="Albumy", font=CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.albums_listbox_label.grid(row=1, column=1, padx=20, pady=(20, 10))
        self.albums_listbox = Listbox(self, font=("Arial", 12), width=40, height=15, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d", highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.albums_listbox.grid(row=2, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.albums_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self)
        scrollbar_frame.grid(row=2, column=2, padx=(0, 0), pady=(10, 0), sticky="ns")
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_albums = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.albums_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_albums.pack(fill=Y, side=LEFT)
        self.albums_listbox.configure(yscrollcommand=scrollbar_albums.set)


        self.tracks_listbox_label = CTkLabel(self, text="Utwory", font=CTkFont(size=20, weight="bold"), text_color="#f0f0f0")
        self.tracks_listbox_label.grid(row=3, column=1, padx=20, pady=(20, 10))
        self.tracks_listbox = Listbox(self, font=("Arial", 12), width=40, height=15, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d", highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.tracks_listbox.grid(row=4, column=1, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.tracks_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self)
        scrollbar_frame.grid(row=4, column=2, padx=(0, 0), pady=(10, 0), sticky="ns")
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_tracks = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.tracks_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_tracks.pack(fill=Y, side=RIGHT)
        self.tracks_listbox.configure(yscrollcommand=scrollbar_tracks.set)



        self.button_clicked = BooleanVar()
        self.button_clicked.set(False)
        self.albums_listbox.bind("<<ListboxSelect>>", self.show_albums)
        self.tracks_listbox.bind("<<ListboxSelect>>", self.show_track_info)
    
        """
        self.tabview = CTkTabview(self,height=200, width=200,text_color="white", command= self.show_track_info)
        self.tabview.grid(row=3, column=3, rowspan = 1,padx=(200, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Lista Utworów")
        self.tabview.tab("Lista Utworów").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        """

        """
        self.textbox_label = CTkLabel(self, text="Utwory", font=CTkFont(size=20, weight="bold"), text_color="#2b2b2b")
        self.textbox_label.grid(row=3, column=1, padx=20, pady=(20, 10))
      
        self.textbox = CTkTextbox(self, width=300 ,text_color="white",corner_radius = 10, font=("Arial", 15))
        self.textbox.grid(row=4, column=1,rowspan = 2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        
       
        scrollbar_tracks = Scrollbar(self, orient=VERTICAL, command=self.tarcks_listbox.yview,troughcolor="#2b2b2b",width=20 )
        scrollbar_tracks.grid(row=1, column=2,pady=(2, 2),rowspan = 2, sticky="ns")
        self.tracks_listbox.configure(yscrollcommand=scrollbar_tracks.set)
        """
   
    def enter_artist_name(self):
        artist_name = self.artist_entry.get()
        artist_id = self.sp_analyzer.get_artist_id(artist_name)
        self.artist_id = artist_id
        self.button_clicked.set(True)
        artist_stats= self.sp_analyzer.get_artist_info(artist_id)
        artist_image_url = artist_stats['image_url']
        _artist_followers = artist_stats['followers']
        _artist_genres = artist_stats['genres']
        self.insert_albums_to_listbox()
        self.show_artist_image_from_url(artist_image_url)


    def insert_albums_to_listbox(self):
        albums = self.sp_analyzer.get_all_albums(self.artist_id)
        self.albums= albums
        albums_names =  set([album['name'] for album in albums])
        self.albums_listbox.delete(0, END)
        for album in albums_names:
            self.albums_listbox.insert(END, album)
        #self.album_selection(albums_names)
  
        
    #def album_selection(self, albums_names):
     #   selected_album = self.albums_listbox.curselection()
        #if selected_album:
            #album_name = list(albums_names)[selected_album[0]]
            #album = [album for album in albums_names if album['name'] == album_name][0]
            #return album


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
            album_cover_url = album_stats['image_url']
            self.show_album_cover_from_url(album_cover_url)       
        except:
            pass
    
        
    def insert_tracks_to_listbox(self):
        tracks = self.sp_analyzer.get_tracks_from_album(self.album_id)
        self.tracks_listbox.delete(0, END)
        for track in tracks:
            self.tracks_listbox.insert(END, track['name'])
        

    
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
            print(track_stats)
            """
            self.textbox.delete('1.0', END)
            for  i in track_stats:
                #time_in_minutes = round(track['duration_ms']/60000,2)
                
                self.textbox.insert(END, f" {i} ")
            """
        except:
            pass
        

    def show_album_cover_from_url(self, album_cover_url,  width=150, height=150):
        album_cover_data = urlopen(album_cover_url).read()
        album_cover = Image.open(BytesIO(album_cover_data))
        photo = CTkImage(album_cover, size=(width, height))
        self.album_cover_label.configure(image=photo)

    def show_artist_image_from_url(self, artist_image_url,  width=150, height=150):
        artist_image_url = urlopen(artist_image_url).read()
        album_image = Image.open(BytesIO(artist_image_url))
        photo = CTkImage(album_image, size=(width, height))
        self.artist_image_label.configure(image=photo)

    