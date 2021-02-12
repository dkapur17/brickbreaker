import json
import os
from time import sleep

import header
import utilities
import menu
import gameover
from board import Board
from paddle import Paddle
from ball import Ball

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
    board=Board(HEIGHT,WIDTH)
    score=0

    try:
        os.system('stty -echo')
        while paddle.lives > 0:
            ball = Ball(paddle)
            # Game Loop
            while True:
                in_bound = ball.move(board, paddle)
                if not in_bound:
                    break

                # Get input
                ip = nbinput.get_parsed_input(0.07)
                if ip == 'quit':
                    os.system('clear')
                    cursor.show()
                    exit()
                if ip in ['left', 'right']:
                    paddle.move(ip, ball)
                elif ip == 'space':
                        ball.launch()
                board.update(paddle,ball)
                utilities.print_frame(score, paddle.lives,board.content,ball)
                
            paddle.lives-=1
            paddle.reset()
        cursor.show()
        gameover.print_game_over_screen(score)
    finally:
        os.system('stty echo')
        cursor.show()
    
        

if __name__=="__main__":
    main()