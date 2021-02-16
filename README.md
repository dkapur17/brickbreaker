# DASS Assignment 2 - Brick Breaker

This is a terminal based brick breaker game. Zero GUI. The game physics makes use of a 2D grid that represents the board, with each element of the board being a single character. In each iteration of the game loop, the board is updated based on user input and other factors within the game and the new board is printed on the screen.

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

## Specifications

1. The game is highly customizable as all configuration variables of the game have been stored together in a `config.json` file. When the game is launched,  the file is read and configuration variables are set in the game using a helper function.

2. The brick layout is highly customizable. Specify the brick layout in a 13x13 matrix in `brick_layout.txt`. The allowed characters are `.` representing an empty space, `1`,`2` and `3` representing bricks of respective strengths and `4`, representing an unbreakable brick.

3. Power ups appear with a 50% chance when a brick is broken. Which power up appears is randomly chosen. Each powerup is represented as a collectable that falls downwards from the location of the brick that was broken. If not collected, it goes out of bounds and is removed from the game. Each powerup is represented by a unique chracter:
* `E`: "Expand Paddle"
* `S`: "Shrink Paddle"
* `M`: "Ball Multiplier" (a.k.a Multi-ball)
* `F`: "Fast Ball"
* `T`: "Thru Ball"
* `G`: "Paddle Grab"

4. If a powerup that is already active is collected again, the duration for that powerup will be topped up to its original duration.

5. For the **"Expand Paddle"** and **"Shrink Paddle"** powerups, the latest collected powerup will replace the existing one and duration will be topped up to the original duration.

6. The **"Ball Multiplier"** is the only powerup that doesn't have a duration.

7. Though not mentioned as a requirement, diagonal collision has also been handled. If the ball hits a brick or the border of the board at a corner, both its `x` and `y` velocities will be flipped.

8. When the the **"Ball Mutliplier"** powerup is picked up, evey ball already in play is cloned. A clone of a ball is an exact copy of the ball, including all the same powerups currently in effect to the original ball. The only difference in a clone is that its `x` direction velocity is negative of that of its source ball.

9. Each time the ball hits a brick and does damage to it, the score is increased by `1`. But in while the **"Thru-ball"** powerup is active, every brick that is destoryed adds an amount equal to its strength to the score. Breaking an *unbreakable* brick while in **"Thru-ball"** mode will add `4` points to the score.

10. The a round is over when the all the balls have gone out of bounds, i.e., they have hit the bottom edge of the board. In this case, the player loses a life.

11. The game is over either when the player loses all his lives or all breakable bricks in the game have been destroyed.


### Usage of OOP Concepts

1. **Inheritance**: Each Brick type has its own class, each of which inherit some generic brick properties and methods from a parent `Brick` class (Refer to `brick.py`)

2. **Polymorphism**: Each Powerup is unique and has unique effects, but have a generic template. They are created, collected, activated and destroyed. What happens in each of these steps is unique to the powerup itself. Thus each powerup has its own class which inherits from a general `Powerup` class. Each method then modifies the methods in the parent class as per its own requirements (Refer to `powerups.py`).

3. **Encapsulation**: Every game object is represented as instance of a class. The actions and properties of the object are defined by the class methods and variables.

4. **Abstraction**: The behaviour of game objects are hidden from the end user by using methods. Making an object move is as simple as called its `.move()` method. (Refer to `main.py`)