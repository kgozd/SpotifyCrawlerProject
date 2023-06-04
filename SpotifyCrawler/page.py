#my libraries
from api_requests import  SpotifyAuthenticator, SpotifyRequester
from config import client_id, client_secret

#additional libraries
from tkinter import(
    Frame, Label,Toplevel
) 
from customtkinter import( 
     CTkButton, set_appearance_mode,
     set_default_color_theme, CTkLabel,CTkFrame 
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

        image_paths = {
            "error_icon": join(current_dir, 'Pictures\\error_icon.png'),
            "warning_icon": join(current_dir, 'Pictures\\warning_icon.png'),
            "info_icon": join(current_dir, 'Pictures\\info_icon.png'),
            "save_icon": join(current_dir, 'Pictures\\save_icon.png')
        }

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
 
        dialog.transient(self.root)
        dialog.grab_set()

        # Wycentrowanie okna dialogowego na ekranie
        dialog.update_idletasks()
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        x = (screen_width // 2) - (dialog_width // 2)
        y = (screen_height // 3) - (dialog_height // 2)
        dialog.geometry(f"+{x}+{y}")

        dialog.update()  # Odświeżenie interfejsu

        self.root.wait_window(dialog)



class Labele:
    def __init__(self, parent):
        self.parent = parent

    def create_label(self, text, font_size=20, font_weight="bold", text_color="#f0f0f0",
                     row=0, column=0, padx=(0, 0), pady=(0, 0), columnspan=1, sticky="", fg_color = "#242424"):
        label = CTkLabel(self.parent, text=text, font=("Arial", font_size, font_weight), text_color=text_color,fg_color= fg_color)
        label.grid(row=row, column=column, padx=padx, pady=pady, columnspan=columnspan, sticky=sticky)
        return label


class ListItem(CTkFrame):
    def __init__(self, parent, header, text):
        super().__init__(parent, bg_color='#242424')
        self.my_labels1 = Labele(self)


        header_label = self.my_labels1.create_label(text=header,   row=0, column=0   ,font_size=13   , padx=(5, 10), pady=(10, 11), columnspan=1, sticky="",fg_color = "#2b2b2b")
        bullet_label = self.my_labels1.create_label(text='\u2022',   row=0, column=1  ,font_size=14,text_color="#4ddf5d"    , padx=(10, 10), pady=(10, 10), columnspan=1, sticky="",fg_color = "#2b2b2b")
        text_label = self.my_labels1.create_label(text=text,   row=0, column=2  ,font_size=13     , padx=(10, 10), pady=(11, 10), columnspan=1, sticky="",fg_color = "#2b2b2b")

        


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



class Page(Frame):
    def __init__(self, parent, name):
        super().__init__(parent, bg="#242424")
        self.name = name
        self.sp_authenticator = SpotifyAuthenticator(client_id, client_secret)
        self.sp_requester = SpotifyRequester(self.sp_authenticator.get_spotify_instance())
     
        set_appearance_mode("system")
        set_default_color_theme("green")





