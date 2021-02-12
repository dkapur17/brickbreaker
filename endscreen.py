import os
from colorama import Fore
import art

def print_endscreen(score, bricks):

    a,b,c,d,e,f,g=art.get_game_over_art() if len(bricks) else art.get_win_art()
    os.system('clear')
    print("\n"*(os.get_terminal_size().lines//4))
    print(Fore.GREEN)
    print (a.center(os.get_terminal_size().columns))
    print (b.center(os.get_terminal_size().columns))
    print (c.center(os.get_terminal_size().columns))
    print (d.center(os.get_terminal_size().columns))
    print (e.center(os.get_terminal_size().columns))
    print (f.center(os.get_terminal_size().columns))
    print (g.center(os.get_terminal_size().columns))
    print(Fore.RESET)
    print('\n'*3)
    print(f"Your score is: {score}".center(os.get_terminal_size().columns))