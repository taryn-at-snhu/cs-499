# Taryn Brownfield
# CS 499 Milestone 2 Enhancement

import tkinter as tk
from tkinter import ttk
import sqlite3

global debug
debug = False

global player_location_global
player_location_global = "Living Room"

global player_inventory_global
player_inventory_global = []

global nav_count
nav_count = 0

room_dir = {
    "Living Room": {
        "NORTH": "Veggie Garden",
        "EAST": "Kitchen",
        "SOUTH": "Front Yard",
        "WEST": "Hallway"
        },
    "Kitchen": {
        "EAST": "Pantry",
        "SOUTH": "Dining Room",
        "WEST": "Living Room"
    },
    "Pantry": {
        "WEST": "Kitchen"
    },
    "Dining Room": {
        "NORTH": "Kitchen"
    },
    "Front Yard": {
        "NORTH": "Living Room"
    },
    "Veggie Garden": {
        "SOUTH": "Living Room"
    },
    "Hallway": {
        "NORTH": "Guest Bedroom",
        "EAST": "Living Room"
    },
    "Guest Bedroom": {
        "SOUTH": "Hallway"
    }
}

global room_items
room_items = {
    "Living Room": ["none"],
    "Kitchen": ["Dutch Oven", "Iron Pot", "Rusty Pot"],
    "Pantry": ["Herbs", "Salt & Pepper", "Jar of Suspicious Liquid"],
    "Dining Room": ["Wooden Spoon", "Metal Spoon", "Broken Fork"],
    "Front Yard": ["Mushrooms", "Beef Chunks, Freshly Butchered", "Earthworms"],
    "Veggie Garden": ["Onions", "Carrots", "Strange Moss"],
    "Hallway": ["Wooden Tray", "Silver Tray", "Flat Rock"],
    "Guest Bedroom": ["none"]
}

mushroom_stew = ["Dutch Oven", "Herbs", "Wooden Spoon", "Mushrooms", "Onions", "Wooden Tray"]

beef_stew = ["Iron Pot", "Salt & Pepper", "Metal Spoon", "Beef Chunks, Freshly Butchered", "Carrots", "Silver Tray"]

gooey_stew = ["Rusty Pot", "Jar of Suspicious Liquid", "Broken Fork", "Earthworms", "Strange Moss", "Flat Rock"]

def main_menu():
    # Create a frame for the start page
    startframe = ttk.Frame(root)
    startframe.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
    startframe.columnconfigure(0, weight=1)
    startframe.columnconfigure(1, weight=1)
    startframe.columnconfigure(2, weight=1)
    startframe.columnconfigure(3, weight=1)

    # Welcome text
    tk.Label(startframe, text="*** GUI Stew ***").grid(column=0, row=0, columnspan=4)
    tk.Label(startframe, text="Collect everything you need to make and serve a delicious stew\nbefore entering the guest bedroom, or be eaten by your hangry guest!").grid(column=0, row=1, columnspan=4)
    tk.Label(startframe, text="Tip: Try combining different items and minimizing movements for a high score!").grid(column=0, row=2, columnspan=4)
    tk.Label(startframe, text="*** Have fun! ***").grid(column=0, row=3, columnspan=4)

    # Start a new game
    select_new_game = tk.Button(startframe, text="New Game", command=newgame)
    select_new_game.grid(column=1, row=4, sticky="e")

    # View High Scores ## TODO: Implememnt High Scores View
    select_high_scores = tk.Button(startframe, text="High Scores", command=view_high_scores)
    select_high_scores.grid(column=2, row=4, sticky="w")

def newgame():
    global player_location_global
    player_location_global = "Living Room"
    global player_inventory_global
    player_inventory_global = []
    global nav_count
    nav_count = 0
    update_labels()
    mainframe.tkraise()

def view_high_scores():
    # Create a frame for the start page
    highscoresframe = ttk.Frame(root)
    highscoresframe.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
    highscoresframe.columnconfigure(0, weight=1)
    highscoresframe.columnconfigure(1, weight=1)
    highscoresframe.columnconfigure(2, weight=1)
    highscoresframe.columnconfigure(3, weight=1)

    tk.Label(highscoresframe, text="*** HIGH SCORES! ***").grid(column=1, row=0, columnspan=2)
    tk.Label(highscoresframe, text="PLAYER").grid(column=1, row=1)
    tk.Label(highscoresframe, text="SCORE").grid(column=2, row=1)

    # Fetch all records
    c.execute("SELECT * FROM HIGHSCORES ORDER BY SCORE DESC LIMIT 10")
    rows = c.fetchall()
    index = 0
    for row in rows:
        tk.Label(highscoresframe, text=row[1]).grid(column=1, row=2+index)
        tk.Label(highscoresframe, text=row[2]).grid(column=2, row=2+index)
        index += 1

    tk.Button(highscoresframe, text="Main Menu", command=main_menu).grid(column=1, row=20, columnspan=2)

def on_click_save_name(player_name_input, score, save_name_button):
    player_name = player_name_input.get()
    if player_name != "":
        # Get the most recently used ID and increase by 1 for next instance
        c.execute("SELECT MAX(ID) FROM HIGHSCORES")
        player_id = c.fetchone()[0]
        if type(player_id) is int:
            player_id += 1
        else:
            # If this is the first instance, set the ID to 1
            player_id = 1
        c.execute("INSERT INTO HIGHSCORES (ID, PLAYER_NAME, SCORE) " \
            "VALUES ({0}, '{1}', {2})".format(player_id, player_name, score))
        save_name_button.config(state="disabled")

def gameover():
    # Create a frame for the game over page
    game_over_frame = ttk.Frame(root)
    game_over_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
    game_over_frame.columnconfigure(0, weight=1)
    game_over_frame.columnconfigure(1, weight=1)
    game_over_frame.columnconfigure(2, weight=1)
    game_over_frame.columnconfigure(3, weight=1)

    if len(player_inventory_global) == 6:
        # YOU WIN
        tk.Label(game_over_frame, text="*** YOU WIN! ***").grid(column=1, row=0, columnspan=2)
        multiplier_mushroom = 0
        multiplier_beef = 0
        multiplier_gooey = 0
        score = 0
        
        for item in player_inventory_global:
            if item in mushroom_stew:
                score += 15
                multiplier_mushroom += 1
            if item in beef_stew:
                score += 10
                multiplier_beef += 2
            if item in gooey_stew:
                score += 5
                multiplier_gooey += 5
        
        penalty = (nav_count - 12) * 15 # The minimum number of navigations to win the game is 12, and any navigations beyond that are 15 penalty points each
        
        score = score * (multiplier_mushroom + multiplier_beef + multiplier_gooey) - penalty

        c.execute("SELECT COUNT(*) FROM HIGHSCORES")
        count_high_scores = c.fetchone()[0]
        if count_high_scores >= 10:
            # Find the lowest score in the HIGHSCORES database
            c.execute("SELECT MIN(SCORE) FROM HIGHSCORES")
            min_high_score = c.fetchone()[0]
            if score > min_high_score:
                tk.Label(game_over_frame, text="You scored " + str(score) + " points!").grid(column=1, row=2, columnspan=2)
                tk.Label(game_over_frame, text="*** NEW HIGH SCORE! ***").grid(column=1, row=3, columnspan=2)
                player_name_label = tk.Label(game_over_frame, text="Enter your name:")
                player_name_label.grid(column=1, row=4, columnspan=2)
                player_name_input = tk.Entry(game_over_frame)
                player_name_input.grid(column=1, row=5, columnspan=2)
                save_name_button = tk.Button(game_over_frame, 
                                            text="Save Name", 
                                            command=lambda: on_click_save_name(player_name_input, score),
                                            state="normal")
                save_name_button.grid(column=1, row=6, columnspan=2)
                tk.Label(game_over_frame, text="Play again?").grid(column=1, row=7, columnspan=2)
                tk.Button(game_over_frame, text="Main Menu", command=main_menu).grid(column=1, row=8, columnspan=2)
            else:
                tk.Label(game_over_frame, text="You scored " + str(score) + " points!").grid(column=1, row=2, columnspan=2)
                tk.Label(game_over_frame, text="Play again?").grid(column=1, row=3, columnspan=2)
                tk.Button(game_over_frame, text="Main Menu", command=main_menu).grid(column=1, row=4, columnspan=2)
        else:
            tk.Label(game_over_frame, text="You scored " + str(score) + " points!").grid(column=1, row=2, columnspan=2)
            tk.Label(game_over_frame, text="*** NEW HIGH SCORE! ***").grid(column=1, row=3, columnspan=2)
            player_name_label = tk.Label(game_over_frame, text="Enter your name:")
            player_name_label.grid(column=1, row=4, columnspan=2)
            player_name_input = tk.Entry(game_over_frame)
            player_name_input.grid(column=1, row=5, columnspan=2)
            save_name_button = tk.Button(game_over_frame, 
                                        text="Save Name", 
                                        command=lambda: on_click_save_name(player_name_input, score, save_name_button))
            save_name_button.grid(column=1, row=6, columnspan=2)
            tk.Label(game_over_frame, text="Play again?").grid(column=1, row=7, columnspan=2)
            tk.Button(game_over_frame, text="Main Menu", command=main_menu).grid(column=1, row=8, columnspan=2)
    else:
        # YOU LOSE
        tk.Label(game_over_frame, text="*** YOU LOSE! ***").grid(column=1, row=0, columnspan=2)
        tk.Label(game_over_frame, text="Play again?").grid(column=1, row=1, columnspan=2)
        tk.Button(game_over_frame, text="Main Menu", command=main_menu).grid(column=1, row=2, columnspan=2)

def navigate(player_location, direction):
    new_location = room_dir[player_location][direction]
    global nav_count
    nav_count += 1
    if new_location == "Guest Bedroom":
        gameover()
    return new_location

def on_click_north():
    # This function calls the navigate function to go North and updates all labels accordingly.
    global player_location_global
    player_location_global = navigate(player_location_global, "NORTH")
    update_labels()

def on_click_south():
    # This function calls the navigate function to go Sout and updates all labels accordingly.
    global player_location_global
    player_location_global = navigate(player_location_global, "SOUTH")
    update_labels()

def on_click_east():
    # This function calls the navigate function to go East and updates all labels accordingly.
    global player_location_global
    player_location_global = navigate(player_location_global, "EAST")
    update_labels()

def on_click_west():
    # This function calls the navigate function to go West and updates all labels accordingly.
    global player_location_global
    player_location_global = navigate(player_location_global, "WEST")
    update_labels()

def on_click_get_item():
    # This function adds the item to the user's inventory and removes it from the room.
    global player_location_global
    global player_inventory_global
    global room_items
    if item_box.get() != "There is something here.":
        player_inventory_global.append(item_box.get())
        room_items[player_location_global] = ["none"]
    update_labels()

def update_labels():
    # YOU ARE HERE
    you_are_here.config(text="You are in the "+player_location_global+".")
    # DIRECTIONS
    if "NORTH" in room_dir[player_location_global]:
        adjacent_north.config(text=room_dir[player_location_global]["NORTH"])
        dir_north_button.config(state="normal")
    else:
        adjacent_north.config(text="There is nothing in that direction.")
        dir_north_button.config(state="disabled")
    if "SOUTH" in room_dir[player_location_global]:
        adjacent_south.config(text=room_dir[player_location_global]["SOUTH"])
        dir_south_button.config(state="normal")
    else:
        adjacent_south.config(text="There is nothing in that direction.")
        dir_south_button.config(state="disabled")
    if "EAST" in room_dir[player_location_global]:
        adjacent_east.config(text=room_dir[player_location_global]["EAST"])
        dir_east_button.config(state="normal")
    else:
        adjacent_east.config(text="There is nothing in that direction.")
        dir_east_button.config(state="disabled")
    if "WEST" in room_dir[player_location_global]:
        adjacent_west.config(text=room_dir[player_location_global]["WEST"])
        dir_west_button.config(state="normal")
    else:
        adjacent_west.config(text="There is nothing in that direction.")
        dir_west_button.config(state="disabled")
    # ITEM
    if room_items[player_location_global] == ["none"]:
        item_box.set("There is nothing here.")
        get_item_button.config(state="disabled")
    else:
        item_box.config(values=room_items[player_location_global])
        item_box.set("There is something here.")
        get_item_button.config(state="normal")
    # INVENTORY
    index = 0
    for item in player_inventory_global:
        ttk.Label(mainframe, text=item).grid(column=3, row=5+index, pady=3)
        index += 1
    inventory_label.config(text="Inventory [" + str(len(player_inventory_global)) + "/6]")

# Create the main application window
root = tk.Tk()
root.title("Gui Stew")
root.geometry("700x350")

# Create the database and HIGHSCORES table
high_scores_conn = sqlite3.connect('highscores.db')
c = high_scores_conn.cursor() # cursor
c.execute('''
    CREATE TABLE IF NOT EXISTS HIGHSCORES (
        ID            INTEGER PRIMARY KEY     NOT NULL,
        PLAYER_NAME   CHAR(8)                 NOT NULL,
        SCORE         INTEGER                 NOT NULL
    )
''')

# Create a frame widget for the game
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)

# You Are Here
you_are_here = tk.Label(mainframe, text="You are in the "+player_location_global+".")
you_are_here.grid(column=0, row=0, columnspan=3, padx=5, pady=5, sticky="nsw")

# Get Item Button
get_item_button = tk.Button(mainframe, text="Get Item", command=on_click_get_item, state="disabled")
get_item_button.grid(column=0, row=2, sticky="we", pady=15)

# Item Label
item_box = ttk.Combobox(mainframe, values=room_items[player_location_global])
item_box.set("There is nothing here.")
item_box.grid(column=1, row=2, sticky="we")

# Direction Buttons
dir_north_button = tk.Button(mainframe, text="Go North", command=on_click_north)
dir_north_button.grid(column=0, row=5, sticky="we")
dir_south_button = tk.Button(mainframe, text="Go South", command=on_click_south)
dir_south_button.grid(column=0, row=6, sticky="we")
dir_east_button = tk.Button(mainframe, text="Go East", command=on_click_east)
dir_east_button.grid(column=0, row=7, sticky="we")
dir_west_button = tk.Button(mainframe, text="Go West", command=on_click_west)
dir_west_button.grid(column=0, row=8, sticky="we")

# Adjacent Room Labels
adjacent_north = tk.Label(mainframe, text=room_dir[player_location_global]["NORTH"], width=30)
adjacent_north.grid(column=1, row=5)
adjacent_south = tk.Label(mainframe, text=room_dir[player_location_global]["SOUTH"])
adjacent_south.grid(column=1, row=6)
adjacent_east = tk.Label(mainframe, text=room_dir[player_location_global]["EAST"])
adjacent_east.grid(column=1, row=7)
adjacent_west = tk.Label(mainframe, text=room_dir[player_location_global]["WEST"])
adjacent_west.grid(column=1, row=8)

# Inventory Label
inventory_label = tk.Label(mainframe, text="Inventory [0/6]", justify="center", width=30)
inventory_label.grid(column=3, row=2, padx=10)

main_menu()

root.mainloop()

high_scores_conn.commit()
high_scores_conn.close()

## TODO: Comment code
## TODO: refactor code. it needs work.
## TODO: remove debug statements