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

import math
from os import link
import random
from re import A
from readline import replace_history_item
from sys import flags
import typing

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

    #get free surface
    totalSurface = game_state['board']['width']*game_state['board']['height']
    takenSurface = 0
    for snake in game_state['board']['snakes']:
        for body in snake['body']:
            takenSurface=takenSurface+1
    freeSurface = totalSurface - takenSurface
    print(f"Total:{totalSurface}, Taken:{takenSurface}, Free:{freeSurface}")

    map = []
    for y in range(game_state['board']['height']):
        map1 = ['a'] * game_state['board']['height']
        for x in range(game_state['board']['width']):
            for snake in game_state['board']['snakes']:
                for body in snake['body']:
                    if body['x'] == x and body['y'] == y:
                        map1[x] = 'b'
                        break
        map.append(map1)

    def mapoutput(mapinput) -> str:
        output = ""
        for x in range(len(mapinput)):
            for y in range(len(mapinput[x])):
                output = output + str(mapinput[x][y])
            output = output + "\n"
        return output

    def floodfill(matrix, x, y):
        if matrix[x][y] == "a":  
            matrix[x][y] = "c" 
            if x > 0:
                floodfill(matrix,x-1,y)
            if x < len(matrix[y]) - 1:
                floodfill(matrix,x+1,y)
            if y > 0:
                floodfill(matrix,x,y-1)
            if y < len(matrix) - 1:
                floodfill(matrix,x,y+1)

    floodfill(map, my_head['x'], my_head['y'])
    print(mapoutput(map))

    aCount = 0
    cCount = 0
    for x in map:
        aCount = aCount + x.count('a')
        cCount = cCount + x.count('c')
    print(aCount,cCount)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    food_distance = []
    for x in food:
        food_distance.append(math.sqrt(math.pow(my_head['x']-x['x'],2)+math.pow(my_head['y']-x['y'],2)))

    nearest_food = game_state['board']['food'][food_distance.index(min(food_distance))]
    print(f"snake:{my_head}\nnearest fruit:{nearest_food}")
    
    next_move = ""
    if my_head['x'] == nearest_food['x']:
        if my_head['y'] < nearest_food['y']:
            next_move = "up"
        elif my_head['y'] > nearest_food['y']:
            next_move = 'down'
    elif my_head['x'] < nearest_food['x']:
        next_move = "right"
    elif my_head['x'] > nearest_food['x']:
        next_move = "left"

    #Rechts
    if not my_head['x']==board_width-1:
        rechts = map[my_head['y']][my_head['x']+1]
    else:
        rechts = ''
    #links
    if not my_head['x']==0:
        links = map[my_head['y']][my_head['x']-1]
    else:
        links = ''
    #oben
    if not my_head['y']==board_height-1:
        oben = map[my_head['y']+1][my_head['x']]
    else:
        oben = ''
    #unten
    if not my_head['y']==0:
        unten = map[game_state['you']['body'][0]['y']-1][game_state['you']['body'][0]['x']]
    else:
        unten = ''
    bac = [oben, unten, links, rechts]
    print(f'oben:{oben}, unten: {unten}, links:{str(links)}, rechts:{str(rechts)}')

    if not next_move in safe_moves:
        if aCount > cCount:
            if oben == 'a' and 'up' in safe_moves:
                next_move = 'up'
            elif unten == 'a' and 'down' in safe_moves:
                next_move = 'down'
            elif rechts == 'a' and 'right' in safe_moves:
                next_move = 'right'
            elif links == 'a' and'left' in safe_moves:
                next_move = 'left'
        elif cCount > aCount:
            if oben == 'c' and'up' in safe_moves:
                next_move = 'up'
            elif unten == 'c' and'down' in safe_moves:
                next_move = 'down'
            elif rechts == 'c' and'right' in safe_moves:
                next_move = 'right'
            elif links == 'c' and'left' in safe_moves:
                next_move = 'left'
        elif cCount == aCount:
            next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}
# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})