# DASS Assignment 2 - Brick Breaker

This is a terminal based brick breaker game. Zero GUI. The game physics makes use of a 2D grid that represents the board, with each element of the board being a single character. In each iteration of the game loop, the board is updated based on user input and other factors within the game and the new board is printed to the screen.

The only non-core python library used was `colorama` to add color to the text.

## Running the game

Install `colorama` if you haven't already:
```bash
pip3 install colorama
```
Then `cd` into the root directory of this project and run
```bash
python3 main.py
```
to launch the game.

## How to play

Use `a` and `d` or the left and right arrow keys to move the paddle. Use `space` to launch the ball. Your target is to destroy all the colored bricks on the screen. To do damage to a brick, hit it with the ball.

There are 5 types of bricks in the game. Green bricks take 1 hit to destroy, Yellow ones take 2 and Red ones take 3. White bricks are unbreakable under normal circumstances. Blue bricks are called exploding bricks. Upon hitting one of them, it not just destroys the brick, but all its neighboring bricks as well. If one of its neighboring bricks is also an exploding brick, it triggers a chain reaction.

If the ball hits the bottom edge of the screen, you lose a life. You lose if you lose all your lives before destroying all colored bricks.

On destroying a brick, a random powerup may appear in the bricks position and start moving downwards. Collect it with your paddle to gain the powerup. The powerups are:

* `E`: "Expand Paddle" make the paddle larger
* `S`: "Shrink Paddle" makes the paddle smaller
* `M`: "Ball Multiplier" (a.k.a Multi-ball) makes a copy of each ball currently in play
* `F`: "Fast Ball" increases the speed of each ball in play 1.5 times
* `T`: "Thru Ball" ball goes through any bricks it touches, including unbreakable ones
* `G`: "Paddle Grab" every time the ball hits the paddle, you can launch it at will.

Each powerup lasts for 15 seconds (except for Ball Multiplier, which has no time duration).

Every time you do damage to a brick, your score increases by 1. If you directly destroy a brick (using Thru-ball or an exploding brick), you get a score equivalent to its strength (the strength of an exploding brick itself is 1). If you manage to destroy an unbreakable brick (using Thru-ball or an exploding brick), your score increases by 5 points.


## Specifications

1. The game is highly customizable as all configuration variables of the game have been stored together in a `config.json` file. When the game is launched,  the file is read and configuration variables are set in the game using a helper function.

2. The brick layout is highly customizable. Specify the brick layout in a 13x13 matrix in `brick_layout.txt`. The allowed characters are `.` representing an empty space, `1`,`2` and `3` representing bricks of respective strengths, `4` representing an unbreakable brick and `5` representing an exploding brick.

3. A custom Input method has been used that allows using arrow keys to control the paddle as well as the `a` and `d` keys.

4. Power ups appear with a 50% chance when a brick is broken. Which power up appears is randomly chosen. Each powerup is represented as a collectable that falls downwards from the location of the brick that was broken. If not collected, it goes out of bounds and is removed from the game.

5. If a powerup that is already active is collected again, the duration for that powerup will be topped up to its original duration.

6. For the **"Expand Paddle"** and **"Shrink Paddle"** powerups, the latest collected powerup will replace the existing one and duration will be topped up to the original duration.

7. The **"Ball Multiplier"** is the only powerup that doesn't have a duration.

8. Though not mentioned as a requirement, diagonal collision has also been handled. If the ball hits a brick or the border of the board at a corner, both its `x` and `y` velocities will be flipped.

9. When the the **"Ball Mutliplier"** powerup is picked up, evey ball already in play is cloned. A clone of a ball is an exact copy of the ball, including all the same powerups currently in effect to the original ball. The only difference in a clone is that its `x` direction velocity is negative of that of its source ball.

10. Each time the ball hits a brick and does damage to it, the score is increased by `1`. But in while the **"Thru-ball"** powerup is active, every brick that is destoryed adds an amount equal to its strength to the score. Breaking an *unbreakable* brick while in **"Thru-ball"** mode will add `4` points to the score.

12. A round is over when the all the balls have gone out of bounds, i.e., they have hit the bottom edge of the board. In this case, the player loses a life.

13. The game is over either when the player loses all his lives or all breakable bricks in the game have been destroyed.


### Usage of OOP Concepts

1. **Inheritance**: Each Brick type has its own class, each of which inherit some generic brick properties and methods from a parent `Brick` class (Refer to `brick.py`)

2. **Polymorphism**: Each Powerup is unique and has unique effects, but have a generic template. They are created, collected, activated and deactivated. What happens in each of these steps is unique to the powerup itself. Thus each powerup has its own class which inherits from a general `Powerup` class. Each power up class then modifies the methods in the parent class as per its own requirements (Refer to `powerups.py`).

3. **Encapsulation**: Every game object is represented as instance of a class. The actions and properties of the object are defined by the class methods and variables (Refer `ball.py`, `board.py`, `brick.py`, `paddle.py`, `powerups.py`).

4. **Abstraction**: The behaviour of game objects are hidden from the end user by using methods. For example, making an object move is as simple as called its `.move()` method (Refer to `main.py`), or cloning a ball is just requires a call to the `.make_twin()` method.