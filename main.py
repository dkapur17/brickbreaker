import json
import os
from time import sleep,time

import header
import utilities
import menu
import endscreen
from board import Board
from paddle import Paddle
from ball import Ball


def main():
    # Get configurations
    config = utilities.fetch_configurations('config.json')
    HEIGHT = config["height"]
    WIDTH = config["width"]
    SMALL_PADDLE_SIZE = config["small_paddle_size"]
    MEDIUM_PADDLE_SIZE = config["medium_paddle_size"]
    LARGE_PADDLE_SIZE = config["large_paddle_size"]
    PADDLE_BOTTOM_PADDING = config["paddle_bottom_padding"]
    PADDLE_SPEED = config["paddle_speed"]
    MAX_LIVES = config["max_lives"]
    BRICK_LENGTH = config["brick_length"]
    FAST_BALL_MULTIPLIER = config["fast_ball_mutliplier"]
    POWERUP_DURATION = config["powerup_duration"]

    # Show blocking menu
    menu.print_menu()

    # Initialize class instances
    cursor = utilities.Cursor()
    nbinput = utilities.Input()
    cursor.hide()

    paddle=Paddle(SMALL_PADDLE_SIZE, MEDIUM_PADDLE_SIZE, LARGE_PADDLE_SIZE, HEIGHT, WIDTH, PADDLE_BOTTOM_PADDING, PADDLE_SPEED, MAX_LIVES)
    board=Board(HEIGHT,WIDTH)
    bricks = utilities.init_bricks(BRICK_LENGTH, WIDTH)
    balls = []
    on_screen_powerups = []
    active_powerups = []
    score = 0
    start_time = time()

    try:
        os.system('stty -echo')
        while paddle.lives > 0:
            balls.append(Ball(paddle,max_multiplier=FAST_BALL_MULTIPLIER))
            # Game Loop
            while True:
                # Get input
                ip = nbinput.get_parsed_input(0.07)
                if ip == 'quit':
                    os.system('clear')
                    cursor.show()
                    exit()
                if ip in ['left', 'right']:
                    paddle.move(ip, balls)
                elif ip == 'space':
                        for ball in balls:
                            ball.launch()
                
                brick_x,brick_y=[],[]
                for ball in balls:
                    a,b,c = ball.move(board, paddle)
                    ball.inbound = a
                    brick_x.append(b)
                    brick_y.append(c)

                balls = list(filter(lambda ball: ball.inbound, balls))
                if len(balls) == 1:
                    paddle.multiball = False
                if not len(balls):
                    break

                bricks,score = utilities.collide_with_brick(bricks, brick_x, brick_y,score,on_screen_powerups,paddle, POWERUP_DURATION)
                for powerup in on_screen_powerups:
                    powerup.move(HEIGHT)
                    if powerup.collected(paddle):
                        powerup.activate(paddle,ball)
                        active_powerups.append(powerup)
                        powerup.inbound = False

                for powerup in active_powerups:
                    if powerup.check_completion():
                        powerup.deactivate(paddle,ball)
            
                on_screen_powerups = list(filter(lambda powerup: powerup.inbound, on_screen_powerups))
                active_powerups = list(filter(lambda powerup: not powerup.expired, active_powerups))

                board.update(paddle,balls,bricks,on_screen_powerups)

                utilities.print_frame(score, paddle.lives, time() - start_time,board.content, WIDTH)

                if not len(list(filter(lambda brick: brick.strength != -1, bricks))):
                    break
            paddle.lives-=1
            paddle.reset()
            on_screen_powerups = []
            if not len(list(filter(lambda brick: brick.strength != -1, bricks))):
                break
        cursor.show()
        endscreen.print_endscreen(score,list(filter(lambda brick: brick.strength != -1, bricks)))
    finally:
        os.system('stty echo')
        cursor.show()
    
        

if __name__=="__main__":
    main()