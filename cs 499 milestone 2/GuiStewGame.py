import tkinter as tk
from tkinter import ttk

global player_location_global
player_location_global = "Living Room"

global player_inventory_global
player_inventory_global = []

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
    "Living Room": "none",
    "Kitchen": "Pot",
    "Pantry": "Spices",
    "Dining Room": "Spoon",
    "Front Yard": "Mushrooms",
    "Veggie Garden": "Veggies",
    "Hallway": "Tray",
    "Guest Bedroom": "none"
}

def gameover():
    ## TODO: This function will be used to determine what text is shown on the game over page.
    if len(player_inventory_global) == 6:
        # YOU WIN
        print("You win") ## DEBUG OUTPUT
    else:
        # YOU LOSE
        print("You lose") ## DEBUG OUTPUT

def navigate(player_location, direction):
    # This function takes the current room that the player is in, the room directory,
    # and the direction entered as arguments. It then checks if the direction is valid
    # for the current room, and updates the player"s location if it is. Otherwise it
    # outputs a message that the direction is invalid.
    if direction.upper() in room_dir[player_location]:
        new_location = room_dir[player_location][direction.upper()]
    if new_location == "Guest Bedroom":
        gameover()
    return new_location

def on_click_north():
    # call the navigate function and update all labels
    global player_location_global
    player_location_global = navigate(player_location_global, "NORTH")
    update_labels()

def on_click_south():
    # call the navigate function and update all labels
    global player_location_global
    player_location_global = navigate(player_location_global, "SOUTH")
    update_labels()

def on_click_east():
    # call the navigate function and update all labels
    global player_location_global
    player_location_global = navigate(player_location_global, "EAST")
    update_labels()

def on_click_west():
    # call the navigate function and update all labels
    global player_location_global
    player_location_global = navigate(player_location_global, "WEST")
    update_labels()

def on_click_get_item():
    global player_location_global
    global player_inventory_global
    global room_items
    if room_items[player_location_global] != "none":
        player_inventory_global.append(room_items[player_location_global])
        room_items[player_location_global] = "none"
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
    if room_items[player_location_global] == "none":
        item_label.config(text="There is nothing here.")
        get_item_button.config(state="disabled")
    else:
        item_label.config(text=room_items[player_location_global])
        get_item_button.config(state="normal")
    # INVENTORY
    index = 0
    for item in player_inventory_global:
        ttk.Label(mainframe, text=item).grid(column=6, row=3+index)
        index += 1

# Create the main application window
root = tk.Tk()
root.title("Gui Stew")
root.geometry('500x275')

# Create a frame widget
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky="nsew")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Spacers
## TODO: This is sloppy. I'm certain there is a better way to do this. Find that and fix this.
ttk.Label(mainframe, text="", width=20).grid(column=6, row=2)
ttk.Label(mainframe, text="", width=2).grid(column=0, row=0)
ttk.Label(mainframe, text="", padding=3).grid(column=2, row=4)
ttk.Label(mainframe, text="", width=2).grid(column=0, row=20)
ttk.Label(mainframe, text="", width=25).grid(column=4, row=0)

# You Are Here
you_are_here = tk.Label(mainframe, text="You are in the "+player_location_global+".")
you_are_here.grid(column=2, row=1, columnspan=3, padx=5, pady=5, sticky="nsw")

# Get Item Button
get_item_button = tk.Button(mainframe, text="Get Item", command=on_click_get_item, state="disabled")
get_item_button.grid(column=2, row=3, sticky="we")

# Item Label
item_label = tk.Label(mainframe, text="There is nothing here.")
item_label.grid(column=4, row=3)

# Direction Buttons
dir_north_button = tk.Button(mainframe, text="Go North", command=on_click_north)
dir_north_button.grid(column=2, row=5, sticky="we")
dir_south_button = tk.Button(mainframe, text="Go South", command=on_click_south)
dir_south_button.grid(column=2, row=6, sticky="we")
dir_east_button = tk.Button(mainframe, text="Go East", command=on_click_east)
dir_east_button.grid(column=2, row=7, sticky="we")
dir_west_button = tk.Button(mainframe, text="Go West", command=on_click_west)
dir_west_button.grid(column=2, row=8, sticky="we")

# Adjacent Room Labels
adjacent_north = tk.Label(mainframe, text=room_dir[player_location_global]["NORTH"])
adjacent_north.grid(column=4, row=5)
adjacent_south = tk.Label(mainframe, text=room_dir[player_location_global]["SOUTH"])
adjacent_south.grid(column=4, row=6)
adjacent_east = tk.Label(mainframe, text=room_dir[player_location_global]["EAST"])
adjacent_east.grid(column=4, row=7)
adjacent_west = tk.Label(mainframe, text=room_dir[player_location_global]["WEST"])
adjacent_west.grid(column=4, row=8)

# Inventory
inventory_label = ttk.Label(mainframe, text="Inventory", justify="center", border=1, borderwidth=1).grid(column=6, row=2)

root.mainloop()

## TODO: Add a home page
# The home page will display the welcome message of the game, and have two buttons. One starts a new game,
# and the other takes the user to a high score page.

## TODO: Add a high score page
# This page displays the top 5 or so high scores, and has a button to return to the home page.

## TODO: Add a game over page
# This page displays a game over message and has a button to return to the home page.