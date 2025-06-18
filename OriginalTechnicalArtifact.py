# Taryn Brownfield
# IT 140 - Project 2

def welcome():
    print('\n\n*** Welcome to the Mushroom Stew Game! ***')
    print('Collect everything you need to make and serve a delicious mushroom stew, or be eaten by your hangry guest!\n')
    print('To move around, type \'go <direction>\' (North, East, South, or West) and hit enter.')
    print('To add an item to your inventory, type \'get <item name>\' and hit enter.')
    print('\n*** Have fun ***!\n')

def navigation(current_room, room_dir, direction):
    # This function takes the current room that the player is in, the room directory,
    # and the direction entered as arguments. It then checks if the direction is valid
    # for the current room, and updates the player's location if it is. Otherwise it
    # outputs a message that the direction is invalid.
    if direction.upper() in room_dir[current_room]:
        you_are_here = room_dir[current_room][direction.upper()]
    else:
        print('That is not a valid direction for this room. Try again.')
        you_are_here = current_room
    return you_are_here

def get_item(current_room, room_items, basket):
    # This function takes the current player location, the dictionary of room items,
    # and the player's current inventory as arguments. It then adds the item from the
    # current room to the player's inventory, and returns the inventory.
    basket.append(room_items[current_room])
    return basket

def action(current_room, room_dir, basket, necessary_items):
    # This function takes the current player location, the room directory, the player's
    # current inventory, and the list of necessary items as arguments. It then gets a
    # command from the player, and checks whether the command is a valid one. If it is
    # a valid "go" command, then the function calls the navigation function. If it is
    # a valid "get" command, then the function calls the get_items function. It returns
    # a list with the player's current location and inventory.
    choice_valid = False
    while choice_valid == False:
        command = input('What would you like to do next? [Go <direction>, Get <item>]: ')
        command_list = command.split()
        
        # If the user inputs a "go" command, use the navigation function
        if command_list[0].upper() == 'GO':
            you_are_here = navigation(current_room, room_dir, command_list[1])
            choice_valid = True
        
        # If the user inputs a "get" command, use the get_items function
        elif command_list[0].upper() == 'GET':
            if (command_list[1].lower() in necessary_items) and (command_list[1].lower() not in basket):
                basket.append(command_list[1])
            else:
                print('There is nothing to get.')
            you_are_here = current_room
            choice_valid = True
        
        else:
            you_are_here = current_room
            print('Your input was invalid: try again.')

    return [you_are_here, basket]
    

def main():
    welcome()

    room_dir = {
        'Living Room': {
            'NORTH': 'Veggie Garden',
            'EAST': 'Kitchen',
            'SOUTH': 'Front Yard',
            'WEST': 'Hallway'
            },
        'Kitchen': {
            'EAST': 'Pantry',
            'SOUTH': 'Dining Room',
            'WEST': 'Living Room'
        },
        'Pantry': {
            'WEST': 'Kitchen'
        },
        'Dining Room': {
            'NORTH': 'Kitchen'
        },
        'Front Yard': {
            'NORTH': 'Living Room'
        },
        'Veggie Garden': {
            'SOUTH': 'Living Room'
        },
        'Hallway': {
            'NORTH': 'Guest Bedroom',
            'EAST': 'Living Room'
        },
        'Guest Bedroom': {
            'SOUTHs': 'Hallway'
        }
    }

    room_items = {
        'Living Room': 'none',
        'Kitchen': 'pot',
        'Pantry': 'spices',
        'Dining Room': 'spoon',
        'Front Yard': 'mushrooms',
        'Veggie Garden': 'veggies',
        'Hallway': 'tray',
        'Guest Bedroom': 'none'
    }

    you_are_here = 'Living Room' # Initialize the player's starting location
    basket = [] # This is the player's inventory
    necessary_items = ['mushrooms', 'veggies', 'pot', 'spices', 'spoon', 'tray'] # These are all the items necessary to win the game

    print('You are in the {}.\n'.format(you_are_here))

    player_status = [you_are_here, basket]

    win_condition = True

    while sorted(basket) != sorted(necessary_items):
        # The game will run until either the player enters the guest bedroom prematurely,
        # or gathers all necessary items.

        if (room_items[player_status[0]] != 'none') and (room_items[player_status[0]] not in basket):
            print('You see: {}'.format(room_items[player_status[0]]))
        player_status = action(player_status[0], room_dir, player_status[1], necessary_items)
        
        # The player loses if they enter the guest bedroom before they acquire all the necessary items
        if player_status[0] == 'Guest Bedroom':
            win_condition = False
            break
        
        print('You are in the {}.'.format(player_status[0]))
        print('Inventory: ', player_status[1], '\n')
    
    if win_condition == False:
        print('\nYou enter the guest bedroom without anything to eat, and your guest is so hangry that they EAT YOU!\n\n*** YOU LOSE *** GAME OVER ***\n\n')
    else:
        print('Congratulations! You gather all the ingredients to make and serve a delicious mushroom stew to your hangry guest.\n\n*** YOU WIN *** GAME OVER ***\n\n')

if __name__ == "__main__":
    main()