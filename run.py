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
        root.geometry('1160x780')
        #root.state('zoomed')
        main_view = MainView(root)
        main_view.pack(fill='both', expand=True)

        root.mainloop()


if __name__=="__main__":
    app = Application()
    app.main()      



#wykorzystanie cache do zapamiętywania
# import tkinter as tk
# from functools import wraps
# from cachetools import cached, LRUCache

# class MyClass:
#     cache = LRUCache(maxsize=100)  # Zmienna klasowa - pamięć podręczna

#     def __init__(self):
#         pass

#     @classmethod
#     @cached(cache)  # Dekorator cached z użyciem zmiennej klasowej jako pamięci podręcznej
#     def get_data(cls, key):
#         return "Dane dla klucza {}: {}".format(key, cls.cache.get(key))

#     @classmethod
#     def save_data(cls, key, data):
#         cls.cache[key] = data  # Zapis danych do pamięci podręcznej

# if __name__ == "__main__":
#     instance1 = MyClass()
#     instance2 = MyClass()

#     instance1.save_data("klucz", "Przykładowe dane")

#     data1 = instance1.get_data("klucz")
#     data2 = instance2.get_data("klucz")

#     print(data1)  # Wyświetli "Dane dla klucza klucz: Przykładowe dane"
#     print(data2)  # Wyświetli "Dane dla klucza klucz: Przykładowe dane"
