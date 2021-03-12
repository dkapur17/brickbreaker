from random import choice,uniform

from brick import Brick1, Brick2, Brick3, BrickU, BrickE
from powerups import ExpandPaddle, ShrinkPaddle, FastBall, PaddleGrab, MultiBall, ThruBall

def explode(e_brick, bricks):
    to_remove = []

    bricks.remove(e_brick)
    for brick in bricks:
        if brick.x in [e_brick.x - e_brick.length, e_brick.x + e_brick.length] and brick.y == e_brick.y:
            to_remove.append(brick)
        elif brick.y in [e_brick.y -1, e_brick.y + 1] and brick.x == e_brick.x:
            to_remove.append(brick)
        elif brick.x in [e_brick.x - e_brick.length, e_brick.x + e_brick.length] and brick.y in [e_brick.y -1, e_brick.y + 1]:
            to_remove.append(brick)

    for brick in to_remove:
        if brick.strength != -2:
            if brick in bricks:
                bricks.remove(brick)
        else:
            explode(brick, bricks)

def collide_with_brick(bricks, x, y,score,on_screen_powerups,paddle, thru, powerup_prob, ball):

    if x == -1:
        return bricks, score
    
    for brick in bricks:
        if x in range(brick.x, brick.x+brick.length) and y == brick.y:
            # If exploding brick
            if brick.strength == -2:
                post_explosion_bricks = [b for b in bricks]
                explode(brick, post_explosion_bricks)
                destroyed_bricks = [b for b in bricks if b not in post_explosion_bricks]
                explosion_scores = [b.strength for b in destroyed_bricks]
                explosion_scores = [1 if s == -2 else s for s in explosion_scores]
                explosion_scores = [5 if s == -1 else s for s in explosion_scores]
                explosion_scores = [choice([1,2,3]) if s == 6 else s for s in explosion_scores]
                score += sum(explosion_scores)
                bricks = [b for b in post_explosion_bricks]
                for b in destroyed_bricks:
                    if uniform(0,1) <= powerup_prob:
                        powerups = [ExpandPaddle(b.x,b.y,ball.vel_x,ball.vel_y, thru),ShrinkPaddle(b.x,b.y,ball.vel_x,ball.vel_y, thru), FastBall(b.x,b.y,ball.vel_x,ball.vel_y, thru), PaddleGrab(b.x,b.y,ball.vel_x,ball.vel_y, thru), MultiBall(b.x,b.y,ball.vel_x,ball.vel_y, thru), ThruBall(b.x,b.y,ball.vel_x,ball.vel_y, thru)]
                        on_screen_powerups.append(choice(powerups))
            else:
                # If not exploding brick, but thru
                if thru:
                    bricks.remove(brick)
                    if brick.strength in [1,2,3]:
                        score += brick.strength
                    elif brick.strength == 6:
                        score += choice([1,2,3])
                    elif brick.strength == -1:
                        score += 5
                    elif brick.strength == -2:
                        score += 1
                    if uniform(0,1) <= powerup_prob:
                        powerups = [ExpandPaddle(x,y,ball.vel_x,ball.vel_y, thru),ShrinkPaddle(x,y,ball.vel_x,ball.vel_y, thru), FastBall(x,y,ball.vel_x,ball.vel_y, thru), PaddleGrab(x,y,ball.vel_x,ball.vel_y, thru), MultiBall(x,y,ball.vel_x,ball.vel_y, thru), ThruBall(x,y,ball.vel_x,ball.vel_y, thru)]
                        on_screen_powerups.append(choice(powerups))
                # If not exploding brick and not thru
                else:
                    if brick.strength != -1:
                        bricks.remove(brick)
                        score += 1
                    if brick.strength == 1 and uniform(0,1) <= powerup_prob:
                        powerups = [ExpandPaddle(x,y,ball.vel_x,ball.vel_y, thru),ShrinkPaddle(x,y,ball.vel_x,ball.vel_y, thru), FastBall(x,y,ball.vel_x,ball.vel_y, thru), PaddleGrab(x,y,ball.vel_x,ball.vel_y, thru), MultiBall(x,y,ball.vel_x,ball.vel_y, thru), ThruBall(x,y,ball.vel_x,ball.vel_y, thru)]
                        on_screen_powerups.append(choice(powerups))
                    elif brick.strength == 2:
                        bricks.append(Brick1(brick.length, brick.x, brick.y))
                    elif brick.strength == 3:
                        bricks.append(Brick2(brick.length, brick.x, brick.y))
                    elif brick.strength == 6:
                        bricks.append(choice([
                            Brick1(brick.length, brick.x, brick.y),
                            Brick2(brick.length, brick.x, brick.y),
                            Brick3(brick.length, brick.x, brick.y)
                        ]))
            break
    return bricks,score