import tkinter as tk
from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "f8ff48f2b826dda880277d721c81f9ca"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

#Code to create the main window with the heading
home_page=Tk()
home_page.title("Film Diary")
home_page.geometry("900x500")

home_heading=Label(home_page,text='Film Diary',font=('Rockwell',50,'bold'))
home_heading.grid(row=0,column=1)

#Code to create the function that will be used to close the main window and create a "diarystats" sub-window
def opendiarystatspage():
    diarystats_page=Toplevel(home_page)
    diarystats_page.title("Diary + Stats Page")
    diarystats_page.geometry("900x500")
    home_page.withdraw()

    diarystats_heading=Label(diarystats_page, text="Diary + Stats",font=('Rockwell',50,'bold'))
    diarystats_heading.grid(row=0,column=1,columnspan = 2)

    diary_button=Button(diarystats_page,text="Diary Page",font=('Rockwell',40,'underline'))
    diary_button.grid(row=1,column=1,padx=30,pady=50)

    stats_button=Button(diarystats_page,text="Stats Page",font=('Rockwell',40,'underline'))
    stats_button.grid(row=1,column=2,padx=30,pady=50)

    #Code to create a function that closes the sub-window. Command added to a back button
    def closediarystatspage():
        diarystats_page.withdraw()
        home_page.deiconify()

    diarystatsback_button=Button(diarystats_page,text="Back",font=('Rockwell',30),command=closediarystatspage)
    diarystatsback_button.grid(row=2,column=0,padx=20,pady=200)
    
#Code that creates a button that runs the function that runs the previously stated function
diarystats_button=Button(home_page,text="Diary + Stats",font=('Rockwell',40,'underline'),command=opendiarystatspage)
diarystats_button.grid(row=1,column=0)

def openwatchlistpage():
    watchlist_page=Toplevel(home_page)
    watchlist_page.title("Watchlist")
    watchlist_page.geometry("900x500")
    home_page.withdraw()

    watchlist_heading=Label(watchlist_page,text="Watchlist",font=('Rockwell',50,'bold'))
    watchlist_heading.grid(row=0,column=1,columnspan=3)

    temp_poster1=Label(watchlist_page,text="   ",font=('Rockwell',150),bg='red')
    temp_poster1.grid(row=1,column=0,padx=20,pady=20)
    temp_poster2=Label(watchlist_page,text="   ",font=('Rockwell',150),bg='blue')
    temp_poster2.grid(row=1,column=1,padx=20,pady=20)
    temp_poster3=Label(watchlist_page,text="   ",font=('Rockwell',150),bg='green')
    temp_poster3.grid(row=1,column=2,padx=20,pady=20)
    temp_poster4=Label(watchlist_page,text="   ",font=('Rockwell',150),bg='yellow')
    temp_poster4.grid(row=1,column=3,padx=20,pady=20)
    temp_poster5=Label(watchlist_page,text="   ",font=('Rockwell',150),bg='pink')
    temp_poster5.grid(row=1,column=4,padx=20,pady=20)

    def closewatchlistpage():
        watchlist_page.withdraw()
        home_page.deiconify()

    watchlistback_button=Button(watchlist_page,text="Back",font=('Rockwell',30),command=closewatchlistpage)
    watchlistback_button.grid(row=3,column=0,padx=15,pady=150)

watchlist_button=Button(home_page,text="Watchlist",font=('Rockwell',40,'underline'),command=openwatchlistpage)
watchlist_button.grid(row=1,column=2)

def openrecommendedpage():
    recommended_page=Toplevel(home_page)
    recommended_page.title("Recommended")
    recommended_page.geometry("900x500")
    home_page.withdraw()

    recommended_heading=Label(recommended_page,text="Recommended",font=('Rockwell',50,'bold'))
    recommended_heading.grid(row=0,column=1,columnspan=3)

    temp_poster8=Label(recommended_page,text="   ",font=('Rockwell',150),bg='red')
    temp_poster8.grid(row=1,column=0,padx=20,pady=20)
    temp_poster9=Label(recommended_page,text="   ",font=('Rockwell',150),bg='blue')
    temp_poster9.grid(row=1,column=1,padx=20,pady=20)
    temp_poster10=Label(recommended_page,text="   ",font=('Rockwell',150),bg='green')
    temp_poster10.grid(row=1,column=2,padx=20,pady=20)
    temp_poster11=Label(recommended_page,text="   ",font=('Rockwell',150),bg='yellow')
    temp_poster11.grid(row=1,column=3,padx=20,pady=20)
    temp_poster12=Label(recommended_page,text="   ",font=('Rockwell',150),bg='pink')
    temp_poster12.grid(row=1,column=4,padx=20,pady=20)
    
    def closerecommendedpage():
        recommended_page.withdraw()
        home_page.deiconify()

    recommendedback_button=Button(recommended_page,text="Back",font=('Rockwell',30),command=closerecommendedpage)
    recommendedback_button.grid(row=3,column=0,padx=15,pady=150)

recommended_button=Button(home_page,text="Recommended",font=('Rockwell',40,'underline'),command=openrecommendedpage)
recommended_button.grid(row=2,column=0)

def opensearchpage():
    search_page=Toplevel(home_page)
    search_page.title("Search Page")
    search_page.geometry("900x500")
    home_page.withdraw()

    def searchforfilm():
        global poster_photo
        filmsearch_result=filmsearch_input.get()
        filmsearch_heading.configure(text=filmsearch_result)

        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={filmsearch_result}"
        response = requests.get(search_url)
        data = response.json()

        if data['results']:
            movie = data['results'][0]
            poster_path = movie['poster_path']
            full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"

            poster_response = requests.get(full_poster_url)
            poster_image = Image.open(BytesIO(poster_response.content))
            poster_image = poster_image.resize((150, 200), Image.LANCZOS)
            poster_photo = ImageTk.PhotoImage(poster_image)
            poster_display.config(image=poster_photo)     

    resultsfor_heading=Label(search_page,text="Results for:",font=('Rockwell',50,'bold'))
    resultsfor_heading.grid(row=0,column=1)
    
    filmsearch_heading=Label(search_page,text="",font=('Rockwell',50,'bold'))
    filmsearch_heading.grid(row=0,column=2,columnspan=2)

    poster_display = Label(search_page)
    poster_display.grid(row=1,column=2)

    filmsearch_input=Entry(search_page,text="",font=('Rockwell',30))
    filmsearch_input.focus_set()
    filmsearch_input.grid(row=1,column=1)
                
    filmsearch_button=Button(search_page,text="Search",font=('Rockwell',30),command=searchforfilm)
    filmsearch_button.grid(row=2,column=1)

    def closesearchpage():
        search_page.withdraw()
        home_page.deiconify()

    searchback_button=Button(search_page,text="Back",font=('Rockwell',30),command=closesearchpage)
    searchback_button.grid(row=3,column=0,padx=20,pady=150)

search_button=Button(home_page,text="Search",font=('Rockwell',40,'underline'),command=opensearchpage)
search_button.grid(row=2,column=2)

home_page.mainloop()
