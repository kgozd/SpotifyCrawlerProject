#my libraries
from page import  Labele
from page_1 import Page1
from page_2 import Page2
from page_3 import Page3
#additional libraries
from tkinter import(
    Frame, Label, Tk

) 
from customtkinter import CTkButton, CTkFrame,CTkLabel
from os.path import dirname, join, abspath
from tkinter import Tk

from tkinter import Label, Text
from tkinter.constants import END

from tkinter import Label
from customtkinter import CTkTextbox





class MainView(CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.my_labels = Labele(self)
        self.current_page = None
        self.create_widgets()
        self.show_page("Dane")

    def create_widgets(self):
        self.create_sidebar()
        self.create_page_container()

    def create_sidebar(self):
        self.sidebar = Frame(self, bg='#2b2b2b', width=150)
        self.sidebar.pack(side='left', fill='y')

        app_title = Label(self.sidebar, text="Spotify Crawler", font=("Arial", 16, 'bold'), fg='#4ddf5d', bg='#2b2b2b')
        app_title.pack(side='top', pady=(20,10), padx=10)


        page_names = ['Dane', 'Wykresy', 'O aplikacji']
        for name in page_names:
            button = CTkButton(self.sidebar, text=name, height=50, width=150, text_color="#000000", fg_color="#4ddf5d", font=("Arial", 18, 'bold'), command=lambda name=name: self.show_page(name), hover_color="#3bac47")
            button.pack(side='top', pady=10, padx=10)

    def create_page_container(self):
        self.page_container = Frame(self, bg="#e5e5e5", width=500)
        self.page_container.pack(side='top', fill='both', expand=True)

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        if page_name == "Dane":
            self.current_page = Page1(self.page_container)
        elif page_name == "Wykresy":
            self.current_page = Page2(self.page_container)
        elif page_name == "O aplikacji":
            self.current_page = Page3(self.page_container)
        self.current_page.pack(side='top', fill='both', expand=True)


       

class Application:
    def __init__(self):
        self.current_dir = dirname(__file__)
        self.root = None
    
    def main(self):
        self.root = Tk()
        #current_dir = dirname(abspath(__file__))
        icon_path = join(self.current_dir, 'Pictures\\sc_icon.ico')
        self.root.title('Spotify Crawler')
        self.root.iconbitmap(icon_path)
        self.root.geometry('1300x780')
        # root.state('zoomed')
        main_view = MainView(self.root)
        main_view.pack(fill='both', expand=True)
        
        self.root.mainloop()


if __name__ == "__main__":
    app = Application()
    app.main()