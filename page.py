#my libraries
from api_requests import  SpotifyAuthenticator, SpotifyRequester
from config import client_id, client_secret
from cachetools import cached, LRUCache

#additional libraries
from tkinter import(
    Frame, ttk, Label,Toplevel,Button
) 
from customtkinter import( 
    CTkScrollbar, CTkTabview, CTkButton, CTkEntry,
    set_appearance_mode,set_default_color_theme, CTkScrollableFrame,
    CTkTextbox, CTkLabel, CTkFont, CTkImage,CTkFrame 
)  


from PIL import Image, ImageTk
from os.path import dirname, join, abspath

class CustomMessage:
    def __init__(self, root):
        self.root = root
        self.my_labels = Labele(self)

    def show_custom_error_message(self,current_dir, title,  message, icon):
        dialog = Toplevel()
        dialog.title(title)
        dialog.configure(bg="#2b2b2b")
        dialog.geometry("340x120")
        path = join(current_dir, 'Pictures\\sc_icon.ico')
        dialog.iconbitmap(path)
        #current_dir = dirname(abspath(__file__))
        # Słownik mapujący nazwy ikon na odpowiadające im ścieżki obrazów
        image_paths = {
            "error_icon": join(current_dir, 'Pictures\\error_icon.png'),
            "warning_icon": join(current_dir, 'Pictures\\warning_icon.png'),
            "info_icon": join(current_dir, 'Pictures\\info_icon.png'),
            "save_icon": join(current_dir, 'Pictures\\save_icon.png')
        }

        # Sprawdzenie, czy nazwa ikony istnieje w słowniku
        if icon in image_paths:
            image_path = image_paths[icon]
        else:
            # Domyślna ścieżka obrazu w przypadku braku dopasowania
            image_path = join(current_dir, 'Pictures\\info_icon.png')

        # Załadowanie obrazka
        image = Image.open(image_path)

        # Zmiana rozmiaru obrazka
        desired_size = (30, 30)  # Nowy rozmiar obrazka
        resized_image = image.resize(desired_size)

        # Konwersja obrazka do obiektu ImageTk
        error_image = ImageTk.PhotoImage(resized_image)

        error_label = Label(dialog, image=error_image, bg="#2b2b2b")
        error_label.grid(row=0, column=0, padx=(15, 10), pady=(30, 5))
        

        message_label = Label(dialog, text=message,font=("Arial", 9, "bold"), bg="#2b2b2b", fg="#f0f0f0", padx=10, pady=10)
        message_label.grid(row=0, column=1, padx=(0, 20), pady=(30, 5), sticky="w")

       


        ok_button = CTkButton(dialog, text="OK",font=("Arial", 12,'bold'), height=20, width =40,fg_color="#4ddf5d",
                                           text_color="#000000", command=dialog.destroy,  hover_color="#3bac47")
        ok_button.grid(row=1, column=1, pady=(10, 10), padx=(0,20), columnspan=2, sticky="nse")
 
        dialog.columnconfigure(0, weight=0)
        dialog.columnconfigure(1, weight=1)
        dialog.rowconfigure(0, weight=1)

        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)






class ListItem(CTkFrame):
    def __init__(self, parent, header, text):
        super().__init__(parent, bg_color='#242424')

        header_label = Label(self, text=header, foreground='white', background='#2b2b2b', font=('Arial', 12, 'bold'))
        header_label.grid(row=0, column=0, padx=10,pady=10)

        bullet_label = Label(self, text='\u2022', foreground='#4ddf5d', background='#2b2b2b', font=('Arial', 12, 'bold'))
        bullet_label.grid(row=0, column=1,padx=10,pady=10)

        text_label = Label(self, text=text, foreground='white',font=('Arial', 11,'bold'), background='#2b2b2b')
        text_label.grid(row=0, column=2,padx=10,pady=10)


class ListWithItems(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, bg_color='#242424')
        self.parent = parent
        self.grid(row=3, column=3)
        self.list_items = []
        # Ramka listy
        self.list_frame = None
        self.list_frame = CTkFrame(self, bg_color='#242424', corner_radius=50)
        self.list_frame.grid(row=0, column=0)

    def add_list_item(self, header, text):
        item = ListItem(self.list_frame, header, text)
        item.grid(sticky='new')
        self.list_items.append(item)

    def clear_list(self):
        for item in self.list_items:
            item.destroy()
        self.list_items = []


"""
class Buttons:
    def __init__(self, parent):
        self.parent = parent

    def create_button(self, text,command, font_size=18, font_weight="bold", row=0, 
                      column=3, padx=(20, 0), pady=(15, 5), columnspan=1, height=40, width = "", sticky=""  ):
        
        button = CTkButton(self, text=text,font=("Arial", font_size, font_weight), height=height, width=width,fg_color="#4ddf5d",
                                           text_color="#000000", command=command,  hover_color="#3bac47",)
        
        button.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, sticky=sticky)
        return button
"""


"""
class AlbumsListBox:
    def __init__(self, parent):
        self.parent = parent
        self.albums_listbox = None
        self.scrollbar = None

    def create_listbox(self, font_size=12, width=40, height=15, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43", highlightbackground="#4ddf5d", highlightcolor="#4ddf5d", activestyle='none', justify=tk.LEFT, selectmode=tk.SINGLE, relief="flat", borderwidth=3, row=2, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew", rowspan=3):
        self.albums_listbox = tk.Listbox(self.parent, font=("Arial", font_size), width=width, height=height, bg=bg, fg=fg, cursor=cursor, selectbackground=selectbackground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, activestyle=activestyle, justify=justify, selectmode=selectmode, relief=relief, borderwidth=borderwidth)
        self.albums_listbox.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, rowspan=rowspan)
        self.albums_listbox.grid_columnconfigure(0, weight=1)

    def create_scrollbar(self, bg="#2b2b2b", width=20):
        scrollbar_frame = tk.Frame(self.parent)
        scrollbar_frame.grid(row=2, column=2, padx=(0, 0), pady=(0, 0), sticky="ns", rowspan=4)
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor=bg, background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=width)
        scrollbar_albums = ttk.Scrollbar(scrollbar_frame, orient=tk.VERTICAL, command=self.albums_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_albums.pack(fill=tk.Y, side=tk.LEFT)
        self.albums_listbox.configure(yscrollcommand=scrollbar_albums.set)
        self.scrollbar = scrollbar_albums
"""
class Page(Frame):
    def __init__(self, parent, name):
        super().__init__(parent, bg="#242424")
        self.name = name
        self.sp_authenticator = SpotifyAuthenticator(client_id, client_secret) # Replace client_id and client_secret with your own Spotify API credentials
        self.sp_requester = SpotifyRequester(self.sp_authenticator.get_spotify_instance())
        self.current_dir = dirname(__file__)
        set_appearance_mode("system")
        set_default_color_theme("green")




class Labele:
    def __init__(self, parent):
        self.parent = parent

    def create_label(self, text, font_size=20, font_weight="bold", text_color="#f0f0f0",
                     row=0, column=0, padx=(0, 0), pady=(0, 0), columnspan=1, sticky=""):
        label = CTkLabel(self.parent, text=text, font=("Arial", font_size, font_weight), text_color=text_color)
        label.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, sticky=sticky)
        return label
