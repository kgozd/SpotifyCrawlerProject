#my libraries
from page import Page, Labele, CustomMessage
from sql_handling import Database
#additional libraries
from tkinter import(
    Frame,Listbox, END, 
    ttk,filedialog, VERTICAL, 
    SINGLE, Y,LEFT, RIGHT, StringVar
) 
from customtkinter import(
    CTkButton,CTkOptionMenu
)  

from os.path import  join
from sqlite3 import OperationalError,connect
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


class Wykres:
    def __init__(self):
        self.fig = Figure(figsize=(5, 4), dpi=110)
        self.ax = self.fig.add_subplot(111)

    def rysuj(self, plot_title, categories_title, values_title, bars_titles, bars_values  ):
        slupki = self.ax.bar( bars_titles,bars_values, color="#4ddf5d", zorder=2, width=0.5,align='center')
        self.fig.set_facecolor("#242424")
        self.ax.set_facecolor("#2b2b2b")
        self.ax.set_title(f'Wykres {plot_title}', color='white')
        self.ax.set_xlabel(f'{categories_title}', color='white')
        self.ax.set_ylabel(f'{values_title}', color='white')

        self.ax.grid(True, color='black')
        self.ax.autoscale()

        
        self.ax.bar_label(
            slupki,label_type='edge', color='white', zorder=2
        )
  
        self.ax.tick_params(axis='x', colors='white')  
        self.ax.tick_params(axis='y', colors='white') 
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
        self.db_path = join(self.current_dir, 'scdb.db')
        self.PopUpBox = CustomMessage(self)

        self.my_labels = Labele(self)
        self.plot1 = Wykres()
        self.db = Database()
        
        self.create_widgets()

    def create_widgets(self):
        
        self.db.connect(self.db_path)
        query = self.db.retrieve_records("SPotify", "album_name", "available_markets", "brak_wartości")
        self.db.close()

        self.title= self.my_labels.create_label(f"Wykresy dla albumu: {query}",   row=0, column=1, padx=(20, 20), pady=(5, 5), columnspan = 5)



        self.tracks_listbox = Listbox(self, font=("Arial", 12), width=40, height=15, bg="#2b2b2b", fg="white", cursor="hand2", selectbackground="#106a43",highlightbackground="#4ddf5d",
                                      highlightcolor="#4ddf5d", activestyle='none', justify=LEFT, selectmode=SINGLE,relief="flat", borderwidth=3)
        self.tracks_listbox.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")
        self.tracks_listbox.grid_columnconfigure(0, weight=1)

        scrollbar_frame = Frame(self)
        scrollbar_frame.grid(row=1, column=2, padx=(0, 0), pady=(0, 0), sticky="wns")
        scrollbar_style = ttk.Style()
        scrollbar_style.configure("Custom.Vertical.TScrollbar", troughcolor="#2b2b2b", background="#106a43", gripcount=0, gripmargin=0, gripstyle="n", width=20)
        scrollbar_tracks = ttk.Scrollbar(scrollbar_frame, orient=VERTICAL, command=self.tracks_listbox.yview, style="Custom.Vertical.TScrollbar")
        scrollbar_tracks.pack(fill=Y, side=RIGHT)
        self.tracks_listbox.configure(yscrollcommand=scrollbar_tracks.set)
        self.tracks_listbox.bind("<<ListboxSelect>>", self.track_selection)


        self.value_dict = {
            "Wybierz dane":"dane",
            "Czas trwania": "duration_mins",
            "Taneczność": "danceability",
            "Energia": "energy",
            "Głośność": "loudness",
            "Mówność": "speechiness",
            "Akustyczność": "acousticness",
            "Żywiołowość": "liveness",
            "Walencja": "valence",
            "Tempo": "tempo"
        }
        self.selected_key = StringVar(value=list(self.value_dict.keys())[0])
        self.selected_value = StringVar(value=self.value_dict[self.selected_key.get()])

        self.optionmenu = CTkOptionMenu(self, dynamic_resizing=True,
                                        values=list(self.value_dict.keys()), variable=self.selected_key,
                                        command=self.handle_optionmenu_selection, font=("Arial", 17,'bold'), height=40,fg_color="#4ddf5d",
                                           text_color="#000000" ,  text_color_disabled= "#111111",dropdown_font=("Arial", 14,'bold'),dropdown_text_color="white",button_color="#4ddf5d",button_hover_color="#3bac47",dropdown_fg_color="#2b2b2b")
        self.optionmenu.grid(row=0, column=0, padx=20, pady=(20, 10))

        canvas = FigureCanvasTkAgg(self.plot1.fig, master=self)
        canvas.get_tk_widget().grid(row=1, column=3, padx=10, pady=10)
        canvas.draw()
        self.plot1.rysuj("", "Oś X", "Oś Y",[ "Średnia albumu","Wybrany utwór"], [0,0])
        self.insert_tracks_to_listbox()

    def insert_tracks_to_listbox(self):
        self.conn = connect(self.db_path)
        query = f"SELECT name FROM SPotify"
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            self.tracks_listbox.insert(END, row[0])
    
    def track_selection(self, event):
        try:
            self.conn = connect(self.db_path)
            self.selected_track_index = self.tracks_listbox.curselection()[0]
            self.selected_track_name = self.tracks_listbox.get(self.selected_track_index)
            self.set_plot_values()
            self.conn.close()
        except IndexError:
            pass
    def handle_optionmenu_selection(self, selected_key):
        self.selected_value.set(self.value_dict[selected_key])
        
        canvas = FigureCanvasTkAgg(self.plot1.fig, master=self)
        canvas.get_tk_widget().grid(row=1, column=3, padx=10, pady=10)
        canvas.draw()
        
        button_zapisz = CTkButton(self, text="Zapisz wykres",fg_color="#4ddf5d", 
                                  command=self.plot1.zapisz_do_pliku, font=("Arial", 15,'bold'), height=30,
                                           text_color="#000000",  hover_color="#3bac47")
        button_zapisz.grid(row=2, column=3, padx=10, pady=10)
        try:
            self.set_plot_values()
        except AttributeError:
            self.PopUpBox.show_custom_error_message(self.current_dir,"Błąd","Najpierw wybierz utwór!","warning_icon" )


    def set_plot_values(self):
        try:
            self.plot1.ax.clear()
            self.db.connect(self.db_path)
            
            query_1 = self.db.retrieve_records("SPotify", self.selected_value.get(), "name", self.selected_track_name)
            query_2 = self.db.retrieve_records("av_SPotify", self.selected_value.get(), "track_uri", 0)
            
            percent= abs(((float(query_1) - float(query_2))/float(query_2))*100)
            percent = "{:.2f}".format(percent)
            if self.title is not None:
                self.title.destroy()
            if float(query_1) < float(query_2):
                
                self.title= self.my_labels.create_label(f" {self.selected_key.get()} w tym utworze jest o {percent}% mniejsza niż średnia dla albumu",
                                                        row=5, column=2, padx=(20, 20), pady=(5, 5), columnspan = 5) 
            else:
                self.title= self.my_labels.create_label(f"{self.selected_key.get()} w tym utworze jest o {percent}% większa niż średnia dla albumu",
                                                                                     row=5, column=2, padx=(20, 20), pady=(5, 5), columnspan = 5)                                                                                                                                             



            self.plot1.rysuj(
            f"{self.selected_key.get()} dla utworu {self.selected_track_name}",
            "",
            "",
            ["Średnia albumu", "Wybrany utwór"],
            [round(float(query_2), 2), round(float(query_1), 2)]
            )

            

            canvas = FigureCanvasTkAgg(self.plot1.fig, master=self)
            canvas.get_tk_widget().grid(row=1, column=3, padx=10, pady=10)
            canvas.draw()
        except OperationalError:
            pass
        try:
            key = self.selected_key.get()
            utwor = self.selected_track_name
            if len(utwor)> 15:
                three_dots = "..."

            self.plot1.rysuj(f"{key} dla utworu {utwor[0:15]}{three_dots}", "", "",[ "Średnia albumu","Wybrany utwór"], [round(float(query_2),2),round(float(query_1),2)])
            
        except UnboundLocalError:
            pass
        self.db.close()    

        