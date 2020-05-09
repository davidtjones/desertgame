import code
import random
import textwrap 
from text import *

class Character:
    def __init__(self, name):
        self.status = {
            "speed": 1,
            "fatigue": 0.0,
            "line_of_sight": 3
            }

        self.inventory = []
        self.name = name
        self.occupation = "NoOccupation"
        self.symbol = "N"
        self.tile = None
        self.surroudings = None

        
    def show_status(self):
        print(f"Fatigue: {self.status['fatigue']}")

    def update_status(self, status_field, delta):
        self.status[status_field] += delta

    def set_tile(self, new_tile):
        if self.tile:
            self.tile.set_symbol(" ")
            
        self.tile = new_tile
        self.tile.set_symbol(self.symbol)
        self.tile.agent = self

    def get_position(self):
        return self.tile.coordinates
        
    def act(self):
        pass
    
    def move(self, grid):
        pass

    def update_beliefs(self, surroundings):
        self.surroundings = surroundings
    
    def run(self):
        pass


class Agent(Character):
    def __init__(self, name):
        super().__init__(name)
        self.name = name
        self.occupation = "CIA Agent"
        self.symbol = "O"
        self.status["line_of_sight"] = 9
    
    def move(self, grid):
        # desire 1:
        # reach end of map as quickly as possible
        # always move left unless thugs are nearby, in which case maximize distance
        # use gun if they get too close
        self.symbol = "O"
        position = self.get_position()
        surroundings = self.surroundings.tiles
        # check for thugs in surroundings
        move_total = 0
        for row in surroundings:
            for tile in row:
                if tile.symbol == "X":
                    # thug detected!
                    thug_position = tile.coordinates
                    deltax = thug_position[0] - position[0]
                    deltay = thug_position[1] - position[1]
                    distance = (abs(deltax)**2 + abs(deltay)**2)**.5
                    if distance < 5:
                        # need to take more drastic measures!
                        # use the gun
                        print("CIA Operative: Using the gun")

                        thugs_beliefs = tile.agent.surroundings.tiles
                        for row in thugs_beliefs:
                            for tile2 in row:
                                if tile2.symbol == "O":
                                    real_c = tile2.coordinates
                                    best = real_c
                                    best_d = 0
                                    # find furthest tile in thug beliefs:
                                    for row in thugs_beliefs:
                                        for tile3 in row:
                                            curr_c = tile3.coordinates
                                            v1 = real_c[0] - curr_c[0]
                                            v2 = real_c[1] - curr_c[1]
                                            d = abs(v1)**2 + abs(v2)**2
                                            d = d**.5
                                            if d > best_d:
                                                best = curr_c
                                                best_d = d
                                    ruse_tile = grid.get_tile(best[0], best[1])
                                    ruse_tile.symbol = "O"
                                    self.symbol = " "
                                                      
                                    
                    else:
                        move_x = 0
                        move_y = 0
                        
                        # want to maximize this without losing progress... up/down preferrable
                        move_total = self.status["speed"]
                        if abs(thug_position[1] - position[1]+1) > abs(deltay):
                            move_y = 1
                        elif abs(thug_position[1] - position[1]-1) > abs(deltay):
                            move_y = -1
                        else:
                            # neither or these moves are working, try moving back
                            move_x = -1
                        new_position = (position[0]+move_x, position[1] + move_y)
                        self.set_tile(grid.get_tile(new_position[0], new_position[1]))
                        move_total = 1
                    
        if move_total != 1:
            # continue on!
            new_position = position[0]+self.status["speed"], position[1]
            self.set_tile(grid.get_tile(new_position[0], new_position[1]))
        
                      

    
class Thug(Character):
    def __init__(self, name):
        super().__init__(name)
        self.status["speed"] = 4
        self.status["line_of_sight"] = 4
        self.name = name
        self.occupation = "Thug"
        self.symbol = "X"
        self.direction_up = 1
        self.direction_across = 1

        
    def move(self, grid):
        position = self.get_position()
        surroundings = self.surroundings.tiles
        # have thug move in zig-zag pattern
        max_x, max_y = grid.get_dimensions()
        if position[0] == 0: self.direction_across = 1
        if position[0] == max_x-1: self.direction_across = -1
        if position[1] == 0: self.direction_up = 1
        if position[1] == max_y-1: self.direction_up = -1
        
        # check for cia operative nearby:
        found_agent = False
        for row in surroundings:
            for tile in row:
                if tile.symbol == "O":
                    print("Thug: I have found the operative!")
                    agent_position = tile.coordinates
                    deltax = agent_position[0] - position[0]
                    deltay = agent_position[1] - position[1]
                    move_x = 0
                    move_y = 0
                    move_total = self.status["speed"]
                    if deltax < 0:
                        direction_across = -1
                        deltax = abs(deltax)
                    else:
                        direction_across = 1
                    if deltay < 0:
                        direction_up = -1
                        deltay = abs(deltay)
                    else:
                        direction_up = 1

                    while move_x < deltax and move_total > 0:
                        move_x += (1 * direction_across)
                        move_total -= 1
                    while move_y < deltay and move_total > 0:
                        move_y += (1 * direction_up)
                        move_total -= 1
                    new_position = (position[0] + move_x, position[1] + move_y)

                    self.set_tile(grid.get_tile(new_position[0], new_position[1]))
                    found_agent = True

        if not found_agent:
            # agent wasn't found... search randomly while moving towards finish line
            print("Thug: No operative in sight...")
            move_x = 0
            move_y = 0
            move_total = self.status["speed"] - 1
            move_x += 1 * self.direction_across
            if self.direction_up == 1:
                while move_total > 0 and (move_y+position[1] < max_y-1):
                    move_y += 1 * self.direction_up
                    move_total -= 1
            else:
                while move_total > 0 and (position[1]-move_y > 0):
                    move_y += 1 * self.direction_up
                    move_total -= 1
                
            if self.direction_across == 1:
                while move_total > 0 and (move_x+position[0] < max_x-1):
                    move_x += 1 * self.direction_across
                    move_total -=1
            else:
                while move_total > 0 and (position[0]-move_x > 0):
                    move_x += 1 * self.direction_across
                    move_total -= 1
                    
            
                
            new_position = (position[0] + move_x, position[1] + move_y)

            self.set_tile(grid.get_tile(new_position[0], new_position[1]))
                
                    

                
                
                
        
