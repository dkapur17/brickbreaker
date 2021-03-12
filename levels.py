import os
from time import sleep,time
from colorama import Fore

import endscreen
import header
import utilities
import art

import collision_handler
from board import Board
from paddle import Paddle
from ball import Ball

def show_level_screen(level):
    a,b,c,d,e,f,g = art.get_level_art(level)
    os.system('clear')
    print("\n"*(os.get_terminal_size().lines//4))
    print(Fore.YELLOW)
    print (a.center(os.get_terminal_size().columns))
    print (b.center(os.get_terminal_size().columns))
    print (c.center(os.get_terminal_size().columns))
    print (d.center(os.get_terminal_size().columns))
    print (e.center(os.get_terminal_size().columns))
    print (f.center(os.get_terminal_size().columns))
    print (g.center(os.get_terminal_size().columns))
    print(Fore.RESET)
    sleep(1)

def load_level(level, config, lives, score=0, time_elapsed=0):

    HEIGHT = config["height"]
    WIDTH = config["width"]
    SMALL_PADDLE_SIZE = config["small_paddle_size"]
    MEDIUM_PADDLE_SIZE = config["medium_paddle_size"]
    LARGE_PADDLE_SIZE = config["large_paddle_size"]
    PADDLE_BOTTOM_PADDING = config["paddle_bottom_padding"]
    PADDLE_SPEED = config["paddle_speed"]
    BRICK_LENGTH = config["brick_length"]
    FAST_BALL_MULTIPLIER = config["fast_ball_mutliplier"]
    POWERUP_PROB = config["powerup_prob"]
    DROP_INTERVAL = config["drop_interval"]
    MAX_LIVES = lives

    _input = utilities.Input()

    init_times = [-1]*MAX_LIVES
    time_segments = [0]*MAX_LIVES

    paddle=Paddle(SMALL_PADDLE_SIZE, MEDIUM_PADDLE_SIZE, LARGE_PADDLE_SIZE, HEIGHT, WIDTH, PADDLE_BOTTOM_PADDING, PADDLE_SPEED, MAX_LIVES)
    board=Board(HEIGHT,WIDTH)
    bricks = utilities.init_bricks(BRICK_LENGTH, WIDTH, f"level{level}")

    last_drop_time = 0

    show_level_screen(level)

    while paddle.lives > 0:
        balls = []
        balls.append(Ball(paddle, max_multiplier=FAST_BALL_MULTIPLIER))
        powerup_values = {
            "expandPaddle": 0,
            "shrinkPaddle": 0,
            "fastBall": 0,
            "paddleGrab": 0,
            "multiBall": 1,
            "thruBall": 0
        }
        on_screen_powerups = []
        active_powerups = []

        while True:
            if init_times[MAX_LIVES - paddle.lives] != -1:
                time_segments[MAX_LIVES-paddle.lives] = time() - init_times[MAX_LIVES - paddle.lives]
            
            ip = _input.get_parsed_input(0.07)
            if ip == 'quit':
                return 0,0,0,0,0,1
            if ip in ['left', 'right']:
                paddle.move(ip, balls)
            elif ip == 'space':
                if init_times[MAX_LIVES - paddle.lives] == -1:
                    init_times[MAX_LIVES - paddle.lives] = time()
                for ball in balls:
                    ball.launch()

            if(int(time_elapsed + sum(time_segments) )> 0 and int(time_elapsed + sum(time_segments)) % DROP_INTERVAL == 0):
                if(int(time() - last_drop_time) >= DROP_INTERVAL and init_times[MAX_LIVES-paddle.lives] != -1):
                    last_drop_time = time()
                    for brick in bricks:
                        brick.y += 1
                        if brick.y == paddle.y:
                            bricks_left = len(list(filter(lambda brick: brick.strength != -1, bricks)))
                            return score, time_elapsed + sum(time_segments),"lose",bricks_left,0,0
            
            board.update(paddle, balls, bricks, on_screen_powerups)

            for ball in balls:
                ball.inbound, brick_x, brick_y = ball.move(board, paddle)
                bricks, score = collision_handler.collide_with_brick(bricks, brick_x, brick_y, score, on_screen_powerups, paddle, ball.thru, POWERUP_PROB, ball)
                board.update(paddle, balls, bricks, on_screen_powerups)

            balls = list(filter(lambda ball: ball.inbound, balls))

            if not len(balls):
                break
        
            powerup_values["multiBall"] = len(balls)

            for powerup in on_screen_powerups:
                powerup.move(HEIGHT, WIDTH)
                if powerup.collected(paddle):
                    powerup.activate(paddle, balls)
                    if powerup.name == "multiBall":
                        balls = powerup.activate(paddle, balls)
                    elif powerup.name in ["expandPaddle", "shrinkPaddle"]:
                        powerup_values["expandPaddle"] = 0
                        powerup_values["shrinkPaddle"] = 0
                        active_powerups = list(filter(lambda p: p.name not in ["expandPaddle", "shrinkPaddle"], active_powerups))
                    else:
                        active_powerups = list(filter(lambda p: p.name != powerup.name, active_powerups))
                    if powerup.name != "multiBall":
                        active_powerups.append(powerup)
                    powerup.inbound = False
            
            for powerup in active_powerups:
                if powerup.name != "multiBall":
                    powerup_values[powerup.name] = powerup.get_time_left()
                if powerup.check_completion():
                    powerup.deactivate(paddle, balls)
                    if powerup_values[powerup.name] != "multiBall":
                        powerup_values[powerup.name] = 0

            on_screen_powerups = list(filter(lambda powerup: powerup.inbound, on_screen_powerups))
            active_powerups = list(filter(lambda powerup: not powerup.expired, active_powerups))

            board.update(paddle, balls, bricks, on_screen_powerups)

            utilities.print_frame(score, paddle.lives, time_elapsed + sum(time_segments), board.content, WIDTH, powerup_values)

            if not len(list(filter(lambda brick: brick.strength != -1, bricks))):
                break
        
        paddle.lives -= 1
        paddle.reset()

        if not len(list(filter(lambda brick: brick.strength != -1, bricks))):
            break
    bricks_left = len(list(filter(lambda brick: brick.strength != -1, bricks)))
    if bricks_left == 0:
        paddle.lives += 1
    return score, sum(time_segments), ("win" if bricks_left == 0 else "lose"), bricks_left, paddle.lives, 0