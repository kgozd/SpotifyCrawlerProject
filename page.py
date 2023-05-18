from api_requests import  SpotifyAuthenticator, SpotifyAnalyzer
from config import client_id, client_secret

#additional libraries
from tkinter import(
    Frame
) 
from customtkinter import(
    CTkScrollbar, CTkTabview, CTkButton, CTkEntry,
    set_appearance_mode,set_default_color_theme, CTkScrollableFrame,
    CTkTextbox, CTkLabel, CTkFont, CTkImage
)  




class Page(Frame):
    def __init__(self, parent, name):
        super().__init__(parent, bg="#242424")
        self.name = name
        self.sp_authenticator = SpotifyAuthenticator(client_id, client_secret) # Replace client_id and client_secret with your own Spotify API credentials
        self.sp_analyzer = SpotifyAnalyzer(self.sp_authenticator.get_spotify_instance())
        set_appearance_mode("System")
        set_default_color_theme("green")