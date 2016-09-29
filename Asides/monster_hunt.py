# A Simple Game based on the following premise:
# A Two Dimensional Grid (x,y) holds 3 nodes, an escape_door, a monster
# and a player.
# Goal: Escape, before the monster eats you!

import random
import math
#returns size x size grid as a list of tuples
def generate_grid(size):
    grid = []
    for x in list(range(size)):
        for y in list(range(size)):
            grid_loc = x,y
            grid.append(grid_loc)
    return grid

#places the player, the door, and the monster
def setup_game(game_grid):
    player_location  = random.choice(game_grid)
    monster_location = random.choice(game_grid)
    escape_location  = random.choice(game_grid)

    #randomize board again if you have conflicts on position
    while player_location == monster_location or monster_location == escape_location or escape_location == player_location:
        player_location  = random.choice(game_grid)
        monster_location = random.choice(game_grid)
        escape_location  = random.choice(game_grid)

    return player_location,monster_location,escape_location

#moves object on board, returns tuple of new pos (x,y)
def move_object(grid_size, grid_loc, direction, step):
    x,y = grid_loc
    new_pos = 0,0
    if direction == "up":
        if y + step > grid_size:
            new_pos = (-1,-1)
            return new_pos
        else:
            new_pos = (x,y+step)
            return new_pos

    elif direction == "down":
        if y - step < 0:
            new_pos = (-1,-1)
            return new_pos
        else:
            new_pos = (x,y-step)
            return new_pos

    elif direction == "left":
        if x + step < 0:
            new_pos = (-1,-1)
            return new_pos
        else:
            new_pos = (x-1,y)
            return new_pos

    elif direction == "right":
        if x + step > grid_size:
            new_pos = (-1,-1)
            return new_pos
        else:
            new_pos = (x+1,y)
            return new_pos

def square(x):
    return x*x
#simple distance formula implementation
def calc_distance(pos1, pos2):
    x1,y1 = pos1
    x2,y2 = pos2
    #assuming pos1 -> pos2
    distance = math.sqrt(square(x2 - x1) + square(y2-y1))
    return distance

#determines which direction the monster should move
#TODO: May have a left bias bug
def AI_move(grid_size, grid_loc, step):
    chosen_direction = "left" #left default
    min_distance = 1000000
    direction_list = ["left", "right", "up", "down"]
    for direction in direction_list:
        if is_legal_move(grid_loc, direction, step, grid_size):
            candidate_distance = calc_distance(grid_loc, is_legal_move(grid_loc, direction, step, grid_size))
            if candidate_distance < min_distance:
                min_distance = candidate_distance
                chosen_direction = direction
    return chosen_direction

#determines if the move is legal, and returns the new_pos if legal
def is_legal_move(pos1,direction, step, grid_size):
    x1,y1 = pos1
    if direction == "left":
        if x1 - 1 < 0:
            return False
        else:
            return x1-1, y1
    if direction == "right":
        if x1 + 1 > grid_size:
            return False
        else:
            return x1+1, y1
    if direction == "up":
        if y1 + 1 > grid_size:
            return False
        else:
            return x1,y1+1
    if direction == "down":
        if y1 - 1 < 0:
            return False
        else:
            return x1,y1-1

def main_game():
    print("What is the size of the gameboard, enter a single value (e.g 2x2)")
    size = int(input())
    grid = generate_grid(size)

    print("Setting up Game Board")
    player,monster,door = setup_game(grid)
    print("Player is located {}, Monster is located {}, Escape is located {}".format(player,monster,door))

    while player != door:
        print("enter a direction to move your character! (e.g. left,right,up,down)")
        direction = input()
        player = move_object(size, player, direction, 1)
        print("characters current location is: {}".format(player))
        monster_direction = AI_move(size, monster, 1)
        monster = move_object(size,monster,monster_direction,1)
        print("monster is now located at: {}".format(monster))
        if monster == player:
            print("The monster has eaten you! Thank you for playing")
            break
    else:
        print("Congratulations you have escaped!")
