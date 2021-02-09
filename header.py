import os
import json
import art
from colorama import Fore

def create_header(score, lives):
    with open('config.json') as f:
        config = json.load(f)
    WIDTH = config["width"]
    HEIGHT = config["header_heigth"]
    HEADER_TEXT_POSITION = config["header_text_position"]
    header = [[' ']*WIDTH]*HEIGHT
    padding = 4
    a,b,c,d=art.get_header_art()
    header[0] = Fore.GREEN + a.center(os.get_terminal_size().columns) + Fore.RESET
    header[1] = Fore.GREEN + b.center(os.get_terminal_size().columns) + Fore.RESET
    header[2] = Fore.GREEN + c.center(os.get_terminal_size().columns) + Fore.RESET
    header[3] = Fore.GREEN + d.center(os.get_terminal_size().columns) + Fore.RESET
    score_text = f"Score: {score}"
    lives_text = 'Lives: ' + Fore.RED + ' '.join(['♥']*lives) + Fore.RESET
    divider = ' '*(WIDTH-len(score_text)-len(lives_text))
    header[HEADER_TEXT_POSITION] = list(' '*2*padding + score_text+ divider +lives_text)
    return header
