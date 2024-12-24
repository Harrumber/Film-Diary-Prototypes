import tkinter as tk
from tkinter import *
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
import json

diary_entries = []
watchlist_entries = []

def loaddiary():
    global diary_entries
    try:
        with open("Diary Entries.json", "r") as file:
            diary_entries = json.load(file)
    except FileNotFoundError:
        diary_entries = []
        
def savediary():
    with open("Diary Entries.json", "w") as file:
        json.dump(diary_entries, file, indent=4)

def loaddiarylistbox(listbox):
    listbox.delete(0, END)
    for entry in diary_entries:
        listbox.insert(END, f"{entry['date']} - {entry['title']}")

def loadwatchlist():
    global watchlist_entries
    try:
        with open("Watchlist Entries.json", "r") as file:
            watchlist_entries = json.load(file)
    except FileNotFoundError:
        watchlist_entries = []

def savewatchlist():
    with open("Watchlist Entries.json", "w") as file:
        json.dump(watchlist_entries, file, indent=4)

def loadwatchlistlistbox(listbox):
    listbox.delete(0, END)
    for entry in watchlist_entries:
        listbox.insert(END, entry['title'])

loaddiary()
loadwatchlist()

API_KEY = "f8ff48f2b826dda880277d721c81f9ca"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

#Code to create the main window with the heading
home_page=Tk()
home_page.title("Film Diary")
home_page.geometry("900x500")
home_page.resizable(0,0)

home_heading = Label(home_page,text='Film Diary',font=('Rockwell',60,'bold'))
home_heading.place(x=450,y=60,anchor='center')

button_width=15
button_font=('Rockwell',30,'underline')

#Code to create the function that will be used to close the main window and create a "diarystats" sub-window
def opendiarystatspage():
    diarystats_page=Toplevel(home_page)
    diarystats_page.title("Diary + Stats Page")
    diarystats_page.geometry("900x500")
    diarystats_page.resizable(0,0)
    home_page.withdraw()

    diarystats_heading=Label(diarystats_page, text="Diary + Stats",font=('Rockwell',50,'bold'))
    diarystats_heading.grid(row=0,column=1,columnspan = 2)

    def opendiarypage():
        diary_page = Toplevel(home_page)
        diary_page.title("Diary Page")
        diary_page.geometry("900x500")
        diary_page.resizable(0, 0)
        diarystats_page.withdraw()

        diary_heading = Label(diary_page, text="Your Diary", font=('Rockwell', 50, 'bold'))
        diary_heading.pack(pady=10)

        diary_frame = Frame(diary_page, padx=20, pady=10)
        diary_frame.pack(fill='both', expand=True)

        diary_scrollbar = Scrollbar(diary_frame)
        diary_scrollbar.pack(side='right', fill='y', pady=5)

        global diary_listbox
        diary_listbox = Listbox(diary_frame, font=('Rockwell', 20), yscrollcommand=diary_scrollbar.set)
        diary_listbox.pack(side='left', fill='both', expand=True, padx=10, pady=5)
        diary_scrollbar.config(command=diary_listbox.yview)

        loaddiarylistbox(diary_listbox)
        
        def removeentry():
            selected_entry = diary_listbox.curselection()
            if selected_entry:
                index = selected_entry[0]
                deleted_entry = diary_entries.pop(index)
                print(f"Removed from Diary: {deleted_entry['title']} on {deleted_entry['date']}")
                savediary()
                loaddiarylistbox(diary_listbox)

        def openentrydetailspage():
            selected_entry = diary_listbox.curselection()
            if selected_entry:
                index = selected_entry[0]
                movie_entry = diary_entries[index]
                movie_id = movie_entry['id']

                details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
                response = requests.get(details_url)
                movie = response.json()

                entrydetails_page = Toplevel(diary_page)
                entrydetails_page.title(f"{movie['title']} Details")
                entrydetails_page.geometry("900x500")
                entrydetails_page.resizable(0, 0)
                diary_page.withdraw()

                entrytitle_heading = Label(entrydetails_page, text=movie['title'], font=('Rockwell', 40, 'bold'))
                entrytitle_heading.pack(pady=10)

                releaseyear = movie['release_date'] if 'release_date' in movie else "N/A"
                releaseyear_label = Label(entrydetails_page, text=f"Year: {releaseyear[:4]}", font=('Rockwell', 30))
                releaseyear_label.pack(pady=5)

                overview = movie.get('overview', 'No overview available.')
                overview_label = Label(entrydetails_page, text=f"Overview: {overview}", wraplength=800, font=('Rockwell', 20), justify='left')
                overview_label.pack(pady=10)
                
                def closeentrydetailspage():
                    entrydetails_page.withdraw()
                    diary_page.deiconify()

                entrydetailsback_button = Button(entrydetails_page, text="Back", font=('Rockwell', 30), command=closeentrydetailspage)
                entrydetailsback_button.pack()

        def enableentrybuttons(event):
            if diary_listbox.curselection():
                deleteentry_button.config(state='normal')
                openentry_button.config(state='normal')
            else:
                deleteentry_button.config(state='disabled')
                openentry_button.config(state='disabled')
                
        diary_listbox.bind("<<ListboxSelect>>", enableentrybuttons)
        
        deleteentry_button = Button(diary_page, text="Remove Entry", font=('Rockwell', 30), command=removeentry, state='disabled')
        deleteentry_button.pack(pady=20)

        openentry_button = Button(diary_page, text="View Movie Details", font=('Rockwell', 30), command=openentrydetailspage, state='disabled')
        openentry_button.pack()

        def closediarypage():
            diary_page.withdraw()
            diarystats_page.deiconify()

        diaryback_button = Button(diary_page, text="Back", font=('Rockwell', 30), command=closediarypage)
        diaryback_button.place(x=20, y=430)

    diary_button=Button(diarystats_page,text="Diary Page",font=('Rockwell',40,'underline'),command=opendiarypage)
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
diarystats_button=Button(home_page,text="Diary + Stats",font=button_font,width=button_width,height=2,command=opendiarystatspage)
diarystats_button.place(x=200,y=160,anchor='center')

def openwatchlistpage():
    watchlist_page = Toplevel(home_page)
    watchlist_page.title("Watchlist")
    watchlist_page.geometry("900x500")
    home_page.withdraw()

    watchlist_heading = Label(watchlist_page, text="Watchlist", font=('Rockwell', 50, 'bold'))
    watchlist_heading.pack()

    watchlist_frame = Frame(watchlist_page, padx=20, pady=10)
    watchlist_frame.pack(fill='both', expand=True)

    watchlist_scrollbar = Scrollbar(watchlist_frame)
    watchlist_scrollbar.pack(side='right', fill='y', pady=5)

    global watchlist_listbox
    watchlist_listbox = Listbox(watchlist_frame, font=('Rockwell', 20), yscrollcommand=watchlist_scrollbar.set)
    watchlist_listbox.pack(side='left', fill='both', expand=True, padx=10, pady=5)
    watchlist_scrollbar.config(command=watchlist_listbox.yview)

    loadwatchlistlistbox(watchlist_listbox)

    def removefromwatchlist():
        selected_entry = watchlist_listbox.curselection()
        if selected_entry:
            index = selected_entry[0]
            removed_entry = watchlist_entries.pop(index)
            print(f"Removed from Watchlist: {removed_entry['title']}")
            savewatchlist()
            loadwatchlistlistbox(watchlist_listbox)

    def openentrydetailspage():
        selected_entry = watchlist_listbox.curselection()
        if selected_entry:
            index = selected_entry[0]
            movie_entry = watchlist_entries[index]
            movie_id = movie_entry['id']

            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            response = requests.get(details_url)
            movie = response.json()

            entrydetails_page = Toplevel(watchlist_page)
            entrydetails_page.title(f"{movie['title']} Details")
            entrydetails_page.geometry("900x500")
            entrydetails_page.resizable(0, 0)
            watchlist_page.withdraw()

            entrytitle_heading = Label(entrydetails_page, text=movie['title'], font=('Rockwell', 40, 'bold'))
            entrytitle_heading.pack(pady=10)

            releaseyear = movie.get('release_date', "N/A")[:4]
            releaseyear_label = Label(entrydetails_page, text=f"Year: {releaseyear}", font=('Rockwell', 30))
            releaseyear_label.pack(pady=5)

            overview = movie.get('overview', 'No overview available.')
            overview_label = Label(entrydetails_page, text=f"Overview: {overview}", wraplength=800, font=('Rockwell', 20), justify='left')
            overview_label.pack(pady=10)

            def savetodiary():
                watch_date = datetime.now().strftime("%Y-%m-%d")
                diary_entries.append({"title": movie['title'], "date": watch_date, "id": movie['id']})
                savediary()

                if diary_listbox:
                    diary_listbox.insert(END, f"{watch_date} - {movie['title']}")
                    print(f"Added to Diary: {movie['title']} on {watch_date}")

            savetodiary_button = Button(entrydetails_page, text="Save to Diary", font=('Rockwell', 30), command=savetodiary)
            savetodiary_button.pack(pady=10)

            def closeentrydetailspage():
                entrydetails_page.withdraw()
                watchlist_page.deiconify()

            entrydetailsback_button = Button(entrydetails_page, text="Back", font=('Rockwell', 30), command=closeentrydetailspage)
            entrydetailsback_button.pack()

    def enablewatchlistbuttons(event):
        if watchlist_listbox.curselection():
            remove_button.config(state='normal')
            viewdetails_button.config(state='normal')
        else:
            remove_button.config(state='disabled')
            viewdetails_button.config(state='disabled')

    watchlist_listbox.bind("<<ListboxSelect>>", enablewatchlistbuttons)

    remove_button = Button(watchlist_page, text="Remove", font=('Rockwell', 30), command=removefromwatchlist, state='disabled')
    remove_button.pack(pady=10)

    viewdetails_button = Button(watchlist_page, text="View Details", font=('Rockwell', 30), command=openentrydetailspage, state='disabled')
    viewdetails_button.pack(pady=10)

    def closewatchlistpage():
        watchlist_page.withdraw()
        home_page.deiconify()

    watchlistback_button = Button(watchlist_page, text="Back", font=('Rockwell', 30), command=closewatchlistpage)
    watchlistback_button.place(x=20, y=430)

watchlist_button=Button(home_page,text="Watchlist",font=button_font,width=button_width,height=2,command=openwatchlistpage)
watchlist_button.place(x=700,y=160,anchor='center')

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

recommended_button=Button(home_page,text="Recommended",font=button_font,width=button_width,height=2,command=openrecommendedpage)
recommended_button.place(x=200,y=300,anchor='center')

def opensearchpage():
    search_page = Toplevel(home_page)
    search_page.title("Search Page")
    search_page.geometry("900x500")
    search_page.resizable(0,0)
    home_page.withdraw()

    def searchforfilm():
        global poster_photo
        filmsearch_result = filmsearch_input.get()
        filmsearch_heading.configure(text=filmsearch_result)

        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={filmsearch_result}"
        response = requests.get(search_url)
        data = response.json()

        def openmoviedetailspage(movie):
            moviedetails_page = Toplevel(search_page)
            moviedetails_page.title(f"{movie['title']} Details")
            moviedetails_page.geometry("900x500")
            moviedetails_page.resizable(0, 0)
            search_page.withdraw()

            movietitle_heading = Label(moviedetails_page, text=movie['title'], font=('Rockwell', 40, 'bold'))
            movietitle_heading.pack(pady=10)

            releaseyear = movie['release_date'] if 'release_date' in movie else "N/A"
            releaseyear_label = Label(moviedetails_page, text=f"Year: {releaseyear[:4]}", font=('Rockwell', 30))
            releaseyear_label.pack(pady=5)

            overview = movie.get('overview', 'No overview available.')
            overview_label = Label(moviedetails_page, text=f"Overview: {overview}", wraplength=800, font=('Rockwell', 20), justify='left')
            overview_label.pack(pady=10)

            def savetodiary():
                watch_date = datetime.now().strftime("%Y-%m-%d")
                diary_entries.append({"title": movie['title'], "date": watch_date, "id": movie['id']})
                savediary()

                diary_listbox.insert(END, f"{watch_date} - {movie['title']}")
                print(f"Added to Diary: {movie['title']} on {watch_date}")

            savetodiary_button = Button(moviedetails_page, text="Save to Diary", font=('Rockwell', 30), command=savetodiary)
            savetodiary_button.pack(pady=10)

            def savetowatchlist():
                watchlist_entries.append({"title": movie['title'], "id": movie['id']})
                savewatchlist()

                loadwatchlistlistbox(watchlist_listbox)
                print(f"Added to Watchlist: {movie['title']}")

            savetowatchlist_button = Button(moviedetails_page, text="Save to Watchlist", font=('Rockwell', 30), command=savetowatchlist)
            savetowatchlist_button.pack(pady=10)
    
            def closemoviedetailspage():
                moviedetails_page.withdraw()
                search_page.deiconify()

            moviedetailsback_button = Button(moviedetails_page, text="Back", font=('Rockwell', 30), command=closemoviedetailspage)
            moviedetailsback_button.pack()

        if data['results']:
            for i, movie in enumerate(data['results'][:3]):
                poster_path = movie.get('poster_path', None)
                if poster_path:
                    full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    poster_response = requests.get(full_poster_url)
                    poster_image = Image.open(BytesIO(poster_response.content))
                    poster_image = poster_image.resize((150, 200), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)

                    poster_button = Button(search_page,image=poster_photo,command=lambda m=movie: openmoviedetailspage(m))
                    poster_button.image = poster_photo
                    poster_button.place(x=400 + i * 160, y=240)

    search_heading = Label(search_page, text="Search Page", font=('Rockwell', 60, 'bold'))
    search_heading.place(x=450, y=60, anchor='center')

    resultsfor_heading = Label(search_page, text="Results for:", font=('Rockwell', 50, 'bold'))
    resultsfor_heading.place(x=50, y=160)

    filmsearch_heading = Label(search_page, text="", font=('Rockwell', 50, 'bold'))
    filmsearch_heading.place(x=400, y=160, width=500)

    filmsearch_input = Entry(search_page, text="", font=('Rockwell', 30))
    filmsearch_input.focus_set()
    filmsearch_input.place(x=50, y=240, width=300)

    filmsearch_button = Button(search_page, text="Search", font=('Rockwell', 30), command=searchforfilm)
    filmsearch_button.place(x=50, y=310)

    def closesearchpage():
        search_page.withdraw()
        home_page.deiconify()

    searchback_button = Button(search_page, text="Back", font=('Rockwell', 30), command=closesearchpage)
    searchback_button.place(x=20, y=430)

search_button=Button(home_page,text="Search",font=button_font,width=button_width,height=2,command=opensearchpage)
search_button.place(x=700,y=300,anchor='center')

home_page.protocol("WM_DELETE_WINDOW", lambda: [savediary(), home_page.destroy()])
home_page.mainloop()
