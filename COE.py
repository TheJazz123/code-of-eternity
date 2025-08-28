'''
dev notes
complete afaik
'''

import os, pickle, re, subprocess, threading, time
from datetime import timedelta
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from termcolor import colored
import pygame,colorama
from data import realms,items,realm_transitions

def effect(sound):
    fileloc='music\\' + sound
    pygame.mixer.Sound(fileloc).play()

#bgm
def play():
    fileloc='music\\'+game_state['music']
    while not music_thread_stop:
        if fileloc:
            pygame.mixer.music.load(fileloc)
            pygame.mixer.music.play(-1)  
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def change_music(file):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(1000) 
        pygame.time.wait(1000)  
    game_state['music'] = file
    fileloc='music\\'+game_state['music']
    pygame.time.wait(100)  
    pygame.mixer.music.load(fileloc)
    pygame.mixer.music.play(-1)  

#stats display
def stat():
    time_played = timedelta(seconds=statistics["time_played"])

    print("Game Statistics:")
    print(f"Time Played: {time_played} (hh:mm:ss)")
    print(f"Percentage Completed: {statistics['percentage_completed']}%")
    print("\nAchievements:")
    if statistics['achievements']:
        for achievement in statistics['achievements']:
            print(f" - {achievement}")
    else:
        print(" - No achievements yet.")
    
    print("\nQuests Completed:")
    if statistics['quests_completed']:
        for quest in statistics['quests_completed']:
            print(f" - {quest}")
    else:
        print(" - No quests completed yet.")

def statupdater():
    statistics["time_played"] += int(time.time()-start_time)
    playerloc=0
    for i in game_state['visited_locations'].values():
        playerloc += len(i)
    playerachieve = len(statistics['achievements'])
    gameloc = sum(len(realm['locations']) for realm in realms.values())
    gameachieve = 10
    statistics["percentage_completed"] = ((playerloc + playerachieve) * 100) // (gameloc + gameachieve)
    
#clear
def clear():
    print("\033c", end="")

# saving
def save_game():
    with open("savegame.bin", 'wb') as file:
        pickle.dump(game_state, file)
    with open("statistics.bin", 'wb') as file:
        pickle.dump(statistics, file)
    print("Game saved successfully!")

# loading
def load_game():
    global game_state,statistics
    try:
        with open("savegame.bin", 'rb') as file:
            game_state = pickle.load(file)
        with open("statistics.bin",'rb') as file:
            statistics = pickle.load(file) 
        print("Game loaded successfully!")
    except FileNotFoundError:
        input("No saved game found.")
        effect('feedback.mp3')
        clear()
        new_intro()
    except pickle.UnpicklingError:
        print("Error reading the saved game file.")

#image
def img_open(file_name):
    input('You get a vision in your head.')
    effect('feedback.mp3')
    img = 'logicgate\\'+file_name
    os.startfile(img)
    
#close image
def close():
    subprocess.run(['taskkill', '/IM', 'Photos.exe', '/F'], stdout=subprocess.DEVNULL,)

#start
def main_menu():
    while True:
        choice = input('''Main Menu\n1. Start New Game\n2. Load Game\n\n> ''').strip()
        effect('feedback.mp3')
        if choice == '2':
            load_game()
            break
            
        elif choice == '1':
            input(f"Starting a {colored('new game','magenta')}...")
            effect('feedback.mp3')
            clear()
            new_intro()
            break
        else:
            print(f"{colored('Invalid', 'red')} choice.")

#map
def display_map():
    clear()
    map_size = 5
    half_size = map_size // 2
    realm_data = realms[game_state['current_realm']]
    map_width = (map_size * 2) - 1  
    print(colored(realm_data['name'],'green').center(map_width))
    for y in range(half_size, -half_size - 1, -1):
        row = []
        for x in range(-half_size, half_size + 1):
            location_symbol = "."
            for loc, data in realm_data['locations'].items():
                if data['coords'] == (x, y):
                    location_symbol = "O"  
                if game_state['current_location'] == loc and data['coords'] == (x, y):
                    location_symbol = "X"  
            row.append(location_symbol)
        print(" ".join(row))
    width = (map_size) * 2
    print(colored(game_state['current_location'].title().center(width),'yellow'))

def colorize_match(match):
    word = match.group(0)
    return colored(word, color_words.get(word,'white')) 

def display_dialogue(file_name):
    with open('dialogues\\'+file_name) as f:
        lines = f.readlines()
    for line in lines:
        colored_line = pattern.sub(colorize_match, line)
        for character in colored_line:
            print(character, end='', flush=True)
            time.sleep(0.01)
        time.sleep(0.05)

def display_inv():
    if game_state['inventory']:
            print("You have:")
            for item in game_state['inventory']:
                print(f"- {item.title()}")
    else:
        print("Your inventory is empty.")

def look_at(item_name):
    if item_name in realms[game_state['current_realm']]['locations'][game_state['current_location']]['items'] or item_name in game_state['inventory']:
            if item_name in items:
                print(items[item_name])
            else:
                print(f"You see the {item_name}, but there's nothing special about it.")
    else:
        print(f"You don't see any {item_name} here.")

def first_visit():
    clear()
    if game_state['current_location']=='garden':
        display_dialogue('8quirk1.txt')
        input()
        effect('feedback.mp3')
        clear()
    elif game_state['current_location']=='hall':
        change_music('ominous.mp3')
        display_dialogue('21ciphprompt.txt')
        riddleanswer=input('Enter your answer here: ')
        effect('feedback.mp3')
        if riddleanswer.lower().strip()=='silence':
            print(f"???: You pass, yet you fail. The {colored('silence is broken','red')}.")
        else:
            game_state['health']-=1
            input(f"Your current HP: {game_state['health']}/10")
            effect('feedback.mp3')
            print("???: As expected. Thou art not worthy of going any further.")
        if game_state['health']==0:
            return
        display_dialogue('9hallevent1.txt')
        input()
        effect('feedback.mp3')
        print(colored(open('dialogues\\11bug.txt').read()*3,'green'))
        input()
        effect('feedback.mp3')
        clear()
        display_dialogue('10hallevent2.txt')
        input()
        effect('feedback.mp3')
        change_music('idle.mp3')
        clear()
    elif game_state['current_location']=='code fountain':
        display_dialogue('22otto.txt')
        game_state['inventory'].append('ottos shop')
        input(f"{colored('Ottos Shop','blue')} added to inventory.")
        effect('feedback.mp3')
        clear()
    elif game_state['current_location']=='cryptic cave':
        input("You sense a strange power resonating through the air.")  
        effect('feedback.mp3')
    elif game_state['current_location']=='loop labyrinth':
        if 'challengers orb' in game_state['inventory']:
            print("This must be the gate this orb is resonating to.")
        else:
            print("Woah... What\'s this huge gate here for?")
    game_state['visited_locations'][game_state['current_realm']].append(game_state['current_location'])
    if game_state['visited_locations'][game_state['current_realm']]==len(realms[game_state['current_realm']]['locations']):
        effect('achieve.mp3')
        input("Achievement 'Explorer' Unlocked.")
        statistics['achievements'].append('Explorer')
        clear()
        

def move(direction):
    if direction in realms[game_state['current_realm']]['locations'][game_state['current_location']]['exits']:
        game_state['current_location'] = realms[game_state['current_realm']]['locations'][game_state['current_location']]['exits'][direction]
        if not game_state['tut']:
            if game_state['current_location'] not in game_state['visited_locations'][game_state['current_realm']]:
                first_visit()
            display_map()
        print(realms[game_state['current_realm']]['locations'][game_state['current_location']]['description'])
    else:
        print(f"You can't go {direction} from here.")

def look_around():
    print(realms[game_state['current_realm']]['locations'][game_state['current_location']]['description'])
    if realms[game_state['current_realm']]['locations'][game_state['current_location']]['items']:
        print("\nYou see the following items:")
        for item in realms[game_state['current_realm']]['locations'][game_state['current_location']]['items']:
            print("-", item)
    else:
        print("There doesn't seem to be anything of interest here.")

def spec_pick(item):
    if item=='a coding tome':
        clear()
        display_dialogue('12codingtome.txt')
    elif item=='a mysterious key':
        clear()
        display_dialogue('17mystkey.txt')
        statistics['quests_completed'].append(game_state['quests'].pop(game_state['quests'].index('Unlock Hall')))
        print(f"Quest Completed: {colored('Unlock Hall','green')}.")
    elif item=='cipheras note':
        print("Byte: Strange... a note.")
    elif item=='debug' and game_state['current_location']=='hall':
        print('dev notes: if youre not sure on what you picked up, try- \'look at [item]\' to get a description. ')
    elif item=='challengers orb':
        clear()
        change_music('puzzlebgm.mp3')
        display_dialogue('23glitch.txt')
        rid1 = input('''Rearrange the given sentence:
sensitive ... Encryption ...  pivotal ... information. ... in safeguarding ... role ... plays a 

Enter your answer: ''')
        effect('feedback.mp3')
        while rid1.lower() != 'encryption plays a pivotal role in safeguarding sensitive information.':
            game_state['health']-=1
            if game_state['health']==0:
                return
            input(f"Your current HP: {colored(str(game_state['health'])+'/10','red')}")
            effect('feedback.mp3')
            rid1=input('''\nIncorrect. The glitch expands.
Enter your answer: ''')
            effect('feedback.mp3')
        game_state['coins']+=400
        display_dialogue('18glitchfix.txt')
        input()
        effect('feedback.mp3')
        change_music('idle.mp3')
        clear() 

def pick(item_name):
    matching_items = []   
    for item in realms[game_state['current_realm']]['locations'][game_state['current_location']]['items']:
        if item_name in item:
            matching_items.append(item)
    if len(matching_items) == 1:
        item = matching_items[0]
        game_state['inventory'].append(item)
        spec_pick(item)
        realms[game_state['current_realm']]['locations'][game_state['current_location']]['items'].remove(matching_items[0])
        input(f"You picked up {matching_items[0]}!")
        effect('feedback.mp3')
        if game_state['tut']:
            print(f"\nAlgo: Nicely done! You've picked up {matching_items[0]}. It's in your inventory now.")
            game_state['inventory'].remove('bag')
        else:
            clear()
    elif len(matching_items) > 1:                         
            print("Multiple items match your description:")
            for match in matching_items:
                print(f"- {match}")
            print("Please be more specific.")
    else:
        print(f"There doesn't seem to be a '{item_name}' here.")

def trans_gate():
    if not current_location_data['guardian challenge']['completed']:
        for text in current_location_data['guardian challenge']['intro']:
            input(text)
            effect('feedback.mp3')
        clear()
        print(current_location_data['guardian challenge']['challenge'])
        youranswer=input("Enter your answer: ")
        effect('feedback.mp3')
        if youranswer.lower().strip() in current_location_data['guardian challenge']['answer']:
            current_location_data['guardian challenge']['completed']=True
            input(current_location_data['guardian challenge']['victory'])
            effect('feedback.mp3')
            clear()
            effect('achieve.mp3')
            input(colored("\n"*15+f"{realms[game_state['current_realm']]['name'].upper()}".center(100) +"\n" + "SUCCESSFULLY CLEARED".center(100),'green',attrs=['bold']))
            effect('feedback.mp3')
            game_state['current_realm']=realm_transitions[game_state['current_location']]['realm']
            game_state['current_location']=realm_transitions[game_state['current_location']]['enter']
            print(realms[game_state['current_realm']]['locations'][game_state['current_location']]['description'])
            game_state['visited_locations'][game_state['current_realm']].append(game_state['current_location'])
        else:
            game_state['health']-=1
            input(current_location_data['guardian challenge']['defeat']+f"\nYour current HP: {game_state['health']}/10")
            effect('feedback.mp3')
            clear()
    else:
        game_state['current_realm']=realm_transitions[game_state['current_location']]['realm']
        game_state['current_location']=realm_transitions[game_state['current_location']]['enter']
        print(realms[game_state['current_realm']]['locations'][game_state['current_location']]['description'])

def useinv():
    index=0
    for index,item in enumerate(game_state['inventory'],1):
        print(f'{index}. {item.title()}')
    print(f'{index+1}. Exit')
    choice2 = input("Enter Item Number: ")
    effect('feedback.mp3')
    if choice2.isdigit() and 1 <= int(choice2) <= len(game_state['inventory']):
        item_name = game_state['inventory'][int(choice2) - 1]
    elif choice2.isdigit() and int(choice2)==index+1:
        clear()
        return
    else:
        print(f"{colored('Invalid', 'red')} number.")
        return
    use(item_name)

def uniteleport():
    clear()
    for index,realm in enumerate(realms,1):
        print(f'{index}. {realm.title()}')
    choice = input('\nEnter Realm Number: ')
    effect('feedback.mp3')
    if choice.isdigit() and 1 <= int(choice) <= len(realms):
        selected_realm = list(realms.keys())[int(choice) - 1]

    if game_state['visited_locations'][selected_realm]:
        print("Available destinations:")
        for index,location in enumerate(game_state['visited_locations'][selected_realm],1):
            print(f'\t{index}. {location.title()}')
        
        choice1 = input("\nEnter the number of your destination: ")
        effect('feedback.mp3')
        
        # check choice validity
        if choice1.isdigit() and 1 <= int(choice1) <= len(game_state['visited_locations'][selected_realm]):
            selected_location = game_state['visited_locations'][selected_realm][int(choice1) - 1]
            game_state['current_location'] = selected_location
            for realm_name, realm_data in realms.items():
                if game_state['current_location'] in realm_data['locations']:
                    game_state['current_realm'] = realm_name
                    break
            input(f"\nUsing the universal teleporter you are instantly transported to {selected_location}.\n")
            effect('feedback.mp3')
            clear()
            print(realms[game_state['current_realm']]['locations'][game_state['current_location']]['description'])
            return
        else:
            print(f"{colored('Invalid', 'red')} choice!")
            return
    else:
        print("The teleporter doesn't recognize any known locations yet.")
        return
    
def firsttele(destination):
    if destination=='pixel pond':
        input()
        effect('feedback.mp3')
        clear()
        display_dialogue('16mechabot.txt')
        input()
        effect('feedback.mp3')
        clear()
    elif destination=='echo cave':
        clear()
        change_music('puzzlebgm.mp3')
        display_dialogue('26cavelogic.txt')
        img_open('nornand.png')
        while True:
            switch_a = input("\nSet Switch A (0 for OFF, 1 for ON): ")
            effect('feedback.mp3')
            switch_b = input("Set Switch B (0 for OFF, 1 for ON): ")
            effect('feedback.mp3')
            switch_c = input("Set Switch C (0 for OFF, 1 for ON): ")
            effect('feedback.mp3')
            
            if switch_a not in ["0", "1"] or switch_b not in ["0", "1"] or switch_c not in ["0", "1"]:
                input(f"\n{colored('INVALID', 'red')} INPUT. SYSTEM TOOK DAMAGE.")
                effect('feedback.mp3')
                game_state['health']-=1
                if game_state['health']==0:
                    return
                input(f"Your current HP: {colored(str(game_state['health'])+'/10','red')}")
                effect('feedback.mp3')
                continue
            switch_a, switch_b, switch_c = int(switch_a), int(switch_b), int(switch_c)
            nor_output = not(switch_a or switch_b)
            nand_output = not(nor_output and switch_c)
            if nand_output:
                game_state['coins']+=100
                display_dialogue('27caveclear.txt')
                input()
                effect('feedback.mp3')
                break
            else:
                game_state['health']-=1
                input(f"Your current HP: {colored(str(game_state['health'])+'/10','red')}")
                effect('feedback.mp3')
        change_music('idle.mp3')
        close()
    game_state['visited_locations'][game_state['current_realm']].append(destination)

def intrateleport(item_name):
    current_location_data = realms[game_state['current_realm']]['locations'][game_state['current_location']]
    current_realm_name = realms[game_state['current_realm']]['name'].lower()
    
    if item_name != teleport_crystals[current_realm_name]:
        print(f"You can't use the {item_name} in this realm.")
        return
    
    if 'teleport_station' in current_location_data:
        destination = current_location_data['teleport_station']
        
        # Confirmation prompt
        confirmation = input(f"Do you want to use the {item_name} to teleport to the {colored(destination,'green')}? (yes/no): ").lower()
        effect('feedback.mp3')
        if confirmation == "yes":
            print(f"\nUsing the {item_name}, you are transported to the {colored(destination,'green')}.\n")
            if destination not in game_state['visited_locations'][game_state['current_realm']]:
                firsttele(destination)
            game_state['current_location'] = destination
            display_map()
            print(realms[game_state['current_realm']]['locations'][game_state['current_location']]['description'])
            return
        else:
            print("You decided not to teleport.")
            return
    else:
        print(f"You can't use the {item_name} here.")
        return

def use(item_name):
    if item_name == "universal teleporter" and item_name in game_state['inventory']:
        uniteleport()
    elif item_name=='a coding tome' and game_state['current_location']=='garden':
        clear()
        display_dialogue('13quirk2.txt')
        game_state['coins']+=500
        display_dialogue('24keyloc.txt')
        if 'a mysterious key' not in game_state['inventory']:
            input("\nI\'m surprised you don\'t already have it. Not much of the explorer are we?")
            effect('feedback.mp3')
        else:
            display_dialogue('25keyremark.txt')
            input()
            effect('feedback.mp3')
        clear()
        game_state['inventory'].remove(item_name)
        return
    elif item_name=='debug':
        game_state['inventory'].remove(item_name)
        game_state['health']=10
        print("HP Restored.")
        return
    elif item_name=='cipheras note':
        display_dialogue('15cipherasnote.txt')
        input()
        effect('feedback.mp3')
        clear()
        return

    elif item_name=='ottos shop':
        shop()
        return
    elif item_name=='challengers orb':
        input("It deems you worthy of taking on the guardian challenges.") 
        effect('feedback.mp3')

    elif item_name in teleport_crystals.values() and item_name in game_state['inventory']:
        intrateleport(item_name)  
    
    else:
        print(f"You either don't have {item_name} or don't know how to use it.")
def shop():
    if not game_state['shopstock']:
        print("No items currently available. Please visit later.")
        return
    print("Welcome to the Shop!")
    print("-"*40)
    print(f"{'Number':<6} | {'Item':<20} | {'Price':<7}")
    print("-"*40)
    for index, (item, price) in enumerate(game_state['shopstock'].items(), start=1):
        print(f"{index:<6} | {item.title():<20} | ${price:<7}")
    print("-"*40)
    action = input("Enter the item number to purchase, or 'quit' to quit: ").strip().lower()
    if action == 'quit':
        input("Thank you for visiting the shop!")
        effect('feedback.mp3')
        clear()
        return
    elif action.isdigit():
        item_number = int(action)
        item_list = list(game_state['shopstock'].keys())
        if item_number < 1 or item_number > len(item_list):
            print(f"{colored('Invalid', 'red')} item number!")
            return
        item_name = item_list[item_number - 1]
        cost = game_state['shopstock'][item_name]
        if game_state['coins'] < cost:
            input("Insufficient funds!")
            effect('feedback.mp3')
            clear()
            return
        game_state['coins']-=cost
        game_state['shopstock'].pop(item_name)
        game_state['inventory'].append(item_name)
        print(f"Purchased {item_name.capitalize()} for ${cost}.")
        print(f"Your remaining balance: ${game_state['coins']}")
    else:
        print(f"{colored('Invalid', 'red')} option!")

def new_intro():
    start_time=time.time()
    #Title Screen
    print("─"*60+"\n"+colored(' '*20+"Code of Eternity", "red", attrs=["bold"])+"\n"+"─"*60)
    display_dialogue('1intro.txt')
    input()
    effect('feedback.mp3')
    clear()
    display_dialogue('2controls.txt')
    input()
    effect('feedback.mp3')
    display_dialogue('32mapintro.txt')
    input()
    effect('feedback.mp3')
    display_map()
    input()
    effect('feedback.mp3')
    clear()

    #Controls tutorial
    tutorial=input('Do you want a tutorial on the game mechanics(y/n)?: ')
    if tutorial=='y':
        #Moving
        display_dialogue('19introtut.txt')
        while game_state['current_location'] == 'start':
            action = input(f"Try to move by typing '{colored('go south','blue')}': ").lower()
            effect('feedback.mp3')
            try: 
                direction=action.split()[1].strip()
                if action.startswith('go ') and direction=='south':
                    move(direction)
                    print("\nAlgo: Excellent! You're getting the hang of this.")
                else:
                    print(f"Algo: That doesn't seem right. Remember, type '{colored('go south','blue')}'.")
            except:
                print(f"Algo: That doesn't seem right. Remember, type '{colored('go south','blue')}'.")
        input()
        effect('feedback.mp3')
        print(f"\nAlgo: Great! Now, let's head back to the entrance. Use the '{colored('go north','red')}' command.")
        while game_state['current_location'] == 'garden':
            action = input(f"Try to move by typing '{colored('go north','red')}': ").lower()
            effect('feedback.mp3')
            try:
                direction=action.split()[1].strip()
                if action.startswith('go ') and direction=='north':
                    move(direction)
                    print("\nAlgo: Perfect! You've returned to the entrance.")
                else:
                    print(f"Algo: That doesn't seem right. Remember, type '{colored('go north','red')}'.")
            except:
                print(f"Algo: That doesn't seem right. Remember, type '{colored('go north','red')}'.")
        input()
        effect('feedback.mp3')
        clear()

        #Look 
        print(f"\nAlgo: Before you start picking up items,\
        \nit's always a good idea to {colored('look','yellow')} around and understand your surroundings.")
        while True:
            action = input(f"Give the {colored('look','yellow')} command a try: ").lower()
            effect('feedback.mp3')
            if action.strip() == 'look':
                look_around()
                break
            else:
                print(f"Algo: Try again. Just type {colored('look','yellow')} to get a description of where you are and what's around you.")
        input()
        effect('feedback.mp3')

        #Pick
        print("Now that you know how to observe your surroundings, let's try interacting with items.")
        while 'bag' in realms[game_state['current_realm']]['locations']['start']['items']:
            action = input(f"Try picking up an item. For instance, {colored('take bag','red')} will do: ").lower()
            effect('feedback.mp3')
            if action == 'take bag':
                pick('bag')
            else:
                print(f"\nGive it another shot. Just type {colored('take bag','red')}.")
        input()
        effect('feedback.mp3')
        clear()

        #Puzzles
        change_music('puzzlebgm.mp3')
        # Fragmented Memory Reconstruction
        display_dialogue('28puzzle.txt')
        answer = input().strip()
        effect('feedback.mp3')
        if answer.lower() == "byte discovered the secret chamber within scriptoria.":
            print("Algo: Correct! Well done, Byte.")
        else:
            print("Algo: Not quite right. The correct arrangement is: 'Byte discovered the secret chamber within Scriptoria.'")
        input()
        effect('feedback.mp3')
        clear()

        # Logic Gate
        display_dialogue('3logicgatetutorial.txt')
        img_open('and.png')
        
        while True: 
            switch_a = input("Switch A (AND Gate input 1): ")
            effect('feedback.mp3')
            switch_b = input("Switch B (AND Gate input 2): ")
            effect('feedback.mp3')
            if switch_a not in ["0", "1"] or switch_b not in ["0", "1"]:
                print("\nAlgo: Remember, you can only enter 0 (for OFF) or 1 (for ON). Try again.")
                continue
            
            switch_a = int(switch_a)
            switch_b = int(switch_b)

            and_output = switch_a and switch_b
            if and_output:
                print("\nAlgo: Well done! You've activated the AND gate!")
                break
            else:
                print("\nAlgo: Remember, for the AND gate to be true, both its inputs must be ON. Give it another try.")
        close()        
        input()
        effect('feedback.mp3')
        clear()

        #Coding Decipher
        display_dialogue('4codindecipher.txt')
        answer=input()
        effect('feedback.mp3')
        if answer == '120':  # 5 factorial
            print("Algo: Brilliant! That's the spirit.\
            \nThe function you deciphered is a recursive implementation of factorial calculation.")
        else:
            print("Algo: Not quite. The function is actually computing factorials using recursion.\
            \nmystery(5) computes 5 factorial, which is 5 x 4 x 3 x 2 x 1 = 120.")
        input()
        effect('feedback.mp3')
        clear()

        #Narrative Riddle
        display_dialogue('29riddle.txt')
        answer=input()
        effect('feedback.mp3')
        if answer == "code":
            print("Algo: Precisely! You're ready for what lies ahead.")
        else:
            print("Algo: It's at the very heart of every software. The answer is 'code'.")
        input()
        effect('feedback.mp3')
        clear()

    #Villain Encounter
    change_music('ominous.mp3')
    display_dialogue('5villainencounter.txt')
    input()
    effect('feedback.mp3')
    clear()
    display_dialogue('6lockguide.txt')
    img_open('andnor.png')
    #get outta the cocoon
    attempts = 3
    while attempts > 0:
        switch_a = input("\nSet Switch A (0 for OFF, 1 for ON): ")
        effect('feedback.mp3')
        switch_b = input("Set Switch B (0 for OFF, 1 for ON): ")
        effect('feedback.mp3')
        switch_c = input("Set Switch C (0 for OFF, 1 for ON): ")
        effect('feedback.mp3')
        if switch_a not in ["0", "1"] or switch_b not in ["0", "1"] or switch_c not in ["0", "1"]:
            print("\nAlgo: Remember, you can only enter 0 (for OFF) or 1 (for ON).")
            input()
            effect('feedback.mp3')
            continue
        switch_a, switch_b, switch_c = int(switch_a), int(switch_b), int(switch_c)
        and_output = switch_a and switch_b
        or_output = and_output or switch_c
        final_output = not or_output
        if final_output:
            clear()
            display_dialogue('30villaindefeat.txt')
            input()
            effect('feedback.mp3')
            break
        else:
            attempts -= 1
            game_state['health']-=1
            input(f"Your current HP: {game_state['health']}/10")
            effect('feedback.mp3')
            if attempts > 0:
                print(f"\nThe cocoon's walls tighten, and the internal display warns: '{attempts} attempts remaining'.\n\
                      \nAlgo: Think, Byte! We don't have much time.")
    else:
        close()
        clear()
        display_dialogue('31algosave.txt')
        input()
        effect('feedback.mp3')
        clear()
        
    display_dialogue('7algoleaving.txt')
    input()
    effect('feedback.mp3')
    clear()
    game_state['tut']=False
    change_music('idle.mp3')
    statistics['time_played'] += int(time.time()-start_time)
    statistics['achievements'].append('First Steps')
    print(f"Achievement {colored('First Steps','yellow')} Unlocked.")
    effect('achieve.mp3')
    input()
    effect('feedback.mp3')
    clear()

color_words={
    'depths of Scriptoria': 'green',
    'minimap of Scriptoria':'blue',
    'a tutorial':'yellow',
    'Start with movement':'cyan',
    'the entrance':'green',
    'some puzzles':'cyan',
    'AND Gate':'magenta',
    'both inputs are ON':'red',
    'value of mystery':'cyan',
    'trapped':'red',
    'an AND, an OR, and a NOT':'blue',
    'OR Gate':'magenta',
    'at least one input is ON':'green',
    'NOT Gate':'magenta',
    'inverts the input':'yellow',
    'freeing Byte':'green',
    'entity dissipates':'magenta',
    'Be more careful':'red',
    'north is sealed':'red',
    'hidden to the south':'blue',
    'caves':'yellow',
    'Check the map':'green',
    'the key':'magenta',
    'mechabot':'red',
    'a tome': 'cyan',
    'near the ponds': 'yellow',
    '500 coins':'red',
    'teleport crystal nearby':'green',
    'Intruder detected': 'red',
    'Commencing verification': 'yellow',
    'Identity verified':'green',
    'find the tome':'magenta',
    'give this tome to Quirk':'blue',
    'south east of here':'red',
    'use the teleport crystal':'yellow',
    'NOR':'cyan',
    'NAND':'green',
    'GAME OVER':'red',
    'Glitch resolved':'green',
    '100 coins':'yellow',
    'Did he drop something':'magenta',
    'You can now buy from the shop using coins':'green',
    '400 coins':'yellow',
    'use the transition gate':'cyan'
    }

command_aliases = {
    "i": "inventory",
    "l": "look",
    "q": "exit",
    "m": "map",
    "c": "clear",
    "h": "health",
    "s": "save"
}

statistics = {
        "time_played": 0,
        "achievements": [],
        "percentage_completed": 0,
        "quests_completed": []
    }

game_state = {
        "current_realm": 'scriptoria central',
        "current_location": 'start',
        "inventory": [],
        "health": 10,
        "coins": 0,
        "visited_locations": {'scriptoria central':['start'],
                     'recursive realm':[],
                     'binary battlegrounds':[],
                     'variable valleys':[],
                     '':[]},
        "quests": ['Unlock Hall'],
        "realms": realms,
        "tut": True,
        "music": 'idle.mp3',
        "shopstock" : {
        'universal teleporter':1000
           }
    }

teleport_crystals = {
        'scriptoria central': "scriptoria crystal",
        'recursive realm': "recursive crystal",
        'binary battlegrounds': "binary crystal",
        'variable valleys': "variable crystal"
            }

#MAIN GAME
pygame.init()
pygame.mixer.init()
music_thread_stop=False
music_thread = threading.Thread(target=play)
music_thread.daemon = True 
music_thread.start()
colorama.init()
pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in color_words) + r')\b', re.IGNORECASE)
main_menu()

while game_state['health']>0:

    start_time=time.time()

    action = input("What do you want to do? ").lower()
    effect('feedback.mp3')

    if action in command_aliases:
        action = command_aliases[action]

    if action=='help':
        print("\nAvailable Commands:\n" + "-"*20)
        display_dialogue('0help.txt')
    
    elif action=='stat':
        stat()

    elif action=='map':
        display_map()

    elif action=='inventory':
        if game_state['inventory']:
            print("You have:")
            for item in game_state['inventory']:
                print(f"- {item.title()}")
        else:
            print("Your inventory is empty.")

    elif action=='currency':
        print(f"You currently own {colored(game_state['coins'],'red')} coins.")

    elif action=='health':
        print(f"You're still {colored(game_state['health'],'blue')} points away from death.")

    elif action=='clear':
        clear()

    elif action.startswith("go "):
        direction = action.split("go")[1].strip()
        if direction=='north' and game_state['current_location']=='start':
            if 'Unlock Hall' in game_state['quests']:
                print("Algo: Byte, I'm afraid you'll need to find the mysterious key to move forward.")
                continue
            if 'coding tome' in game_state['inventory']:
                print("Byte: I should probably get her the coding tome.")
                print(f"\ndev note-'maybe try {colored('using the coding tome','blue')} near her.'")
                continue
        move(direction)

    elif "look at " in action:
        item_name = action.split("look at ")[1].strip()
        look_at(item_name)

    elif "look" in action:
        look_around()

    elif action.startswith("take "):
        item_name = action.split(maxsplit=1)[-1]
        pick(item_name)

    elif action.strip() == 'use':
        use_inv=True
        current_location_data = realms[game_state['current_realm']]['locations'][game_state['current_location']]
        if 'transition_gate' in current_location_data:
            select=input("1. Use Transition Gate\n2. Open Inventory\n")
            effect('feedback.mp3')
            if select=='1':
                if 'challengers orb' in game_state['inventory']:
                    use_inv=False
                    trans_gate()
                else:
                    input("The gate doesn\'t respond to your touch.")
                    effect('feedback.mp3')
                    continue
        if use_inv:
            useinv()
            
    elif action == 'save':
        save_game()

    elif action == 'exit':
        print("Thank you for playing 'Code of Eternity'!")
        break

    else:
        print("Not sure what you mean. For a list of commands, type 'help'.")
    statupdater()

else:
        input()
        effect('feedback.mp3')
        clear()
        effect('dead.mp3')
        display_dialogue('20death.txt')
        input() 
        colorama.deinit()   

music_thread_stop=True
pygame.quit()