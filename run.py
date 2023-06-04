from os.path import dirname, join, abspath
from tkinter.messagebox import askyesno, showinfo
from sys import exit, version
from importlib.util import find_spec
from subprocess import check_call,run
from os import chdir, remove
from os.path import isfile

class Run:
    def __init__(self):
        self.current_dir = dirname(abspath(__file__))
      
    def check_for_packages(self):
            
        
        # Zmiana katalogu roboczego na obecny katalog
        chdir(self.current_dir)

        python_version = version.split()[0]  # Pobranie wersji Pythona

        # Podział wersji na elementy
        elementy = python_version.split(".")

        # Wybór pierwszych dwóch elementów i połączenie w jedną liczbę
        wersja_pythona = float(".".join(elementy[:2]))

        if wersja_pythona != 3.11:
            answer = askyesno("Ostrzeżenie",f"Twoja obecna wersja Pythona to {python_version},\nzalecana instalacja  wersji 3.11.\nCzy chcesz kontynuować?")
            if answer == False:
                exit()


        packages = (  'customtkinter', 'spotipy', 'matplotlib',  )
        missing_packages = []

        for package in packages:
            spec = find_spec(package)
            if spec is None:
                missing_packages.append(package)

        if missing_packages:
            
            result = askyesno("Instalacja bibliotek Python", "Czy chcesz zainstalować niezbędne brakujące pakiety?\n"+", ".join(missing_packages))

            if result:
                for package in missing_packages:
                    check_call(['pip', 'install', package])
                showinfo("Informacja", "Pakiety zainstalowano pomyślnie!")
            else:
                exit()
        
    def remove_db(self):
            db_path = join(self.current_dir, 'SpotifyCrawler\\scdb.db')
            if isfile(db_path):
                remove(db_path)

if __name__ == "__main__":
    run_app = Run()
    run_app.remove_db()
    run_app.check_for_packages()
    run(["python", "SpotifyCrawler\\mainview.py"])
    exit()