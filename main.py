import json
import os

import header
import utilities
import menu
from board import Board
from paddle import Paddle

def main():
    # Get configurations
    config = utilities.fetch_configurations('config.json')
    HEIGHT = config["height"]
    WIDTH = config["width"]
    SMALL_PADDLE_SIZE = config["small_paddle_size"]
    LARGE_PADDLE_SIZE = config["large_paddle_size"]
    PADDLE_BOTTOM_PADDING = config["paddle_bottom_padding"]
    PADDLE_SPEED = config["paddle_speed"]
    MAX_LIVES = config["max_lives"]

    # Show blocking menu
    menu.print_menu()

    # Initialize class instances
    cursor = utilities.Cursor()
    nbinput = utilities.Input()
    cursor.hide()

    paddle=Paddle(SMALL_PADDLE_SIZE, LARGE_PADDLE_SIZE, HEIGHT, WIDTH, PADDLE_BOTTOM_PADDING, PADDLE_SPEED, MAX_LIVES)
    board=Board(HEIGHT,WIDTH, paddle)
    score=0

    # Game Loop
    while True:
        board.update(paddle)
        utilities.print_frame(score, paddle.lives,board.content)
        # Get input
        ip = nbinput.get_parsed_input(0.1)
        if ip == 'quit':
            os.system('clear')
            cursor.show()
            exit()
        elif ip != 'space':
            paddle.move(ip)
        else:
            # Handle launch
            continue
        # Update paddle position
    cursor.show()
        

if __name__=="__main__":
    main()