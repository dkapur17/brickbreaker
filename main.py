import json
import os

import utilities
import menu
import endscreen

import levels

def main():
    # Get configurations
    config = utilities.fetch_configurations('config.json')
    MAX_LIVES = config["max_lives"]

    # Show blocking menu
    menu.print_menu()

    cursor = utilities.Cursor()
    cursor.hide()
    try:
        os.system('stty -echo')

        # Level 1
        score, time_elapsed, state, bricks_left, lives, quit_stat = levels.load_level(1,config, MAX_LIVES)
        if quit_stat == 1:
            os.system('clear')
            os.system('stty echo')
            cursor.show()
            exit()
        elif state == "lose":
            return endscreen.print_endscreen(score, state)
        
        score, time_elapsed, state, bricks_left, lives, quit_stat = levels.load_level(2, config, lives, score, time_elapsed)
        if quit_stat == 1:
            os.system('clear')
            os.system('stty echo')
            cursor.show()
            exit()
        elif state == "lose":
            return endscreen.print_endscreen(score, state)
        
        score, state, quit_stat = levels.boss_level(config, lives, score, time_elapsed)
        if quit_stat == 1:
            os.system('clear')
            os.system('stty echo')
            cursor.show()
            exit()
        endscreen.print_endscreen(score, state)
        cursor.show()
        # Show endscreen (either Game Over or You Win
    finally:
        # Reset terminal changes
        os.system('stty echo')
        cursor.show()
        
if __name__=="__main__":
    main()