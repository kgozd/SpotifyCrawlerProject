from os.path import dirname, join, abspath
from time import sleep
from mainview import Tk, MainView

#from json import dumps
class Application:
    def main(self):
         
        root = Tk()
        current_dir = dirname(abspath(__file__))
        path = join(current_dir, 'Pictures\\sc_icon.ico')
        root.title('Spotify Crawler')
        root.iconbitmap(path)
        #root.geometry('1920x1080')
        root.state('zoomed')
        main_view = MainView(root)
        main_view.pack(fill='both', expand=True)

        root.mainloop()


if __name__=="__main__":
    app = Application()
    app.main()      

 