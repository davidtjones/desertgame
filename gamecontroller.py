import random
import code
class GameController:
    def __init__(self, grid, agents):
        self.agents = agents
        self.grid = grid

        self.grid_size_x, self.grid_size_y = self.grid.get_dimensions()

        # set agents in grid:
        for agent in self.agents:
            # CIA Agent gets 20% head start
            if agent.occupation == "CIA Agent":
                position = (round(self.grid_size_x * .2),
                            random.randint(0, self.grid_size_y-1))

            if agent.occupation == "Thug":
                position = (0, random.randint(0, self.grid_size_y-1))
                        
            agent.set_tile(self.grid.get_tile(position[0], position[1]))
                                   
                
    def __call__(self, iteration):

        # Agents need to make decisions based on beliefs (act or move)
        for agent in self.agents:

            # Update Agent Beliefs
            agent_los = agent.status["line_of_sight"]
            surroundings = self.grid.get_subgrid(agent.get_position(), agent_los)

            agent.update_beliefs(surroundings)

        for agent in self.agents:
            # now that all beliefs have updated, let agents fulfill desires
            agent.move(self.grid)

    def check_game_conditions(self):
        for agent in self.agents:
            if agent.occupation == "CIA Agent":
                cia_position = agent.get_position()
                if agent.get_position()[0] == self.grid_size_x-1:
                    print("You arrived safely")
                    return "win"

            if agent.occupation == "Thug":
                thug_position = agent.get_position()
                delta_x = abs(thug_position[0]-cia_position[0])
                delta_y = abs(thug_position[1]-cia_position[1])
                if ((delta_x == 1 and delta_y < 2) or
                    (delta_x < 2 and delta_y == 1) or
                    (delta_x == 0 and delta_y == 0)):
                    print("You got caught!")
                    return "lose"

        
