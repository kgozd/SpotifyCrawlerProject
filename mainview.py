#my libraries
from page import Page
from page_1 import Page1
from page_2 import Page2
#additional libraries
from tkinter import(
    Frame, Label, Button, Tk, 
    Entry, Listbox, Canvas, END, 
    BooleanVar, Scrollbar, ttk, VERTICAL, 
     EXTENDED, SINGLE, MULTIPLE, Y,LEFT, RIGHT
) 
from customtkinter import(
    CTkScrollbar, CTkTabview, CTkButton, CTkEntry,
    set_appearance_mode,set_default_color_theme, CTkScrollableFrame,
    CTkTextbox, CTkLabel, CTkFont, CTkImage
)  
from io import BytesIO
from PIL import ImageTk, Image, ImageDraw
from urllib.request import urlopen
 


    



class Page3(Page):
    def __init__(self, parent):
        super().__init__(parent, "Page 3")
        self.create_widgets()

    def create_widgets(self):
        canvas = Canvas(self, width=200, height=200)
        canvas.grid(row=4, column=0)
        canvas.create_rectangle(50, 50, 150, 150, fill="blue")
        canvas.create_text(100, 100, text="Canvas Text", font=("Arial", 12), fill="white")


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
        self.sidebar = Frame(self, bg='#2b2b2b', width=150)
        self.sidebar.pack(side='left', fill='y')

        app_title = Label(self.sidebar, text="Spotify Crawler", font=("Arial", 16, 'bold'), fg='#4ddf5d', bg='#2b2b2b')
        app_title.pack(side='top', pady=(20,10), padx=10)

        page_names = ['Page1', 'Page2', 'Page3']
        for name in page_names:
            button = CTkButton(self.sidebar, text=name, height=50, width=150, text_color="#000000", fg_color="#4ddf5d", font=("Arial", 18, 'bold'), command=lambda name=name: self.show_page(name), hover_color="#3bac47")
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


       
