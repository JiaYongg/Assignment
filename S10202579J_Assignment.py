#Poh Jia Yong P09 S10202579J

from random import randint
import json
import sys


# +-------------------------------------------------------------
# | Default stats stored in dictionary for hero,enemies and boss
# +-------------------------------------------------------------
hero = {
    "name": "The Hero",
    "min_damage": 2,
    "max_damage": 4,
    "hp": 20,
    "max_hp": 20,
    "defence": 1,
    "position": [0, 0],
    "orb": False,
    "gold": 0
}

enemy = {
    "name":"Small Rat",
    "min_damage": 1,
    "max_damage": 3,
    "defence": 1,
    "hp": 10,
    "gold": 3
}

enemy2 = {
    "name":"Medium Rat",
    "min_damage": 1,
    "max_damage": 3,
    "defence": 1,
    "hp": 15,
    "gold": 4
}

enemy3 = {
    "name":"Large Rat",
    "min_damage": 1,
    "max_damage": 3,
    "defence": 1,
    "hp": 15,
    "gold": 5
}

boss = {
    "name":"Rat King",
    "min_damage": 8,
    "max_damage": 12,
    "defence": 5,
    "hp": 25
}
# +------------------------
# | Text for various menus 
# +------------------------
main_text = ["New Game",\
             "Resume Game",\
             "View Leaderboard",\
             "Exit Game"]

town_text = ["View Character",\
             "View Map",\
             "View Shop",\
             "Move",\
             "Rest",\
             "Save Game",\
             "Exit Game"]

open_text = ["View Character",\
             "View Map",\
             "Move",\
             "Sense Orb",\
             "Exit Game"]

fight_text = ["Attack",\
              "Run"]


# +-----------------------
# | Game map, day and orb
# +-----------------------
world_map = [['T', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],\
             [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'K']]
current_day = 1
orb = [0, 0]
name = ""
# +----------------------------------------
# | Functions that print menus and messages
# +----------------------------------------

def print_welcome():
    print("Welcome to Ratventure!")
    print("----------------------")

# Prints the input menu based on the user's choice
def print_menu(menu):
    choice = -1
    for x in range(len(menu)):
        print("{}) {}".format(x+1,menu[x]))
    print()
    try:
        choice = int(input("Enter choice: "))
        if choice < 1 or choice > len(menu):
            raise ValueError() #Throws manual exception to be caught
    except ValueError:
        print("Enter numeric values within the options only.")
        return print_menu(menu)
    return choice

# This function prints the map base on the world_map list and the hero position
def print_map():

    position = hero["position"]
    x_coordinate = position[0]
    y_coordinate = position[1]

    for x in range(8):
        print("+---"*8 + "+")
        for y in range(8):
            legend = "   "
            if world_map[x][y] == 'T':
                legend = " T "
                if x == x_coordinate and y == y_coordinate:
                    legend = "H/T"
            elif world_map[x][y] == "K":
                legend = " K "
                if x == x_coordinate and y == y_coordinate:
                    legend = "H/K"
            else:
                if x == x_coordinate and y == y_coordinate:
                    legend = " H "
            print("|{}".format(legend), end="")
        print("|")
    print("+---"*8 + "+")

#Prints the current day and location of Hero
def print_day():
    tile = get_hero_position()
    location = ""
    if tile == "T":
        location = "You are in a town."
    elif tile == " ":
        location = "You are out in the open."
    print("Day {}: {}".format(current_day,location))

#Randomize the 4 other town every new game
def random_town():
    global world_map,town_coordinates
    count = 0 
    total = 0
    town_coordinates = [[0,0]]
    while True:
        x = randint(0, 7)
        y = randint(0, 7)
        random_coordinates = [x, y] #random coordinate every iteration for each town
        tile = world_map[x][y] #set the tile to a random x,y coordinate

        if tile == " ":
            to_add = True
            for i in town_coordinates:
                town_x = i[0]
                town_y = i[1]
                total = abs(town_y - y) + abs(town_x - x)
                if total < 3: 
                    to_add = False
                    break
            if to_add:
                world_map[x][y] = "T"
                count += 1 
                town_coordinates.append(random_coordinates)
                if count == 4:
                    break
        
#Prints shop, only accessible in towns
def print_shop():
    print()
    print("----------------------T O W N  S H O P--------------------------")
    print("----------------------------------------------------------------")
    print("1) Heart(+) , Increases Hero's Max HP by 5. Cost:15 gold")
    print("2) Infinity Sword, Increases Hero's damage by 3. Cost:20 gold")
    print("3) Kite Shield, Increases Hero's defence by 3. Cost:25 gold")
    print("----------------------------------------------------------------")
    print("4) Return to town menu")
    print()
    print("Gold:{}".format(hero["gold"]))
    try:
        buy_choice = int(input("Enter choice : "))

        if buy_choice == 1:
            if hero["gold"] >= 15:
                hero["gold"] -= 15
                hero["max_hp"] += 5
                print("Heart(+) purchased! Your Max HP is now {}".format(hero["max_hp"]))
            else:
                print("Insufficient gold.")
                print_shop()
        elif buy_choice == 2:
            if hero["gold"] >= 20:
                hero["gold"] -= 20
                hero["min_damage"] += 3
                hero["max_damage"] += 3
                print("Infinity Sword purchased! Your total damage is now {}-{}".format(hero["min_damage"],hero["max_damage"]))
            else:
                print("Insufficient gold.")
                print_shop()
        elif buy_choice == 3:
            if hero["gold"] >= 25:
                hero["gold"] -= 25
                hero["defence"] += 3
                print("Kite Shield purchased! Your total defence is now {}".format(hero["defence"]))
            else:
                print("Insufficient gold.")
                print_shop()
        elif buy_choice == 4:
            return
        else:
            print("Enter numbers within the options only")
            print_shop()
    except ValueError:
        print("Enter numeric values within the options only.")
        print_shop()
# +--------------------------
# | Functions related to Hero 
# +--------------------------

#Prints the player combat status
def print_hero_stats():
    print(hero["name"])
    name_length = len(hero["name"])
    print("{:>{}}: {}".format("Gold", name_length, hero["gold"]))
    print("{:>{}}: {}-{}".format("Damage", name_length, hero["min_damage"], hero["max_damage"]))
    print("{:>{}}: {}".format("Defence", name_length, hero["defence"]))
    print("{:>{}}: {}".format("HP", name_length, hero["hp"]))
    if hero["orb"] == True:
        print("You are holding the Orb of Power.")
    print()

#Returns the hero's position in x,y coordinates
def get_hero_position():
    position = hero["position"]
    x_coordinate = position[0]
    y_coordinate = position[1]
    tile = world_map[x_coordinate][y_coordinate]
    return tile

#Set hero position according to x and y coordinates
def set_hero_position(x=None, y=None):
    position = hero["position"]
    x_coordinate = position[0]
    y_coordinate = position[1]
    if y != None:
        y_coordinate += y
        if y_coordinate < 0 or y_coordinate > 7:
            print("Not able to move out of map!")
            return False
    if x != None:
        x_coordinate += x
        if x_coordinate < 0 or x_coordinate > 7:
            print("Not able to move out of map!")
            return False
    #Save updated position
    position[0] = x_coordinate
    position[1] = y_coordinate
    hero["position"] = position 
    return True

#Move hero based on user's input
def move_hero():
    print()
    print_map()
    print("W = up; A = left; S = down; D = right")

    while True: 
        move = input("Your move: ").lower()
        if move == "w":
            status = set_hero_position(x=-1) 
            if status == False:
                continue
            break
        elif move == "a":
            status = set_hero_position(y=-1)
            if status == False:
                continue
            break
        elif move == "s":
            status = set_hero_position(x=1)
            if status == False:
                continue
            break
        elif move == "d":
            status = set_hero_position(y=1)
            if status == False:
                continue
            break
        elif move == "tele":
            x = int(input("Enter X: "))
            y = int(input("Enter Y: "))

            status = set_hero_position(x, y)
            if status == False:
                continue
            break
        else:
            print("Input out of range")
    print_map()

#Restore hero's HP back to maximum
def rest_hero():
    hero["hp"] = hero["max_hp"]
    print("You are fully healed.")

# +--------------------------------
# | Functions relating to game file
# +--------------------------------
def new_game():
    global current_day, hero
    current_day = 1
    random_town()
    spawn_orb()

    hero = {
    "name": "The Hero",
    "min_damage": 2,
    "max_damage": 4,
    "hp": 20,
    "max_hp":20,
    "defence": 1,
    "position": [0, 0],
    "orb": False,
    "gold": 0
    }    

def load_game():
    try:
        global hero, world_map, current_day, orb
        file = open("./save.json", mode = "r")
        load_data = json.load(file)
        hero = load_data["hero"]
        world_map = load_data["world_map"]
        current_day = load_data["current_day"]
        orb = load_data["orb"]
        file.close()
    except FileNotFoundError:
        print("Existing file does not exist.")
        print()
        main()

def save_game():
    file = open("./save.json",mode = "w+")
    file.write(json.dumps({"hero": hero, "world_map": world_map, "current_day": current_day, "orb": orb}))
    file.close()
    print("Game saved.")

def leaderboard_elem(elem):
    return int(elem.split("|")[1])

#After Rat King defeated, prompt user to enter name to save it in leaderboard to see if the user's current day beats the top 5 players.
def save_leaderboard():
    global name
    file = open("./leaderboard.txt",mode = "r")
    leaderboard = file.read()
    file.close()
    leaderboardlist = leaderboard.split("\n")
    leaderboardlist = leaderboardlist[:-1]
    leaderboardlist.append(name + "|" + str(current_day))
    sorted_list = sorted(leaderboardlist,key=leaderboard_elem)
    file = open("./leaderboard.txt",mode = "r+")
    for i in range(5):
        file.write(sorted_list[i] + "\n")
    file.close()

def view_leaderboard():
    file = open("./leaderboard.txt", mode = "r")
    leaderboard = file.read()
    leaderboardlist = leaderboard.split("\n")
    print("Top 5 players on the leaderboard")
    print()
    for i in range(5):
        print("Number {} placing:{} Days taken".format(i+1,leaderboardlist[i]))

    file.close()
    


# +-----------------------------
# | Functions relating to combat
# +-----------------------------

#Prints Small Rat combat status
def print_enemy_stats():
    print("Encounter! - {}".format(enemy["name"]))
    print("Damage: {}-{}".format(enemy["min_damage"], enemy["max_damage"]))
    print("Defence:{:>3}".format(enemy["defence"]))
    print("HP: {}".format(enemy["hp"]))

#Prints Medium Rat combat status
def print_enemy2_stats():
    print("Encounter! - {}".format(enemy2["name"]))
    print("Damage: {}-{}".format(enemy2["min_damage"], enemy2["max_damage"]))
    print("Defence:{:>3}".format(enemy2["defence"]))
    print("HP: {}".format(enemy2["hp"]))

#Prints Large Rat combat status
def print_enemy3_stats():
    print("Encounter! - {}".format(enemy3["name"]))
    print("Damage: {}-{}".format(enemy3["min_damage"], enemy3["max_damage"]))
    print("Defence:{:>3}".format(enemy3["defence"]))
    print("HP: {}".format(enemy3["hp"]))

#Prints Rat King combat status
def print_boss_stats():
    print("Encounter! - {}".format(boss["name"]))
    print("Damage: {}-{}".format(boss["min_damage"], boss["max_damage"]))
    print("Defence:{:>3}".format(boss["defence"]))
    print("HP: {}".format(boss["hp"]))

#One round of attack with Small Rat
def attack():


    hero_damage = randint(hero["min_damage"],hero["max_damage"]) 
    enemy_damage = randint(enemy["min_damage"],enemy["max_damage"]) 

    hero_total_damage = hero_damage - enemy["defence"]
    enemy_total_damage = enemy_damage - hero["defence"]

    if enemy_total_damage <= 0:
        enemy_total_damage = 0

    enemy["hp"] = enemy["hp"] - hero_total_damage
    hero["hp"] = hero["hp"] - enemy_total_damage
    

    print("You deal {} damage to the {}".format(hero_total_damage, enemy["name"]))
    print("Ouch! The {} hit you for {} damage".format(enemy["name"], enemy_total_damage))

    if hero["hp"] <= 0:
        print("You ran out of HP! Game over.")
        sys.exit(0)
    
    print("You have {} HP left.".format(hero["hp"]))

    if enemy["hp"] <= 0:
        print("The {} is dead! You are victorious!".format(enemy["name"]))

#One round of attack with Medium Rat
def attack2():
    
    hero_damage = randint(hero["min_damage"],hero["max_damage"]) 
    enemy2_damage = randint(enemy2["min_damage"],enemy2["max_damage"]) 

    hero_total_damage = hero_damage - enemy2["defence"]
    enemy2_total_damage = enemy2_damage - hero["defence"]

    if enemy2_total_damage <= 0:
        enemy2_total_damage = 0

    enemy2["hp"] = enemy2["hp"] - hero_total_damage
    hero["hp"] = hero["hp"] - enemy2_total_damage
    

    print("You deal {} damage to the {}".format(hero_total_damage, enemy2["name"]))
    print("Ouch! The {} hit you for {} damage".format(enemy2["name"], enemy2_total_damage))

    if hero["hp"] <= 0:
        print("You ran out of HP! Game over.")
        sys.exit(0)
    
    print("You have {} HP left.".format(hero["hp"]))

    if enemy2["hp"] <= 0:
        print("The {} is dead! You are victorious!".format(enemy2["name"]))

#One round of attack with Large Rat
def attack3():
    
    hero_damage = randint(hero["min_damage"],hero["max_damage"]) 
    enemy3_damage = randint(enemy3["min_damage"],enemy3["max_damage"]) 

    hero_total_damage = hero_damage - enemy3["defence"]
    enemy3_total_damage = enemy3_damage - hero["defence"]

    if enemy3_total_damage <= 0:
        enemy3_total_damage = 0

    enemy3["hp"] = enemy3["hp"] - hero_total_damage
    hero["hp"] = hero["hp"] - enemy3_total_damage
    

    print("You deal {} damage to the {}".format(hero_total_damage, enemy3["name"]))
    print("Ouch! The {} hit you for {} damage".format(enemy3["name"], enemy3_total_damage))

    if hero["hp"] <= 0:
        print("You ran out of HP! Game over.")
        sys.exit(0)
    
    print("You have {} HP left.".format(hero["hp"]))

    if enemy3["hp"] <= 0:
        print("The {} is dead! You are victorious!".format(enemy3["name"]))

#One round of boss attack, check if hero has orb
def boss_attack():
    global name

    if hero["orb"] == True:
        hero_damage = randint(hero["min_damage"],hero["max_damage"]) 
        hero_total_damage = hero_damage - boss["defence"]
        boss["hp"] = boss["hp"] - hero_total_damage
    else:
        print("You do not have the Orb of Power - the {} is immune!".format(boss["name"]))
        print("You deal 0 damage to the {}".format(boss["name"]))

    boss_damage = randint(boss["min_damage"],boss["max_damage"]) 
    boss_total_damage = boss_damage - hero["defence"]
    hero["hp"] = hero["hp"] - boss_total_damage
    print("Ouch! The {} hit you for {} damage".format(boss["name"], boss_total_damage))

    if hero["hp"] <= 0:
        print("You ran out of HP! Game over.")
        sys.exit(0)
    
    print("You have {} HP left.".format(hero["hp"]))

    if boss["hp"] <= 0:
        print("The {} is dead! You are victorious!".format(boss["name"]))
        print("Congratulations, you have defeated the {}!".format(boss["name"]))
        print("The world is saved! You win!")

        name = input("Enter name to save into leaderboard: ")
        save_leaderboard()

        sys.exit(0)


#Encounter Small Rat when moving or when player does anything else other than moving after running from Small Rat   
def encounter():
    print_enemy_stats()
    encounter_choice = print_menu(fight_text)
    global current_day, world_map
    
    if encounter_choice == 1:
        attack()
        if enemy["hp"] <= 0:
            position = hero["position"]
            hero["gold"] += enemy["gold"]
            return
        encounter()

    if encounter_choice == 2:
        print("You run and hide.")
        enemy["hp"] = 10
        open_choice = print_menu(open_text)

        if open_choice == 1 or open_choice == 2 or open_choice == 4:

            encounter()
        elif open_choice == 3:
            move_hero()
            enemy["hp"] = 10
            current_day += 1
        elif open_choice == 5:
            sys.exit(0) 

#Encounter Medium Rat when moving or when player does anything else other than moving after running from Medium Rat   
def encounter2():
    print_enemy2_stats()
    encounter_choice = print_menu(fight_text)
    global current_day, world_map

    if encounter_choice == 1:
        attack2()
        if enemy2["hp"] <= 0:
            position = hero["position"]
            hero["gold"] += enemy2["gold"]
            return
        encounter2()

    if encounter_choice == 2:
        print("You run and hide.")
        enemy2["hp"] = 15
        open_choice = print_menu(open_text)

        if open_choice == 1 or open_choice == 2 or open_choice == 4:
            encounter2()
        elif open_choice == 3:
            move_hero()
            enemy2["hp"] = 15
            current_day += 1
        elif open_choice == 5:
            sys.exit(0) 

#Encounter Large Rat when moving or when player does anything else other than moving after running from Large
def encounter3():
    print_enemy3_stats()
    encounter_choice = print_menu(fight_text)
    global current_day, world_map

    if encounter_choice == 1:
        attack3()
        if enemy3["hp"] <= 0:
            position = hero["position"]
            hero["gold"] += enemy3["gold"]
            return
        encounter3()

    if encounter_choice == 2:
        print("You run and hide.")
        enemy3["hp"] = 15
        open_choice = print_menu(open_text)

        if open_choice == 1 or open_choice == 2 or open_choice == 4:
            encounter3()
        elif open_choice == 3:
            move_hero()
            enemy3["hp"] = 15
            current_day += 1
        elif open_choice == 5:
            sys.exit(0) 

#Encounter Rat King when moving or when player does anything else other than moving after running from Rat King
def boss_encounter():
    print_boss_stats()
    encounter_choice = print_menu(fight_text)
    global current_day, world_map

    if encounter_choice == 1:
        boss_attack()
        boss_encounter()

    if encounter_choice == 2:
        print("You run and hide.")
        boss["hp"] = 25
        open_choice = print_menu(open_text)

        if open_choice == 1 or open_choice == 2 or open_choice == 4:
            boss_encounter()
        elif open_choice == 3:
            move_hero()
            boss["hp"] = 25
            current_day += 1
        elif open_choice == 5:
            sys.exit(0) 


# +--------------------------
# | Functions relating to orb
# +--------------------------

#Spawns orb at a random location everytime it is a new game
def spawn_orb():
    global orb

    x = randint(0, 7)
    
    if x >= 4:
        y = randint(0,7)
    else:
        y = randint(4,7)

    tile = world_map[x][y]

    if tile == " ":
        orb = [x,y]
    else:
        spawn_orb()
    print("Orb:", orb)
#Sense orb location and track the direction of the orb
def sense_orb():
    
    hero_position = hero["position"] 
    orb_position = orb

    if hero_position == orb_position:
        hero["min_damage"] += 5
        hero["max_damage"] += 5
        hero["defence"] += 5
        hero["orb"] = True

        print("You found the Orb of Power!")
        print("Your attack increases by 5!")
        print("Your defence increases by 5!")
        return

    orb_direction = ""
    x_difference = hero_position[1] - orb_position[1]
    y_difference = hero_position[0] - orb_position[0]

    if x_difference == 0 and y_difference > 0:
        orb_direction = "north"
    elif x_difference < 0 and y_difference > 0:
        orb_direction = "northeast"
    elif x_difference < 0 and y_difference == 0:
        orb_direction = "east"
    elif x_difference < 0 and y_difference < 0:
        orb_direction = "southeast" 
    elif x_difference == 0 and y_difference < 0:
        orb_direction = "south"
    elif x_difference > 0 and y_difference < 0:
        orb_direction = "southwest"
    elif x_difference > 0 and y_difference == 0:
        orb_direction = "west"
    elif x_difference > 0 and y_difference > 0:
        orb_direction = "northwest"

    print("You sense that the Orb of Power is to the {}".format(orb_direction))
        
# +--------------
# | Main function
# +--------------

def main():
    global current_day
    print_welcome() 
    choice = print_menu(main_text)
    if choice == 1:
        new_game()
    elif choice == 2:
        load_game()
    elif choice == 3:
        view_leaderboard()
        main()
    elif choice == 4:
        sys.exit(0)

    while True: #Get user input until game end
        print_day()
        position = get_hero_position() #Check hero's current tile
        if position == "T":
            choice = print_menu(town_text)
            
            if choice == 1:
                print_hero_stats()
            elif choice == 2:
                print_map()
            elif choice == 3:
                print_shop()
            elif choice == 4:
                move_hero()
                current_day += 1
            elif choice == 5:
                rest_hero()
                current_day += 1
            elif choice == 6:
                save_game()
            elif choice == 7:
                sys.exit(0)

            if current_day % 10 == 0:
                enemy["min_damage"] += 1
                enemy["max_damage"] += 1
                enemy2["min_damage"] += 1
                enemy2["max_damage"] += 1
                enemy3["min_damage"] += 1
                enemy3["max_damage"] += 1

        elif position == " ":
                if enemy["hp"] <= 0 or enemy2["hp"] <= 0 or enemy3["hp"] <= 0:
                    choice = print_menu(open_text)

                    if choice == 1:
                        print_hero_stats()
                    elif choice == 2:
                        print_map()
                    elif choice == 3:
                        move_hero()
                        enemy["hp"] = 10
                        enemy2["hp"] = 15
                        enemy3["hp"] = 15
                        current_day += 1
                    elif choice == 4:                  
                        if hero["orb"] == False:
                            sense_orb()
                            current_day +=1
                        elif hero["orb"] == True:
                            print("You have already obtained the Orb of Power!")
                    elif choice == 5:
                        sys.exit(0)
                    if current_day % 10 == 0:
                        enemy["min_damage"] += 1
                        enemy["max_damage"] += 1
                        enemy2["min_damage"] += 1
                        enemy2["max_damage"] += 1
                        enemy3["min_damage"] += 1
                        enemy3["max_damage"] += 1
            
                else:
                    rand_encounter = randint(1, 3)
                    if rand_encounter == 1:
                        if enemy["hp"] > 0:
                            encounter()
                            
                    elif rand_encounter == 2:
                        if enemy2["hp"] > 0:
                            encounter2()
                            
                    elif rand_encounter == 3:
                        if enemy3["hp"] > 0:
                            encounter3()
                 
        elif position == "K":
            boss_encounter()

if __name__ == "__main__":
    main()
