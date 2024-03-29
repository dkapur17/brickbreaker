import os
import json
from colorama import Fore, Back
import sys
import termios
import tty
import signal
from time import sleep
from re import sub
from random import choice

import header
from brick import Brick1, Brick2, Brick3, BrickU, BrickE, BrickR


class Cursor:
    def __init__(self):
        self.__hide_string = "\x1b[?25l"
        self.__show_string = "\x1b[?25h"
    def hide(self):
        print(self.__hide_string)
    def show(self):
        print(self.__show_string)

class Input:
    def _get_key_raw(self):
        fd = sys.stdin.fileno()
        self.old_config = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.buffer.raw.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_config)
        return ch
    
    def _timeout_handler(self, signum, frame):
        raise TimeoutError
    
    def get_parsed_input(self, timeout=0.1):
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout)
        try:
            ip = self._get_key_raw()
            signal.alarm(0)
            if ip == b'\x03':
                text = 'quit'
            elif ip in [b'\x1b[D', b'a', b'A']:
                text = 'left'
            elif ip in [b'\x1b[C', b'd', b'D']:
                text = 'right'
            elif ip in [b'\x1b[A', b'w', b'W']:
                text = 'fire'
            elif ip == b' ':
                text = 'space'
            elif ip == b'\r':
                text = 'enter'
            elif ip in [b's', b'S']:
                text = 'skip'
            else:
                text = 'none'
            sleep(timeout)
            return text
        except TimeoutError:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return None

def print_frame(score, lives, time_elapsed, board, WIDTH, powerup_values, ufo_lives = None):
    os.system('clear')
    HEADER = header.create_header(score, lives, time_elapsed)
    padding = (os.get_terminal_size().columns - WIDTH)//2
    for row in HEADER:
        print(' '*padding + ''.join(row))
    colors = [Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.WHITE, Fore.BLUE]
    brick_colors = {'1': colors[0],'2': colors[1],'3': colors[2],'4': colors[3], '5': colors[4], '6': choice(colors[:3])}
    for row in board:
        s=''
        for ch in row:
            if ch in get_brick_chars():
                s+=brick_colors[ch] +  '█' + Fore.RESET
            else:
                s+=ch
        print(' '*padding + s)
    if ufo_lives == None:
        active_powerup_values = [(sub(r'([A-Z])', r' \g<1>', k).title() + ": " + str(v)) for k,v in zip(powerup_values.keys(),powerup_values.values()) if v != 0]
        print("Active Powerups".center(os.get_terminal_size().columns))
        print((' '.join(active_powerup_values)).center(os.get_terminal_size().columns))
    else:
        print(("Boss Lives:" + Fore.BLUE + ' ♥'*ufo_lives + Fore.RESET).center(os.get_terminal_size().columns))


def fetch_configurations(file_name):
    with open(file_name) as f:
            config = json.load(f)
    return config


def init_bricks(brick_length, board_width, level):
    bricks = []
    try:
        with open('./layouts/' + level+ '.txt') as f:
            data = f.read().split('\n')
    except:
        print("Could not locate required layout file")
        exit()
    i,j=0,0
    brick_list = {"1": Brick1, "2": Brick2, "3": Brick3, "4": BrickU, "5": BrickE, "6": BrickR}
    try:
        for x in range(21, board_width-21, brick_length):
            for y in range(4,17):
                if data[i][j] != '.':
                    bricks.append(brick_list[data[i][j]](brick_length, x, y))
                i+=1
            j += 1
            i = 0
        return bricks
    except:
        print("The brick layout file must be 13x13 in size and only have characyer '.','1','2','3', '4','5','6'")
        exit()

def get_brick_chars():
    return '123456'