
#my libraries
from page import Page, Labele
#additional libraries
from customtkinter import CTkLabel

from customtkinter import CTkTextbox

class Page3(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 3")
        self.create_widgets()

    def create_widgets(self):


        empty_label = CTkLabel(self, text="", font=("Arial", 10))
        empty_label.pack(pady=50)
        title_label = CTkLabel(self, text="Informacje o aplikacji", font=("Arial", 24, 'bold'))
        title_label.pack(pady=10)
        self.textbox = CTkTextbox(self, width=420, height=300, font=("Arial", 20),fg_color="#2b2b2b", padx= 10, pady= 10)
        self.textbox.pack(pady=20)
        kropka = "\u2022"
        
        self.textbox.insert("0.0", f"{kropka} Nazwa: Spotify Crawler\n")
        self.textbox.insert("end", f"{kropka} Wersja: 1.0.1\n")
        self.textbox.insert("end", f"{kropka} Autor: Krystian Góźdź\n")
        self.textbox.insert("end", f"{kropka} Data utworzenia: 01-06-2023\n")
        self.textbox.insert("end", f"{kropka} Opis:\nTa aplikacja służy do pobierania informacji o artystach, albumach i utworach ze Spotify, aby wydobyć te dane komunikauje się z API tego serwisu a następnie przetwarza i prezentuje je z pomocą tabeli oraz wykresów.")
       
        self.textbox.configure(state="disabled")