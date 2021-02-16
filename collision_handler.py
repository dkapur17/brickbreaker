from random import choice,uniform

from brick import Brick1, Brick2, Brick3, BrickU, BrickE
from powerups import ExpandPaddle, ShrinkPaddle, FastBall, PaddleGrab, MultiBall, ThruBall

def collide_with_brick(bricks, x, y,score,on_screen_powerups,paddle, thru):

    if x == -1:
        return bricks,score
    for brick in bricks:
        if x in range(brick.x, brick.x+brick.length) and y == brick.y:
            # powerups = [ExpandPaddle(x,y),ShrinkPaddle(x,y), FastBall(x,y), PaddleGrab(x,y), MultiBall(x,y), ThruBall(x,y)]
            powerups = [ExpandPaddle(x,y)]
            if thru:
                bricks.remove(brick)
                if int(brick.content[0]) < 5:
                    score += int(brick.content[0])
                if uniform(0,1) <= 0.5:
                    on_screen_powerups.append(choice(powerups))
            else:
                if brick.strength != -1:
                    bricks.remove(brick)
                    score += 1
                if brick.strength == 1 and uniform(0,1) <= 0.9:
                    on_screen_powerups.append(choice(powerups))
                if brick.strength == 2:
                    bricks.append(Brick1(brick.length, brick.x, brick.y))
                elif brick.strength == 3:
                    bricks.append(Brick2(brick.length, brick.x, brick.y))
                break

    return bricks,score
