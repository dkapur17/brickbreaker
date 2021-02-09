import os
from colorama import Fore
import utilities
import art

def print_menu():
    a,b,c,d,e,f,g = art.get_homescreen_art()
    color_loop = [Fore.RED, Fore.MAGENTA, Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW]
    color_index = 0
    cursor = utilities.Cursor()
    nbinput = utilities.Input()
    cursor.hide()
    while True:
        os.system('clear')
        print("\n"*(os.get_terminal_size().lines//4))
        print(color_loop[color_index])
        print (a.center(os.get_terminal_size().columns))
        print (b.center(os.get_terminal_size().columns))
        print (c.center(os.get_terminal_size().columns))
        print (d.center(os.get_terminal_size().columns))
        print (e.center(os.get_terminal_size().columns))
        print (f.center(os.get_terminal_size().columns))
        print (g.center(os.get_terminal_size().columns))
        print(Fore.RESET)
        print("\n"*3)
        print("Press Enter to Play...".center(os.get_terminal_size().columns))
        color_index += 1
        color_index %= len(color_loop)
        ip = nbinput.get_parsed_input()
        if ip == 'enter':
            break
        elif ip == 'quit':
            os.system('clear')
            cursor.show()
            exit()
    cursor.show()