#my libraries
from page import Page

#additional libraries
from tkinter import(
    Frame, Label, Button, Tk, 
    Entry, Listbox, Canvas, END, 
    BooleanVar, Scrollbar, ttk,filedialog, VERTICAL, 
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

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


class Wykres:
    def __init__(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

    def rysuj(self):
        self.ax.bar(['A', 'B', 'C'], [1, 2, 3], color="#4ddf5d")

        self.ax.set_title('Wykres słupkowy')
        self.ax.set_xlabel('Kategorie')
        self.ax.set_ylabel('Wartości')

        self.ax.grid(True)

        self.fig.tight_layout()

    def zapisz_do_pliku(self):
        default_extension = ".png"
        default_filename = f"wykres_{datetime.now().strftime('%d.%m.%Y-%H.%M')}"

        nazwa_pliku = filedialog.asksaveasfilename(defaultextension=default_extension,
                                                  initialfile=default_filename,
                                                  filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
        if nazwa_pliku:
            self.fig.savefig(nazwa_pliku)
            print(f"Wykres zapisany jako {nazwa_pliku}")
class Page2(Page):
    def __init__(self, parent):
        super().__init__(parent,"Page 2")
        self.parent = parent

        self.nasz_wykres = Wykres()
        self.create_widgets()

    def create_widgets(self):
        self.nasz_wykres.rysuj()

        canvas = FigureCanvasTkAgg(self.nasz_wykres.fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        button_zapisz = CTkButton(self, text="Zapisz wykres",fg_color="#4ddf5d",text_color="#000000",                          command=self.nasz_wykres.zapisz_do_pliku)
        button_zapisz.grid(row=1, column=0, padx=10, pady=10)



