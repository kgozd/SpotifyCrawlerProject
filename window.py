from tkinter import Frame, Label, Button, Tk

class Page(Frame):
    def __init__(self, parent, name):
        Frame.__init__(self, parent)
        self.name = name
        label = Label(self, text="This is " + self.name + " page", font=("Arial", 12))
        label.pack(pady=10, padx=10)

class MainView(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="white")
        
        # create sidebar
        self.sidebar = Frame(self, bg='#222831', width=150)
        self.sidebar.pack(side='left', fill='y')
        
        # create page container
        self.page_container = Frame(self, bg='#EEEEEE')
        self.page_container.pack(side='right', fill='both', expand=True)
        self.pages = {}
        
        # create pages
        page_names = ['Page 1', 'Page 2', 'Page 3']
        for name in page_names:
            page = Page(self.page_container, name)
            self.pages[name] = page
        
        # set current page to the first page
        self.current_page = self.pages[page_names[0]]
        self.current_page.pack(fill='both', expand=True, padx=20, pady=20)
        
        # create buttons in the sidebar to switch between pages
        for name, page in self.pages.items():
            button = Button(self.sidebar, text=name, font=("Arial", 12), fg='#EEEEEE', bg='#393E46', activebackground='#222831', activeforeground='#EEEEEE', 
                               borderwidth=0, highlightthickness=0, padx=20, pady=10, command=lambda name=name: self.switch_page(name))
            button.pack(fill='x', pady=5, padx=10)
    
    def switch_page(self, name):
        self.current_page.pack_forget()
        self.current_page = self.pages[name]
        self.current_page.pack(fill='both', expand=True, padx=20, pady=20)


