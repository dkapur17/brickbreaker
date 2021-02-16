import json
import os
from time import sleep,time

import header
import utilities
import collision_handler
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

    # Show blocking menu
    menu.print_menu()

    # Initialize class instances
    # Utility items
    cursor = utilities.Cursor()
    nbinput = utilities.Input()
    cursor.hide()

    # Game objects
    paddle=Paddle(SMALL_PADDLE_SIZE, MEDIUM_PADDLE_SIZE, LARGE_PADDLE_SIZE, HEIGHT, WIDTH, PADDLE_BOTTOM_PADDING, PADDLE_SPEED, MAX_LIVES)
    board=Board(HEIGHT,WIDTH)
    bricks = utilities.init_bricks(BRICK_LENGTH, WIDTH)
    # Game Variables
    balls = []
    on_screen_powerups = []
    active_powerups = []
    score = 0
    init_times = [-1]*MAX_LIVES
    time_segments = [0]*MAX_LIVES

    powerup_values = {
        "expandPaddle": 0,
        "shrinkPaddle": 0,
        "fastBall": 0,
        "paddleGrab": 0,
        "multiBall": 1,
        "thruBall": 0
    }

    try:
        # Make stdin non-echo
        os.system('stty -echo')

        while paddle.lives > 0:
            # At the start of the round, add a ball to the balls array
            balls = []
            balls.append(Ball(paddle,max_multiplier=FAST_BALL_MULTIPLIER))

            # Round Loop
            while True:
                # Update time
                if init_times[MAX_LIVES-paddle.lives] != -1:
                    time_segments[MAX_LIVES-paddle.lives] = time() - init_times[MAX_LIVES-paddle.lives]

                # Get input and take action
                ip = nbinput.get_parsed_input(0.07)
                if ip == 'quit':
                    os.system('clear')
                    cursor.show()
                    exit()
                if ip in ['left', 'right']:
                    paddle.move(ip, balls)
                elif ip == 'space':
                    if init_times[MAX_LIVES - paddle.lives] == -1:
                        init_times[MAX_LIVES-paddle.lives] = time()
                    for ball in balls:
                        ball.launch()

                # Update the contents of the board since some game objects may have changed positions
                board.update(paddle,balls,bricks,on_screen_powerups)

                # Handle movement and collision for each ball
                for ball in balls:
                    ball.inbound,brick_x,brick_y = ball.move(board, paddle)
                    bricks,score = collision_handler.collide_with_brick(bricks, brick_x, brick_y,score,on_screen_powerups,paddle, ball.thru)
                    # After each ball collision, update board contents
                    board.update(paddle,balls,bricks,on_screen_powerups)

                # Remove all the balls that have gone out of bounds
                balls = list(filter(lambda ball: ball.inbound, balls))

                # If all ball have gone out of bounds, end the round
                if not len(balls):
                    break

                powerup_values["multiBall"] = len(balls)
                # Iterate over all the powerups visible on the screen
                for powerup in on_screen_powerups:
                    # Update its position
                    powerup.move(HEIGHT)
                    # If it has been collected, activate it and moce it to the activated array and remove it from current array
                    if powerup.collected(paddle):
                        powerup.activate(paddle,balls)
                        if powerup.name == "multiBall":
                            balls = powerup.activate(paddle, balls)
                        elif powerup.name in ["expandPaddle", "shrinkPaddle"]:
                            active_powerups = list(filter(lambda p: p.name not in ['expandPaddle', 'shrinkPaddle'], active_powerups))
                        else:
                            active_powerups = list(filter(lambda p: p.name != powerup.name, active_powerups))
                        if powerup.name != "multiBall":
                            active_powerups.append(powerup)
                        powerup.inbound = False
                
                # Iterate over all active powerups
                for powerup in active_powerups:
                    # If the power up's duration is completed, deactivate it
                    if powerup.name != "multiBall":
                        powerup_values[powerup.name] = powerup.get_time_left()
                    if powerup.check_completion():
                        powerup.deactivate(paddle,balls)
                        if powerup_values[powerup.name] != "multiBall":
                            powerup_values[powerup.name] = 0
            
                # Filter the two powerup lists as mentioned above
                on_screen_powerups = list(filter(lambda powerup: powerup.inbound, on_screen_powerups))
                active_powerups = list(filter(lambda powerup: not powerup.expired, active_powerups))

                # Update the board as new game objects may have been introduced
                board.update(paddle,balls,bricks,on_screen_powerups)

                # Print the board on the screen
                utilities.print_frame(score, paddle.lives, sum(time_segments),board.content, WIDTH, powerup_values)

                # If all breakable bricks have been broken, end the round
                if not len(list(filter(lambda brick: brick.strength != -1, bricks))):
                    break
            # Since the round was over, decrement lives
            paddle.lives-=1
            # Reset the paddle position and size
            paddle.reset()
            # Remove all powerups from the screen
            on_screen_powerups = []
            # Remove all active powerups
            active_powerups = []
            # Reset powerup values
            powerup_values = {
                "expandPaddle": 0,
                "shrinkPaddle": 0,
                "fastBall": 0,
                "paddleGrab": 0,
                "multiBall": 1,
                "thruBall": 0
            }
            # If there are no more breakable bricks in the game, break from game loop
            if not len(list(filter(lambda brick: brick.strength != -1, bricks))):
                break
        cursor.show()
        # Show endscreen (either Game Over or You Win)
        endscreen.print_endscreen(score,list(filter(lambda brick: brick.strength != -1, bricks)))
    finally:
        # Reset terminal changes
        os.system('stty echo')
        cursor.show()
    
        
if __name__=="__main__":
    main()