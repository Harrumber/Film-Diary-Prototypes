import tkinter as tk
from tkinter import *

main_window = tk.Tk()
main_window.title("Film Diary")
main_window.geometry("900x500")

heading = tk.Label(main_window,text='Film Diary', font=('Rockwell', 50, 'bold'))
heading.grid(row = 0, column = 1)

def opendiarystatspage():
    diarystats_page = Toplevel(main_window)
    diarystats_page.title("Diary + Stats Page")
    diarystats_page.geometry("900x500")
    main_window.withdraw()

diary_button = Button(main_window, text = "Diary + Stats", font=('Rockwell', 40, 'underline'), command = opendiarystatspage)
diary_button.grid(row = 1, column = 0)

def openwatchlistpage():
    watchlist_page = Toplevel(main_window)
    watchlist_page.title("Watchlist")
    watchlist_page.geometry("900x500")
    main_window.withdraw()

watchlist_button = Button(main_window, text = "Watchlist", font=('Rockwell', 40, 'underline'), command = openwatchlistpage)
watchlist_button.grid(row = 1, column = 2)

def openrecommendedpage():
    recommended_page = Toplevel(main_window)
    recommended_page.title("Recommended")
    recommended_page.geometry("900x500")
    main_window.withdraw()

recommended_button = Button(main_window, text = "Recommended", font=('Rockwell', 40, 'underline'), command = openrecommendedpage)
recommended_button.grid(row = 2, column = 0)

def opensearchpage():
    search_page = Toplevel(main_window)
    search_page.title("Search Page")
    search_page.geometry("900x500")
    main_window.withdraw()

search_button = Button(main_window, text = "Search", font=('Rockwell', 40, 'underline'), command = opensearchpage)
search_button.grid(row = 2, column = 2)

main_window.mainloop()
