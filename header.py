import os
import json
import art
from colorama import Fore

def create_header(score, lives, time_elapsed):
    with open('config.json') as f:
        config = json.load(f)
    WIDTH = config["width"]
    HEIGHT = config["header_heigth"]
    HEADER_TEXT_POSITION = config["header_text_position"]
    header = [[' ']*WIDTH]*HEIGHT
    padding = 4
    a,b,c,d=art.get_header_art()
    header[0] = Fore.GREEN + a.center(WIDTH) + Fore.RESET
    header[1] = Fore.GREEN + b.center(WIDTH) + Fore.RESET
    header[2] = Fore.GREEN + c.center(WIDTH) + Fore.RESET
    header[3] = Fore.GREEN + d.center(WIDTH) + Fore.RESET
    score_text = f"Score: {score}"
    lives_text = 'Lives: ' + Fore.RED + ' '.join(['♥']*lives) + Fore.RESET
    time_text = f'Time: {time_elapsed:.2f}s'
    divider = ' '*((WIDTH-len(score_text)-len(lives_text)-len(time_text))//2)
    header[HEADER_TEXT_POSITION] = list(' '*padding + score_text+ divider + time_text + divider +lives_text)
    return header
