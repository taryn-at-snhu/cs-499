# Taryn Brownfield
# CS 499 Capstone Project

import tkinter as tk
from tkinter import ttk
import sqlite3

class Player:
    def __init__(self):
        self.location = "Living Room"
        self.inventory = []
        self.nav_count = 0
        self.score = 0
        self.items_by_room = {
            "Living Room": ["none"],
            "Kitchen": ["Dutch Oven", "Iron Pot", "Rusty Pot"],
            "Pantry": ["Herbs", "Salt & Pepper", "Jar of Suspicious Liquid"],
            "Dining Room": ["Wooden Spoon", "Metal Spoon", "Broken Fork"],
            "Front Yard": ["Mushrooms", 
                           "Beef Chunks, Freshly Butchered", 
                           "Earthworms"],
            "Veggie Garden": ["Onions", "Carrots", "Strange Moss"],
            "Hallway": ["Wooden Tray", "Silver Tray", "Flat Rock"],
            "Guest Bedroom": ["none"]
        }

class Game_Info:
    def __init__(self, game_frame, player, root, c):
        self.you_are_here = tk.Label(game_frame, 
                            text="You are in the " + player.location + ".")
        self.item_box = ttk.Combobox(game_frame, 
                            values="")
        self.get_item_button = tk.Button(game_frame,
                                text="Get Item",
                                command=lambda: on_click_get_item(player),
                                state="disabled")
        self.dir_north_button = tk.Button(game_frame, 
                                          text="Go North",
                                          command=lambda: 
                                            on_click_direction(player, 
                                                               "NORTH",
                                                               root,
                                                               c))
        self.dir_south_button = tk.Button(game_frame, 
                                          text="Go South", 
                                          command=lambda: 
                                            on_click_direction(player, 
                                                               "SOUTH",
                                                               root,
                                                               c))
        self.dir_east_button = tk.Button(game_frame, 
                                         text="Go East", 
                                         command=lambda: 
                                            on_click_direction(player, 
                                                               "EAST",
                                                               root,
                                                               c))
        self.dir_west_button = tk.Button(game_frame, 
                                         text="Go West", 
                                         command=lambda: 
                                            on_click_direction(player, 
                                                               "WEST",
                                                               root,
                                                               c))
        self.adjacent_north = tk.Label(game_frame, 
                                       text=room_dir[player.location]["NORTH"],
                                       width=30)
        self.adjacent_south = tk.Label(game_frame, 
                                       text=room_dir[player.location]["SOUTH"])
        self.adjacent_east = tk.Label(game_frame, 
                                      text=room_dir[player.location]["EAST"])
        self.adjacent_west = tk.Label(game_frame, 
                                      text=room_dir[player.location]["WEST"])
        self.inventory_label = tk.Label(game_frame, 
                                        text="Inventory [0/6]", 
                                        justify="center", 
                                        width=30)
        self.inventory_item_1 = tk.Label(game_frame, text="")
        self.inventory_item_2 = tk.Label(game_frame, text="")
        self.inventory_item_3 = tk.Label(game_frame, text="")
        self.inventory_item_4 = tk.Label(game_frame, text="")
        self.inventory_item_5 = tk.Label(game_frame, text="")
        self.inventory_item_6 = tk.Label(game_frame, text="")
        
        def update(player):
            # YOU ARE HERE
            self.you_are_here.config(text=
                                     "You are in the " + player.location + ".")
            # DIRECTIONS
            if "NORTH" in room_dir[player.location]:
                self.adjacent_north.config(
                    text=room_dir[player.location]["NORTH"])
                self.dir_north_button.config(state="normal")
            else:
                self.adjacent_north.config(
                    text="There is nothing in that direction.")
                self.dir_north_button.config(state="disabled")
            if "SOUTH" in room_dir[player.location]:
                self.adjacent_south.config(
                    text=room_dir[player.location]["SOUTH"])
                self.dir_south_button.config(state="normal")
            else:
                self.adjacent_south.config(
                    text="There is nothing in that direction.")
                self.dir_south_button.config(state="disabled")
            if "EAST" in room_dir[player.location]:
                self.adjacent_east.config(
                    text=room_dir[player.location]["EAST"])
                self.dir_east_button.config(state="normal")
            else:
                self.adjacent_east.config(
                    text="There is nothing in that direction.")
                self.dir_east_button.config(state="disabled")
            if "WEST" in room_dir[player.location]:
                self.adjacent_west.config(
                    text=room_dir[player.location]["WEST"])
                self.dir_west_button.config(state="normal")
            else:
                self.adjacent_west.config(
                    text="There is nothing in that direction.")
                self.dir_west_button.config(state="disabled")
            # ITEM
            if player.items_by_room[player.location] == ["none"]:
                self.item_box.config(values="")
                self.item_box.set("There is nothing here.")
                self.get_item_button.config(state="disabled")
            else:
                self.item_box.config(values=
                                     player.items_by_room[player.location])
                self.item_box.set("There is something here.")
                self.get_item_button.config(state="normal")
            # INVENTORY
            self.inventory_label.config(text="Inventory [" 
                                        + str(len(player.inventory)) 
                                        + "/6]")
            if len(player.inventory) > 0:
                self.inventory_item_1.config(text=player.inventory[0])
            if len(player.inventory) > 1:
                self.inventory_item_2.config(text=player.inventory[1])
            if len(player.inventory) > 2:
                self.inventory_item_3.config(text=player.inventory[2])
            if len(player.inventory) > 3:
                self.inventory_item_4.config(text=player.inventory[3])
            if len(player.inventory) > 4:
                self.inventory_item_5.config(text=player.inventory[4])
            if len(player.inventory) > 5:
                self.inventory_item_6.config(text=player.inventory[5])

        def on_click_direction(player, direction, root, c):
            player.location = room_dir[player.location][direction]
            player.nav_count += 1
            if player.location == "Guest Bedroom":
                game_over(root, player, c)
            update(player)

        def on_click_get_item(player):
            if self.item_box.get() != "There is something here.":
                player.inventory.append(self.item_box.get())
                player.items_by_room[player.location] = ["none"]
            update(player)

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

mushroom_stew = ["Dutch Oven", 
                 "Herbs", 
                 "Wooden Spoon", 
                 "Mushrooms", 
                 "Onions", 
                 "Wooden Tray"]

beef_stew = ["Iron Pot", 
             "Salt & Pepper", 
             "Metal Spoon", 
             "Beef Chunks, Freshly Butchered", 
             "Carrots", 
             "Silver Tray"]

gooey_stew = ["Rusty Pot", 
              "Jar of Suspicious Liquid", 
              "Broken Fork", 
              "Earthworms", 
              "Strange Moss", 
              "Flat Rock"]

def start_menu(root, c):
    # Create a frame for the start page
    startframe = ttk.Frame(root)
    startframe.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
    startframe.columnconfigure(0, weight=1)
    startframe.columnconfigure(1, weight=1)
    startframe.columnconfigure(2, weight=1)
    startframe.columnconfigure(3, weight=1)

    # Welcome text
    tk.Label(startframe, 
             text="*** GUI Stew ***"
             ).grid(column=0, row=0, columnspan=4, padx=300, pady=10)
    tk.Label(startframe, 
             text="Collect everything you need to make and serve a delicious" \
                " stew\nbefore entering the guest bedroom, or be eaten by " \
                "your hangry guest!"
             ).grid(column=0, row=1, columnspan=4)
    tk.Label(startframe, 
             text="Tip: Try combining different items and minimizing " \
                "movements for a high score!"
             ).grid(column=0, row=2, columnspan=4, pady=10)
    tk.Label(startframe, 
             text="*** Have fun! ***"
             ).grid(column=0, row=3, columnspan=4, pady=10)

    # Start a new game
    select_new_game = tk.Button(startframe, 
                                text="New Game",
                                command=lambda: new_game(root, c))
    select_new_game.grid(column=1, row=4, sticky="e", pady=10)

    # View High Scores
    select_high_scores = tk.Button(startframe, 
                                   text="High Scores", 
                                   command=lambda: view_high_scores(root, c))
    select_high_scores.grid(column=2, row=4, sticky="w")

def new_game(root, c):
    # Initialize the game
    player = Player()
    game_play(root, player, c)

def on_click_save_name(player, player_name_input, c, save_name_button):
    player_name = player_name_input.get()
    player_name = player_name[:20]
    if player_name != "" and "'" not in player_name and ";" not in player_name:
        c.execute("SELECT COUNT(*) FROM HIGHSCORES")
        count_high_scores = c.fetchone()[0]
        # Determine player_id for the HIGHSCORES database
        if count_high_scores >= 10:
            # If there are already 10 records, replace the lowest scoring 
            # record
            c.execute("SELECT MIN(SCORE), ID FROM HIGHSCORES")
            player_id = c.fetchone()[1]
            c.execute("UPDATE HIGHSCORES SET PLAYER_NAME = '{0}', SCORE = " \
                      "{1} WHERE ID = {2}".format(player_name, 
                                                  player.score, 
                                                  player_id))
        else:
            # Otherwise, get the current highest ID and increment
            c.execute("SELECT MAX(ID) FROM HIGHSCORES")
            player_id = c.fetchone()[0]
            if type(player_id) is int:
                # If previous entries exist, increment the most recent ID
                player_id += 1
            else:
                # If this is the first entry set the ID to 1
                player_id = 1
            c.execute("INSERT INTO HIGHSCORES (ID, PLAYER_NAME, SCORE) " \
                      "VALUES ({0}, '{1}', {2})".format(player_id, 
                                                        player_name, 
                                                        player.score))
        save_name_button.config(state="disabled")

def new_high_score(game_over_frame, player, c):
    tk.Label(game_over_frame, 
             text="*** NEW HIGH SCORE! ***"
             ).grid(column=1, row=5, columnspan=2, pady=5)
    tk.Label(game_over_frame, 
             text="Enter your name"
             ).grid(column=1, row=6, columnspan=2)
    player_name_input = tk.Entry(game_over_frame)
    player_name_input.grid(column=1, row=7, columnspan=2)
    save_name_button = tk.Button(game_over_frame, 
                            text="Save Name", 
                            command=lambda: on_click_save_name(player, 
                                                            player_name_input, 
                                                            c, 
                                                            save_name_button), 
                                                            state="normal")
    save_name_button.grid(column=1, row=8, columnspan=2)

def game_over(root, player, c):
    # Create a frame for the game over page
    game_over_frame = ttk.Frame(root)
    game_over_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
    game_over_frame.columnconfigure(0, weight=1)
    game_over_frame.columnconfigure(1, weight=1)
    game_over_frame.columnconfigure(2, weight=1)
    game_over_frame.columnconfigure(3, weight=1)

    if len(player.inventory) == 6:
        # PLAYER WIN
        you_win = tk.Label(game_over_frame, text="*** YOU WIN! ***")
        you_win.grid(column=1, row=0, columnspan=2, pady=10)
        
        multiplier_mushroom = 0
        multiplier_beef = 0
        multiplier_gooey = 0

        # Calculate base score and multipliers
        for item in player.inventory:
            if item in mushroom_stew:
                player.score += 15
                multiplier_mushroom += 1
            if item in beef_stew:
                player.score += 10
                multiplier_beef += 2
            if item in gooey_stew:
                player.score += 5
                multiplier_gooey += 5
        
        # Calculate penalty -- the minimum number of navigations in order to 
        # win the game is 12, and any navigation beyond that are 15 penalty 
        # points each
        penalty = (player.nav_count - 12) * 15

        # Perfect stew determination -- doubles the score before penalty
        perfect_multiplier = 1
        if multiplier_mushroom == 6:
            tk.Label(game_over_frame, 
                     text="* You made a perfect mushroom stew! *"
                     ).grid(column=1, row=1, columnspan=2, pady=10)
            perfect_multiplier = 2
        elif multiplier_beef == 12:
            tk.Label(game_over_frame, 
                     text="* You made a perfect beef stew! *"
                     ).grid(column=1, row=1, columnspan=2, pady=10)
            perfect_multiplier = 2
        elif multiplier_gooey == 30:
            tk.Label(game_over_frame, 
                     text="* You made a perfect gooey stew! *"
                     ).grid(column=1, row=1, columnspan=2, pady=10)
            perfect_multiplier = 2
        else:
            tk.Label(game_over_frame, 
                     text="* You made a motley stew. *"
                     ).grid(column=1, row=1, columnspan=2, pady=10)
        
        # Final score calculation
        player.score = (player.score 
                        * (multiplier_mushroom 
                           + multiplier_beef 
                           + multiplier_gooey
                           ) * perfect_multiplier
                           ) - penalty
        tk.Label(game_over_frame, 
                 text="You scored " + str(player.score) + " points!"
                 ).grid(column=1, row=2, columnspan=2, pady=10)

        # Fetch High Score data
        c.execute("SELECT COUNT(*) FROM HIGHSCORES")
        count_high_scores = c.fetchone()[0]

        # If there are fewer than 10 recorded scores, record the new high 
        # score.
        if count_high_scores < 10:
            new_high_score(game_over_frame, player, c)
        # If there are more than 10 recorded scores, check whether the new
        # score is higher than the lowest score and if so, record it and
        # replace the lowest scoring entry.
        else:
            c.execute("SELECT MIN(SCORE) FROM HIGHSCORES")
            lowest_high_score = c.fetchone()[0]
            if player.score > lowest_high_score:
                new_high_score(game_over_frame, player, c)

    else:
        # PLAYER LOSE
        you_lose = tk.Label(game_over_frame, text="*** YOU LOSE! ***")
        you_lose.grid(column=1, row=0, columnspan=2, pady=20)
    
    tk.Label(game_over_frame, text="Play again?").grid(column=1, 
                                                       row=9, 
                                                       columnspan=2)
    tk.Button(game_over_frame, text="Start Menu", 
              command=lambda: start_menu(root, c)).grid(column=1, 
                                                        row=10, 
                                                        columnspan=2)

def game_play(root, player, c):
    # Create the frame for the game
    game_frame = ttk.Frame(root)
    game_frame.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)

    game = Game_Info(game_frame, player, root, c)
    
    # You Are Here
    game.you_are_here.grid(column=0, 
                           row=0, 
                           columnspan=3, 
                           padx=5, 
                           pady=5, 
                           sticky="nsw")
    
    # Item Combobox
    game.item_box.set("There is nothing here.")
    game.item_box.grid(column=1, row=2, sticky="we")

    # Get Item
    game.get_item_button.grid(column=0, row=2, sticky="we", pady=15)

    # Direction Buttons
    game.dir_north_button.grid(column=0, row=5, sticky="we")
    game.dir_south_button.grid(column=0, row=6, sticky="we")
    game.dir_east_button.grid(column=0, row=7, sticky="we")
    game.dir_west_button.grid(column=0, row=8, sticky="we")

    # Adjacent room labels
    game.adjacent_north.grid(column=1, row=5, columnspan=3)
    game.adjacent_south.grid(column=1, row=6, columnspan=3)
    game.adjacent_east.grid(column=1, row=7, columnspan=3)
    game.adjacent_west.grid(column=1, row=8, columnspan=3)

    # Inventory Label
    game.inventory_label.grid(column=4, row=2, padx=10)
    game.inventory_item_1.grid(column=4, row=5, pady=3)
    game.inventory_item_2.grid(column=4, row=6, pady=3)
    game.inventory_item_3.grid(column=4, row=7, pady=3)
    game.inventory_item_4.grid(column=4, row=8, pady=3)
    game.inventory_item_5.grid(column=4, row=9, pady=3)
    game.inventory_item_6.grid(column=4, row=10, pady=3)

def view_high_scores(root, c):
    # Create a frame for the high scores page
    highscoresframe = ttk.Frame(root)
    highscoresframe.grid(column=0, row=0, sticky="nsew", padx=20, pady=20)
    highscoresframe.columnconfigure(0, weight=1)
    highscoresframe.columnconfigure(1, weight=1)
    highscoresframe.columnconfigure(2, weight=1)
    highscoresframe.columnconfigure(3, weight=1)

    tk.Label(highscoresframe, 
             text="*** HIGH SCORES! ***"
             ).grid(column=1, row=0, columnspan=2)
    tk.Label(highscoresframe, text="PLAYER").grid(column=1, row=1)
    tk.Label(highscoresframe, text="SCORE").grid(column=2, row=1)

    # Fetch all records from the HIGHSCORES database
    c.execute("SELECT * FROM HIGHSCORES ORDER BY SCORE DESC LIMIT 10")
    rows = c.fetchall()
    index = 0
    for row in rows:
        tk.Label(highscoresframe, text=row[1]).grid(column=1, row=2+index)
        tk.Label(highscoresframe, text=row[2]).grid(column=2, row=2+index)
        index += 1

    tk.Button(highscoresframe, 
              text="Main Menu", 
              command=lambda: start_menu(root, c)
              ).grid(column=1, row=20, columnspan=2)

def main():
    # Create the main application window
    root = tk.Tk()
    root.title("Gui Stew")
    root.geometry("750x350")

    # Create or connect to the database and HIGHSCORES table
    high_scores_conn = sqlite3.connect('highscores.db') # connection
    c = high_scores_conn.cursor() # cursor
    c.execute('''
        CREATE TABLE IF NOT EXISTS HIGHSCORES (
            ID            INTEGER PRIMARY KEY     NOT NULL,
            PLAYER_NAME   CHAR(8)                 NOT NULL,
            SCORE         INTEGER                 NOT NULL
        )
    ''')

    start_menu(root, c)

    root.mainloop()

    high_scores_conn.commit()
    high_scores_conn.close()

if __name__ == '__main__':
    main()