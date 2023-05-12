from tkinter import Frame, Label, Button, Tk, Entry, Listbox, Canvas, END, BooleanVar, Scrollbar, ttk, VERTICAL
from api_requests import  SpotifyAuthenticator, SpotifyAnalyzer
from config import client_id, client_secret
from customtkinter import CTkScrollbar, CTkTabview, CTkButton, CTkEntry, set_appearance_mode,set_default_color_theme, CTkScrollableFrame, CTkTextbox, CTkLabel, CTkFont



class Page(Frame):
    def __init__(self, parent, name):
        super().__init__(parent, bg="#e5e5e5")
        self.name = name
        self.sp_authenticator = SpotifyAuthenticator(client_id, client_secret) # Replace client_id and client_secret with your own Spotify API credentials
        self.sp_analyzer = SpotifyAnalyzer(self.sp_authenticator.get_spotify_instance())

class Page1(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 1")
        self.parent = parent
        self.create_widgets()
        
       
    def create_widgets(self):
        set_appearance_mode("System")
        set_default_color_theme("green")
        
        self.entry = CTkEntry(self,font=("Arial", 15),  placeholder_text="Wpisz Nazwę Albumu")
        self.entry.grid(row=0, column=0,  padx=(20, 0), pady=(20, 10), sticky="nsew")
        self.entry.grid_columnconfigure(0, weight=1)  # configure grid of individual tabs

        #self.entry = Entry(self, font=("Arial", 12))
        #self.entry.grid(row=2, column=2, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.button_1 = CTkButton(self, text="Pobierz listę albumów ",font=("Arial", 15),  command=self.print_entry_text)
        self.button_1.grid(row=1, column=0, padx=(20, 0), pady=(10, 10), sticky="nsew")
        self.button_1.grid_columnconfigure(0, weight=1) 
        #button = Button(self, text="Pobierz listę albumów ", font=("Arial", 12), command=self.print_entry_text)
        #button.grid(row=3, column=2, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        

        


        self.albums_listbox = Listbox(self, font=("Arial", 12), width=25, height=15, bg="#2b2b2b", fg="white", cursor="hand2",selectbackground="#106a43",highlightcolor="#106a43", activestyle='none')
        self.albums_listbox.grid(row=2, column=0, padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.albums_listbox.grid_columnconfigure(0, weight=1) 
        
       

      
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.albums_listbox.yview,troughcolor="#2b2b2b",width=12 )
        scrollbar.grid(row=2, column=1,pady=(2, 2), sticky="ns")
        self.albums_listbox.configure(yscrollcommand=scrollbar.set)

        # Configure the grid rows and columns to expand as needed
    
        """
        self.tabview = CTkTabview(self,height=200, width=200,text_color="white", command= self.print_all_tracks)
        self.tabview.grid(row=0, column=2, rowspan = 3,padx=(20, 0), pady=(10, 0), sticky="nsew")
        self.tabview.add("Lista Utworów")
        self.tabview.tab("Lista Utworów").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        """
        

        self.logo_label = CTkLabel(self, text="Utwory", font=CTkFont(size=20, weight="bold"), text_color="#2b2b2b")
        self.logo_label.grid(row=0, column=2, padx=20, pady=(20, 10))

        self.textbox = CTkTextbox(self, width=200 ,text_color="white",corner_radius = 10, font=("Arial", 12))
        self.textbox.grid(row=1, column=2,rowspan = 2, padx=(20, 0), pady=(10, 0), sticky="nsew")
        # Set row and column weights
       






        #self.albums_listbox = Listbox(self, font=("Arial", 12), width=50, height=15)      
        #self.albums_listbox.pack(pady=10, padx=10)

        self.button_clicked = BooleanVar()
        self.button_clicked.set(False)
        self.albums_listbox.bind("<<ListboxSelect>>", self.show_tracks)

    def print_entry_text(self):
        entry_text = self.entry.get()
        artist_id = self.sp_analyzer.get_artist_id(entry_text)
        self.button_clicked.set(True)
        albums = self.show_all_albums(artist_id)
        self.remove_duplicates(albums)

    def show_all_albums(self, artist_id):
        albums = self.sp_analyzer.get_all_albums(artist_id)
        return set([album['name'] for album in albums])

    def remove_duplicates(self, albums):
        self.print_all_albums(albums)
        self.pokaz_liste_albumow(albums)

    def print_all_albums(self, albums):
        self.albums_listbox.delete(0, END)
        for album in albums:
            self.albums_listbox.insert(END, album)

    def pokaz_liste_albumow(self, albums):
        selection = self.albums_listbox.curselection()
        if selection:
            album_name = list(albums)[selection[0]]
            album = [album for album in self.sp_analyzer.get_all_albums(self.sp_analyzer.get_artist_id(self.entry.get())) if album['name'] == album_name][0]
            self.get_tracks_from_album(album['uri'])


    def show_tracks(self,even):
        selected_album_index = self.albums_listbox.curselection()[0]
        selected_album_name = self.albums_listbox.get(selected_album_index)
        artist_id = self.sp_analyzer.get_artist_id(self.entry.get())
        albums = self.sp_analyzer.get_all_albums(artist_id)
        selected_album = [album for album in albums if album['name'] == selected_album_name][0]
        tracks = self.sp_analyzer.get_tracks_from_album(selected_album['uri'])
        #self.print_track_info(track_info)
        self.sp_analyzer.display_tracks(tracks ) 
        self.print_all_tracks(tracks) 
        return tracks
        


    def print_all_tracks(self, tracks):
        self.textbox.delete('1.0', END)

        for track in tracks:
            
            self.textbox.insert(END, track["name"] + "\n") # wstaw tekst do panelu pierwszej zakładki

           

    
    """
        def print_all_tracks(self, tracks):
        utwory = self.sp_analyzer.display_tracks( tracks)
        print(utwory)
  






    
    def print_all_tracks(self, track_info):
        self.albums_listbox.delete(0, END)
        for track in track_info:
            self.albums_listbox.insert(END, track['name'])
    
    def get_tracks_from_album(self, album_uri):
        track_info = self.sp_analyzer.get_tracks_from_album(album_uri)
        self.albums_listbox.delete(0, END)
        for track in track_info:
            self.albums_listbox.insert(END, track['name'])
    
    


    def print_track_info(self, track_info):
        print(track_info)
    """


    

class Page2(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 2")
        self.create_widgets()

    def create_widgets(self):
        #label = Label(self, text="This is Page 2", font=("Arial", 12), background="#e5e5e5")
        #label.grid(row=0, column=0)

        self.listbox = Listbox(self, font=("Arial", 12))
        for i in range(10):
            self.listbox.insert(END, "Item %d" % i)
        self.listbox.grid(row=4, column=2)
        self.listbox.bind('<Configure>', self.on_select)

    def on_select(self, event):
        self.listbox.configure(height=self.listbox.size())


class Page3(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 3")
        self.create_widgets()

    def create_widgets(self):
        label = Label(self, text="This is Page 3", font=("Arial", 12), background="#e5e5e5")
        label.grid(row=4, column=0)

        canvas = Canvas(self, width=200, height=200)
        canvas.grid(row=4, column=0)
        canvas.create_rectangle(50, 50, 150, 150, fill="blue")
        canvas.create_text(100, 100, text="Canvas Text", font=("Arial", 12), fill="white")

        button = Button(self, text="Button 3", font=("Arial", 12))
        button.grid(row=4, column=0)


class MainView(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_page = None
        self.create_widgets()
        self.show_page("Page1")

    def create_widgets(self):
        self.create_sidebar()
        self.create_page_container()

    def create_sidebar(self):
        self.sidebar = Frame(self, bg='#222831', width=200)
        self.sidebar.pack(side='left', fill='y')

        page_names = ['Page1', 'Page2', 'Page3']
        for name in page_names:
            button = Button(self.sidebar, text=name, height=2, width= 15, font=("Arial", 12), command=lambda name=name: self.show_page(name))
            button.pack(side='top', pady=10, padx=10)

    def create_page_container(self):
        self.page_container = Frame(self, bg="#e5e5e5", width=500)
        self.page_container.pack(side='top', fill='both', expand=True)

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        if page_name == "Page1":
            self.current_page = Page1(self.page_container)
        elif page_name == "Page2":
            self.current_page = Page2(self.page_container)
        elif page_name == "Page3":
            self.current_page = Page3(self.page_container)
        self.current_page.pack(side='top', fill='both', expand=True)

       
