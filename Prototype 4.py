import tkinter as tk
from tkinter import *
import requests
#pip install requests
from PIL import Image, ImageTk
#pip install pillow
from io import BytesIO
from datetime import datetime
import json

#Code to define these variables that will be used throughout the program to save time
diary_entries = []
watchlist_entries = []
API_KEY = "f8ff48f2b826dda880277d721c81f9ca"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

#Function that are used to update the users diary/ watchlist with entries when application is launched
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
        listbox.insert(END, f"{entry['date']} - {entry['title']} - {entry['rating']}")

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

    #Code to create the function that will be used to open the Diary Page from the "diarystats" sub-window
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

        #Function that creates and opens a page that shows the details of the entry clicked on by the user
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

                entrytitle_heading = Label(entrydetails_page, text=movie.get('title', 'Title not available'), font=('Rockwell', 40, 'bold'))
                entrytitle_heading.place(x=240, y=20)

                poster_path = movie.get('poster_path', None)
                if poster_path:
                    full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    poster_response = requests.get(full_poster_url)
                    poster_image = Image.open(BytesIO(poster_response.content))
                    poster_image = poster_image.resize((200, 300), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)

                    poster_label = Label(entrydetails_page, image=poster_photo)
                    poster_label.image = poster_photo
                    poster_label.place(x=20, y=20)

                releaseyear = movie.get('release_date', "Release date not available")
                releaseyear_label = Label(entrydetails_page, text=f"Year: {releaseyear[:4] if releaseyear != 'Release date not available' else releaseyear}", font=('Rockwell', 30))
                releaseyear_label.place(x=240, y=70)
    
                runtime = movie.get('runtime', 'Runtime not available')
                if isinstance(runtime, int):
                    hours, minutes = divmod(runtime, 60)
                    runtime_str = f"{hours}h {minutes}m"
                else:
                    runtime_str = runtime
                runtime_label = Label(entrydetails_page, text=f"Runtime: {runtime_str}", font=('Rockwell', 30))
                runtime_label.place(x=240, y=110)

                overview = movie.get('overview', 'Overview not available.')
                overview_label = Label(entrydetails_page, text=f"Overview: {overview}", wraplength=640, font=('Rockwell', 20), justify='left')
                overview_label.place(x=240, y=150)

                credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={API_KEY}"
                credits_response = requests.get(credits_url)
                credits_details = credits_response.json()

                cast = credits_details.get('cast', [])
                if cast:
                    top_cast = cast[:10]
                    cast_names = ", ".join(member.get('name', 'Unknown') for member in top_cast)
                else:
                    cast_names = "Cast not available."
                cast_label = Label(entrydetails_page, text=f"Cast: {cast_names}", wraplength=640, font=('Rockwell', 20), justify='left')
                cast_label.place(x=240, y=230)

                director = next((member.get('name', 'Unknown') for member in credits_details.get('crew', []) if member.get('job') == 'Director'), "Director not available")
                director_label = Label(entrydetails_page, text=f"Director: {director}", font=('Rockwell', 30))
                director_label.place(x=550, y=25)

                deleteentry_button = Button(entrydetails_page, text="Remove From Diary", font=('Rockwell', 30), command=lambda: [removeentry(), closeentrydetailspage()])
                deleteentry_button.place(x=20, y=330)

                def closeentrydetailspage():
                    entrydetails_page.withdraw()
                    diary_page.deiconify()

                entrydetailsback_button = Button(entrydetails_page, text="Back", font=('Rockwell', 30), command=closeentrydetailspage)
                entrydetailsback_button.place(x=20, y=430)

        #Function that highlights the buttons that allow the user to open or remove a movie, when a diary entry is clicked on by the user
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

    #Code to create the function that will be used to open the Stats Page and display the calculated statistics
    def openstatspage():
        stats_page = Toplevel(home_page)
        stats_page.title("Stats Page")
        stats_page.geometry("900x500")
        stats_page.resizable(0, 0)
        diarystats_page.withdraw()

        stats_heading = Label(stats_page, text="Your Stats", font=('Rockwell', 50, 'bold'))
        stats_heading.pack(pady=10)

        totalentries_stat = len(diary_entries)
        totalruntime_stat = 0
        highestratedfilm_stat = None
        highestrating_stat = 0
        totalratings_stat = []
        actor_count = {}
        director_count = {}
 
        #Code to create the function that calculates some of the statistics that get displayed on the stats page
        for entry in diary_entries:
            movie_id = entry['id']
            movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
            response = requests.get(movie_url).json()

            runtime = response.get("runtime", 0) or 0
            totalruntime_stat += runtime

            rating = entry.get("rating", 0)
            totalratings_stat.append(rating)
            if rating > highestrating_stat:
                highestrating_stat = rating
                highestratedfilm_stat = entry["title"]

            credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
            credits_response = requests.get(credits_url).json()

            for cast_member in credits_response.get("cast", []):
                actor = cast_member["name"]
                actor_count[actor] = actor_count.get(actor, 0) + 1

            for crew_member in credits_response.get("crew", []):
                if crew_member["job"] == "Director":
                    director = crew_member["name"]
                    director_count[director] = director_count.get(director, 0) + 1

        totalentries_label = Label(stats_page, text=(f"Total Entries: {totalentries_stat}"), font=('Rockwell', 20))
        totalentries_label.pack()

        highestratedfilm_label = Label(stats_page, text=(f"Highest Rated Film: {highestratedfilm_stat} ({highestrating_stat} stars)"), font=('Rockwell', 20))
        highestratedfilm_label.pack()

        averagerating_stat = sum(totalratings_stat) / len(totalratings_stat) if totalratings_stat else 0
        averagerating_label = Label(stats_page, text=(f"Average Rating: {averagerating_stat:.1f} stars"), font=('Rockwell', 20))
        averagerating_label.pack()

        highestactor_stat = max(actor_count, key=actor_count.get, default="N/A")
        highestactor_count = actor_count.get(highestactor_stat, 0)
        highestactor_label = Label(stats_page, text=(f"Most Watched Actor: {highestactor_stat} ({highestactor_count} movies)"), font=('Rockwell', 20))
        highestactor_label.pack()

        highestdirector_stat = max(director_count, key=director_count.get, default="N/A")
        highestdirector_count = director_count.get(highestdirector_stat, 0)
        highestdirector_label = Label(stats_page, text=(f"Most Watched Director: {highestdirector_stat} ({highestdirector_count} movies)"), font=('Rockwell', 20))
        highestdirector_label.pack()

        totalhours_stat, totalminutes_stat = divmod(totalruntime_stat, 60)
        totalruntime_label = Label(stats_page, text=(f"Total Runtime: {totalhours_stat}h {totalminutes_stat}m"), font=('Rockwell', 20))
        totalruntime_label.pack()

        def closestatspage():
            stats_page.withdraw()
            diarystats_page.deiconify()

        statsback_button = Button(stats_page, text="Back", font=('Rockwell', 30), command=closestatspage)
        statsback_button.pack(pady=10)

    diary_button=Button(diarystats_page,text="Diary Page",font=('Rockwell',40,'underline'),command=opendiarypage)
    diary_button.grid(row=1,column=1,padx=30,pady=50)

    stats_button=Button(diarystats_page,text="Stats Page",font=('Rockwell',40,'underline'),command=openstatspage)
    stats_button.grid(row=1,column=2,padx=30,pady=50)

    #Code to create a function that closes the sub-window. Command added to a back button
    def closediarystatspage():
        diarystats_page.withdraw()
        home_page.deiconify()

    diarystatsback_button=Button(diarystats_page,text="Back",font=('Rockwell',30),command=closediarystatspage)
    diarystatsback_button.grid(row=2,column=0,padx=20,pady=200)
    
#Code that creates a button that runs the function that runs the original function to open the diarystatspage
diarystats_button=Button(home_page,text="Diary + Stats",font=button_font,width=button_width,height=2,command=opendiarystatspage)
diarystats_button.place(x=200,y=160,anchor='center')

#Function that creates and opens the watchlist with the users movie's that they want to watch
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

    #Function that allows the user to see the details for the movie they saved to their watchlist with functionality to add it to the diary
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
            entrytitle_heading.place(x=240, y=20)

            poster_path = movie.get('poster_path', None)
            if poster_path:
                full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                poster_response = requests.get(full_poster_url)
                poster_image = Image.open(BytesIO(poster_response.content))
                poster_image = poster_image.resize((200, 300), Image.LANCZOS)
                poster_photo = ImageTk.PhotoImage(poster_image)

                poster_label = Label(entrydetails_page, image=poster_photo)
                poster_label.image = poster_photo
                poster_label.place(x=20, y=20)

            releaseyear = movie.get('release_date', "N/A")
            releaseyear_label = Label(entrydetails_page, text=f"Year: {releaseyear[:4]}", font=('Rockwell', 30))
            releaseyear_label.place(x=240, y=70)

            runtime = movie.get('runtime', 'N/A')
            hours, minutes = divmod(runtime, 60) if runtime != 'N/A' else (0, 0)
            runtime_str = f"{hours}h {minutes}m" if runtime != 'N/A' else "N/A"
            runtime_label = Label(entrydetails_page, text=f"Runtime: {runtime_str}", font=('Rockwell', 30))
            runtime_label.place(x=240, y=110)

            overview = movie.get('overview', 'No overview available.')
            overview_label = Label(entrydetails_page, text=f"Overview: {overview}", wraplength=640, font=('Rockwell', 20), justify='left')
            overview_label.place(x=240, y=150)

            credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={API_KEY}"
            credits_response = requests.get(credits_url)
            credits_details = credits_response.json()

            cast = credits_details.get('cast', [])
            top_cast = cast[:10]
            cast_names = ", ".join(member['name'] for member in top_cast)
            cast_label = Label(entrydetails_page, text=f"Cast: {cast_names}", wraplength=640, font=('Rockwell', 20), justify='left')
            cast_label.place(x=240, y=240)

            director = next((member['name'] for member in credits_details.get('crew', []) if member['job'] == 'Director'), "N/A")
            director_label = Label(entrydetails_page, text=f"Director: {director}", font=('Rockwell', 30))
            director_label.place(x=550, y=25)

            rating_label = Label(entrydetails_page, text="Rating:", font=('Rockwell', 20))
            rating_label.place(x=20, y=330)
            rating_var = StringVar(value="Pick rating")
            rating_options = [str(i / 2) for i in range(1, 11)]
            rating_dropdown = OptionMenu(entrydetails_page, rating_var, *rating_options)
            rating_dropdown.config(font=('Rockwell', 20))
            rating_dropdown.place(x=100, y=330)
    
            def savetodiary():
                rating = rating_var.get()
                if rating == "Select a rating":
                    print("Please select a rating before saving.")
                    return
                watch_date = datetime.now().strftime("%Y-%m-%d")
                diary_entries.append({"title": movie['title'], "date": watch_date, "id": movie['id'], "rating": float(rating)})
                savediary()
                print(f"Added to Diary: {movie['title']} on {watch_date} with rating {rating} stars")

                watchlist_entries.pop(index)
                savewatchlist()
                watchlist_listbox.delete(index)
                closeentrydetailspage()
    
            savetodiary_button = Button(entrydetails_page, text="Save to Diary", font=('Rockwell', 30), command=savetodiary)
            savetodiary_button.place(x=20, y=360)

            deleteentry_button = Button(entrydetails_page, text="Remove From Watchlist", font=('Rockwell', 30), command=lambda: [removefromwatchlist(), closeentrydetailspage()])
            deleteentry_button.place(x=300, y=360)

            def closeentrydetailspage():
                entrydetails_page.withdraw()
                watchlist_page.deiconify()

            entrydetailsback_button = Button(entrydetails_page, text="Back", font=('Rockwell', 30), command=closeentrydetailspage)
            entrydetailsback_button.place(x=20, y=430)
        
    #Function that highlights the buttons that allow the user to open or remove a movie, when an watchlist entry is clicked on by the user
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

    #Function and button that is used to create the button that closes the watchlist page and re-opens the home page
    def closewatchlistpage():
        watchlist_page.withdraw()
        home_page.deiconify()

    watchlistback_button = Button(watchlist_page, text="Back", font=('Rockwell', 30), command=closewatchlistpage)
    watchlistback_button.place(x=20, y=430)

watchlist_button=Button(home_page,text="Watchlist",font=button_font,width=button_width,height=2,command=openwatchlistpage)
watchlist_button.place(x=700,y=160,anchor='center')

#Function that creates and opens the recommended page with space for movies the user might like
def openrecommendedpage():
    recommended_page = Toplevel(home_page)
    recommended_page.title("Recommended")
    recommended_page.geometry("900x500")
    home_page.withdraw()

    recommended_heading = Label(recommended_page, text="Recommended", font=('Rockwell', 50, 'bold'))
    recommended_heading.pack()

    #Code to figure out what film the user will like by looking at there watched movies
    recommended_films = set()
    displayed_films = []

    def recommendfilms():
        nonlocal displayed_films
        liked_films = [entry for entry in diary_entries if entry.get('rating', 0) >= 4.0]

        if liked_films:
            for movie_entry in liked_films:
                movie_id = movie_entry['id']
                recommendations_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={API_KEY}&page=1"
                response = requests.get(recommendations_url)
                data = response.json()

                if data['results']:
                    for movie in data['results']:
                        recommended_films.add(movie['id'])

        newrecommended_films = list(recommended_films - set(displayed_films))[:5]
        displayed_films.extend(newrecommended_films)

        for widget in recommended_page.winfo_children():
            if isinstance(widget, Button) and widget != recommendfilm_button and widget != recommendedback_button:
                widget.destroy()

        if newrecommended_films:
            for i, movie_id in enumerate(newrecommended_films):
                movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
                response = requests.get(movie_details_url)
                movie_details = response.json()

                #Function to open the details page for the movie that gets recommended to the user
                def openrecommendeddetailspage(movie_details):
                    recommendeddetails_page = Toplevel(recommended_page)
                    recommendeddetails_page.title(f"{movie_details['title']} Details")
                    recommendeddetails_page.geometry("900x500")
                    recommended_page.withdraw()

                    movietitle_heading = Label(recommendeddetails_page, text=movie_details['title'], font=('Rockwell', 40, 'bold'))
                    movietitle_heading.place(x=240, y=20)

                    poster_path = movie_details.get('poster_path', None)
                    if poster_path:
                        full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                        poster_response = requests.get(full_poster_url)
                        poster_image = Image.open(BytesIO(poster_response.content))
                        poster_image = poster_image.resize((200, 300), Image.LANCZOS)
                        poster_photo = ImageTk.PhotoImage(poster_image)

                        poster_label = Label(recommendeddetails_page, image=poster_photo)
                        poster_label.image = poster_photo
                        poster_label.place(x=20, y=20)

                    releaseyear = movie_details.get('release_date', "N/A")
                    releaseyear_label = Label(recommendeddetails_page, text=f"Year: {releaseyear[:4]}", font=('Rockwell', 30))
                    releaseyear_label.place(x=240, y=70)

                    runtime = movie_details.get('runtime', 'N/A')
                    hours, minutes = divmod(runtime, 60) if runtime != 'N/A' else (0, 0)
                    runtime_str = f"{hours}h {minutes}m" if runtime != 'N/A' else "N/A"
                    runtime_label = Label(recommendeddetails_page, text=f"Runtime: {runtime_str}", font=('Rockwell', 30))
                    runtime_label.place(x=240, y=110)

                    overview = movie_details.get('overview', 'No overview available.')
                    overview_label = Label(recommendeddetails_page, text=f"Overview: {overview}", wraplength=640, font=('Rockwell', 20), justify='left')
                    overview_label.place(x=240, y=150)

                    credits_url = f"https://api.themoviedb.org/3/movie/{movie_details['id']}/credits?api_key={API_KEY}"
                    credits_response = requests.get(credits_url)
                    credits_details = credits_response.json()

                    cast = credits_details.get('cast', [])
                    top_cast = cast[:10]
                    cast_names = ", ".join(member['name'] for member in top_cast)
                    cast_label = Label(recommendeddetails_page, text=f"Cast: {cast_names}", wraplength=640, font=('Rockwell', 20), justify='left')
                    cast_label.place(x=240, y=240)

                    director = next((member['name'] for member in credits_details.get('crew', []) if member['job'] == 'Director'), "N/A")
                    director_label = Label(recommendeddetails_page, text=f"Director: {director}", font=('Rockwell', 30))
                    director_label.place(x=550, y=25)
                    
                    rating_label = Label(recommendeddetails_page, text="Rating:", font=('Rockwell', 20))
                    rating_label.place(x=20, y=330)
                    rating_var = StringVar(value="Pick rating")
                    rating_options = [str(i / 2) for i in range(1, 11)]
                    rating_dropdown = OptionMenu(recommendeddetails_page, rating_var, *rating_options)
                    rating_dropdown.config(font=('Rockwell', 20))
                    rating_dropdown.place(x=100, y=330)

                    #Code for the functions that allow the user to save the movie, or close out the details page
                    def savetodiary():
                        rating = rating_var.get()
                        if rating == "Select a rating":
                            print("Please select a rating before saving.")
                            return
                        watch_date = datetime.now().strftime("%Y-%m-%d")
                        diary_entries.append({"title": movie_details['title'], "date": watch_date, "id": movie_details['id'], "rating": float(rating)})
                        savediary()
                        print(f"Added to Diary: {movie_details['title']} on {watch_date} with rating {rating} stars")

                    savetodiary_button = Button(recommendeddetails_page, text="Save to Diary", font=('Rockwell', 30), command=savetodiary)
                    savetodiary_button.place(x=20, y=360)

                    def savetowatchlist():
                        watchlist_entries.append({"title": movie_details['title'], "id": movie_details['id']})
                        savewatchlist()
                        print(f"Added to Watchlist: {movie_details['title']}")

                    savetowatchlist_button = Button(recommendeddetails_page, text="Save to Watchlist", font=('Rockwell', 30), command=savetowatchlist)
                    savetowatchlist_button.place(x=300, y=360)

                    def closerecommendeddetailspage():
                        recommendeddetails_page.withdraw()
                        recommended_page.deiconify()

                    closerecommendeddetails_button = Button(recommendeddetails_page, text="Close", font=('Rockwell', 30), command=closerecommendeddetailspage)
                    closerecommendeddetails_button.place(x=20, y=430)

                #Code that finds and displays the poster for the recommended movies
                poster_path = movie_details.get('poster_path', None)
                if poster_path:
                    full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    poster_response = requests.get(full_poster_url)
                    poster_image = Image.open(BytesIO(poster_response.content))
                    poster_image = poster_image.resize((150, 200), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)

                    poster_button = Button(recommended_page, image=poster_photo, command=lambda m=movie_details: openrecommendeddetailspage(m))
                    poster_button.image = poster_photo
                    poster_button.place(x=50 + i * 160, y=200)

            recommendfilm_button.config(text="Generate New Recommendations")
            
        else:
            no_recommendations_label = Label(recommended_page, text="No more recommendations available.", font=('Rockwell', 40))
            no_recommendations_label.pack()
            print("No more recommendations available.")
        
    recommendfilm_button = Button(recommended_page, text="Generate Recommendations", font=('Rockwell', 30), command=recommendfilms)
    recommendfilm_button.pack(pady=10)

    #Code for the button that closes the recommended page and takes the user back to the home page
    def closerecommendedpage():
        recommended_page.withdraw()
        home_page.deiconify()

    recommendedback_button = Button(recommended_page, text="Back", font=('Rockwell', 30), command=closerecommendedpage)
    recommendedback_button.place(x=20, y=430)
    
recommended_button=Button(home_page,text="Recommended",font=button_font,width=button_width,height=2,command=openrecommendedpage)
recommended_button.place(x=200,y=300,anchor='center')

#Code to open the search page
def opensearchpage():
    search_page = Toplevel(home_page)
    search_page.title("Search Page")
    search_page.geometry("900x500")
    search_page.resizable(0, 0)
    home_page.withdraw()

    # Function that fetches the movie from TMDB after the user searches for it
    def searchfilm():
        global poster_photo
        filmsearch_result = filmsearch_input.get()
        filmsearch_heading.configure(text=filmsearch_result)

        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={filmsearch_result}"
        response = requests.get(search_url)
        data = response.json()

        # Code to display all the necessary details for the movie the user searched for
        def openmoviedetailspage(movie):
            moviedetails_page = Toplevel(search_page)
            moviedetails_page.title(f"{movie.get('title', 'Movie Details')} Details")
            moviedetails_page.geometry("900x500")
            search_page.withdraw()

            details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={API_KEY}"
            movie_response = requests.get(details_url)
            movie_details = movie_response.json()

            movietitle_heading = Label(moviedetails_page, text=movie.get('title', 'Title not available'), font=('Rockwell', 40, 'bold'))
            movietitle_heading.place(x=240, y=20)

            poster_path = movie.get('poster_path', None)
            if poster_path:
                full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                poster_response = requests.get(full_poster_url)
                poster_image = Image.open(BytesIO(poster_response.content))
                poster_image = poster_image.resize((200, 300), Image.LANCZOS)
                poster_photo = ImageTk.PhotoImage(poster_image)

                poster_label = Label(moviedetails_page, image=poster_photo)
                poster_label.image = poster_photo
                poster_label.place(x=20, y=20)

            releaseyear = movie.get('release_date', "Release date not available")
            releaseyear_label = Label(moviedetails_page, text=f"Year: {releaseyear[:4] if releaseyear != 'Release date not available' else releaseyear}", font=('Rockwell', 30))
            releaseyear_label.place(x=240, y=70)

            runtime = movie_details.get('runtime', 'Runtime not available')
            if isinstance(runtime, int):
                hours, minutes = divmod(runtime, 60)
                runtime_str = f"{hours}h {minutes}m"
            else:
                runtime_str = runtime
            runtime_label = Label(moviedetails_page, text=f"Runtime: {runtime_str}", font=('Rockwell', 30))
            runtime_label.place(x=240, y=110)

            overview = movie.get('overview', 'Overview not available.')
            overview_label = Label(moviedetails_page, text=f"Overview: {overview}", wraplength=640, font=('Rockwell', 20), justify='left')
            overview_label.place(x=240, y=150)

            credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={API_KEY}"
            credits_response = requests.get(credits_url)
            credits_details = credits_response.json()

            cast = credits_details.get('cast', [])
            if cast:
                top_cast = cast[:10]
                cast_names = ", ".join(member.get('name', 'Unknown') for member in top_cast)
            else:
                cast_names = "Cast not available."
            cast_label = Label(moviedetails_page, text=f"Cast: {cast_names}", wraplength=640, font=('Rockwell', 20), justify='left')
            cast_label.place(x=240, y=230)

            director = next((member.get('name', 'Unknown') for member in credits_details.get('crew', []) if member.get('job') == 'Director'), "Director not available")
            director_label = Label(moviedetails_page, text=f"Director: {director}", font=('Rockwell', 30))
            director_label.place(x=550, y=25)

            rating_label = Label(moviedetails_page, text="Rating:", font=('Rockwell', 20))
            rating_label.place(x=20, y=330)
            rating_var = StringVar(value="Pick rating")
            rating_options = [str(i / 2) for i in range(1, 11)]
            rating_dropdown = OptionMenu(moviedetails_page, rating_var, *rating_options)
            rating_dropdown.config(font=('Rockwell', 20))
            rating_dropdown.place(x=100, y=330)

            # Save to diary function
            def savetodiary():
                rating = rating_var.get()
                if rating == "Pick rating":
                    print("Please select a rating before saving.")
                    return
                watch_date = datetime.now().strftime("%Y-%m-%d")
                diary_entries.append({"title": movie.get('title', 'Unknown'), "date": watch_date, "id": movie['id'], "rating": float(rating)})
                savediary()
                print(f"Added to Diary: {movie.get('title', 'Unknown')} on {watch_date} with rating {rating} stars")

            savetodiary_button = Button(moviedetails_page, text="Save to Diary", font=('Rockwell', 30), command=savetodiary)
            savetodiary_button.place(x=20, y=360)

            # Save to watchlist function
            def savetowatchlist():
                watchlist_entries.append({"title": movie.get('title', 'Unknown'), "id": movie['id']})
                savewatchlist()
                print(f"Added to Watchlist: {movie.get('title', 'Unknown')}")

            savetowatchlist_button = Button(moviedetails_page, text="Save to Watchlist", font=('Rockwell', 30), command=savetowatchlist)
            savetowatchlist_button.place(x=300, y=360)

            def closemoviedetailspage():
                moviedetails_page.withdraw()
                search_page.deiconify()

            moviedetailsback_button = Button(moviedetails_page, text="Back", font=('Rockwell', 30), command=closemoviedetailspage)
            moviedetailsback_button.place(x=20, y=430)

        if data.get('results', []):
            for i, movie in enumerate(data['results'][:3]):
                poster_path = movie.get('poster_path')
                if poster_path:
                    full_poster_url = f"{IMAGE_BASE_URL}{poster_path}"
                    poster_response = requests.get(full_poster_url)
                    poster_image = Image.open(BytesIO(poster_response.content))
                    poster_image = poster_image.resize((150, 200), Image.LANCZOS)
                    poster_photo = ImageTk.PhotoImage(poster_image)

                    poster_button = Button(search_page, image=poster_photo, command=lambda m=movie: openmoviedetailspage(m))
                    poster_button.image = poster_photo
                    poster_button.place(x=400 + i * 160, y=240)
                else:
                    print(f"Poster not available for {movie.get('title', 'Unknown')}")

    search_heading = Label(search_page, text="Search Page", font=('Rockwell', 60, 'bold'))
    search_heading.place(x=450, y=60, anchor='center')

    resultsfor_heading = Label(search_page, text="Results for:", font=('Rockwell', 50, 'bold'))
    resultsfor_heading.place(x=50, y=160)

    filmsearch_heading = Label(search_page, text="", font=('Rockwell', 50, 'bold'))
    filmsearch_heading.place(x=400, y=160, width=500)

    filmsearch_input = Entry(search_page, text="", font=('Rockwell', 30))
    filmsearch_input.focus_set()
    filmsearch_input.place(x=50, y=240, width=300)

    filmsearch_button = Button(search_page, text="Search", font=('Rockwell', 30), command=searchfilm)
    filmsearch_button.place(x=50, y=310)

    # Close search page function
    def closesearchpage():
        search_page.withdraw()
        home_page.deiconify()

    searchback_button = Button(search_page, text="Back", font=('Rockwell', 30), command=closesearchpage)
    searchback_button.place(x=20, y=430)

search_button=Button(home_page,text="Search",font=button_font,width=button_width,height=2,command=opensearchpage)
search_button.place(x=700,y=300,anchor='center')

#Code to save the diary and watchlist so it doesn't lose any entries when application is closed
home_page.protocol("WM_DELETE_WINDOW", lambda: [savediary(), savewatchlist(), home_page.destroy()])
home_page.mainloop()
