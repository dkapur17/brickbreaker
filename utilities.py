import os
import json
from colorama import Fore, Back
import sys
import termios
import tty
import signal
from time import sleep

import header

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
            elif ip == b'\x1b[D' or ip == b'a':
                text = 'left'
            elif ip == b'\x1b[C' or ip == b'd':
                text = 'right'
            elif ip == b' ':
                text = 'space'
            elif ip == b'\r':
                text = 'enter'
            else:
                text = 'none'
            if text != 'none':
                sleep(timeout)
            return text
        except TimeoutError:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
            return None

def print_frame(score, lives, board, ball):
    os.system('clear')
    HEADER = header.create_header(score, lives)
    for row in HEADER:
        print(''.join(row).center(os.get_terminal_size().columns))
    for row in board:
        print(''.join(row).center(os.get_terminal_size().columns))
    print(ball.x, ball.y)

def fetch_configurations(file_name):
    with open(file_name) as f:
            config = json.load(f)
    return config