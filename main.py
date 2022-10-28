# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

from distutils.file_util import move_file
from genericpath import exists
from inspect import ismodule
import math
import random
from secrets import choice
from subprocess import check_output
from sys import flags
import typing
from xxlimited import foo

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "JoelErni",  # TODO: Your Battlesnake Username
        "color": "#4f2c06",  # TODO: Choose color
        "head": "replit-mark",  # TODO: Choose head
        "tail": "fat-rattle",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    #Check sides
    if my_head['x'] == 0:
        is_move_safe["left"] = False
    if my_head['x'] == board_width-1:
        is_move_safe["right"] = False
    if my_head['y'] == 0:
        is_move_safe["down"] = False
    if my_head['y'] == board_height-1:
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    for snake in game_state['board']['snakes']:
        for body in snake['body']:
            if my_head['x']==body['x'] and my_head['y']==body['y']-1:
                is_move_safe["up"] = False
            if my_head['x']==body['x'] and my_head['y']==body['y']+1:
                is_move_safe["down"] = False
            if my_head['y']==body['y'] and my_head['x']==body['x']-1:
                is_move_safe["right"] = False
            if my_head['y']==body['y'] and my_head['x']==body['x']+1:
                is_move_safe["left"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    # next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    food_distance = []
    for x in food:
        food_distance.append(math.sqrt(math.pow(my_head['x']-x['x'],2)+math.pow(my_head['y']-x['y'],2)))
    print(f"Nearest food:{food_distance.index(min(food_distance))},{min(food_distance)}")

    for x in safe_moves:
        nearest_food = game_state['board']['food'][food_distance.index(min(food_distance))]
        if my_head['x'] < nearest_food['x'] and is_move_safe['up'] in safe_moves:
            next_move = 'up'
        elif my_head['x'] > nearest_food['x'] and is_move_safe['down'] in safe_moves:
            next_move = 'down'
        elif my_head['y'] < nearest_food['y'] and is_move_safe['right'] in safe_moves:
            next_move = 'right'
        elif my_head['y'] > nearest_food['y'] and is_move_safe['left'] in safe_moves:
            next_move = 'left'
        else:
            next_move = random.choice(safe_moves)

        
    

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})