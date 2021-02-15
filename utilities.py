import os
import json
from colorama import Fore, Back
import sys
import termios
import tty
import signal
from time import sleep
from random import choice

import header
from brick import Brick1, Brick2, Brick3, BrickU, BrickE

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
            elif ip == b' ':
                text = 'space'
            elif ip == b'\r':
                text = 'enter'
            else:
                text = 'none'
            sleep(timeout)
            return text
        except TimeoutError:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return None

def print_frame(score, lives, time_elapsed, board, WIDTH):
    os.system('clear')
    HEADER = header.create_header(score, lives, time_elapsed)
    padding = (os.get_terminal_size().columns - WIDTH)//2
    for row in HEADER:
        print(' '*padding + ''.join(row))
    brick_colors = {'1': Fore.GREEN,'2': Fore.YELLOW,'3': Fore.RED,'U': Fore.WHITE, 'E': Fore.BLUE}
    for row in board:
        s=''
        for ch in row:
            if ch in get_brick_chars():
                s+=brick_colors[ch] +  '█' + Fore.RESET
            else:
                s+=ch
        print(' '*padding + s)

def fetch_configurations(file_name):
    with open(file_name) as f:
            config = json.load(f)
    return config


def init_bricks(brick_length, board_width):
    bricks = []
    try:
        with open('brick_layout.txt') as f:
            data = f.read().split('\n')
    except:
        print("Could not locate brick_layout.txt")
        exit()
    i,j=0,0
    brick_list = [BrickU ,Brick1, Brick2, Brick3, BrickE]
    try:
        for x in range(21, board_width-21, brick_length):
            for y in range(5,18):
                if data[i][j] != '.':
                    bricks.append(brick_list[int(data[i][j])](brick_length, x, y))
                i+=1
            j += 1
            i = 0
        return bricks
    except:
        print("The brick layout file must be 13x13 in size and only have characyer '.','0','1','2', '3' and '4'")
        exit()

def get_brick_chars():
    return '123UE'

def collide_with_brick(bricks, x_list, y_list,score):

    for (x,y) in zip(x_list,y_list):
        if x == -1:
            return bricks,score
        for brick in bricks:
            if x in range(brick.x, brick.x+brick.length) and y == brick.y:
                if brick.strength != -1:
                    bricks.remove(brick)
                    score += 1
                if brick.strength == 2:
                    bricks.append(Brick1(brick.length, brick.x, brick.y))
                elif brick.strength == 3:
                    bricks.append(Brick2(brick.length, brick.x, brick.y))
                break

    return bricks,score
