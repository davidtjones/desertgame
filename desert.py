
from pyfiglet import Figlet
import textwrap

from character import *

from grid import Grid
from gamecontroller import GameController

# Load game objects
grid = Grid(40, 20)
agent = Agent("Bullock")
thug = Thug("Harvey")
# monsters = Monsters()
agents = [agent, thug]
gc = GameController(grid, agents)

# Show intro prompt
# intro_prompt()

# Start game loop

iteration = 0
print("Agent  -----  Thug")
while True:
    gc(iteration)
    print(f"{agent.get_position()}      {thug.get_position()}")
    game_over = gc.check_game_conditions()  # check for win/lose conditions

    if game_over:
        break
    iteration += 1
    


	
