import code

class Tile:
    # Base class for tiles in game
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.agent = None  # keep track of which agent is here
        self.symbol = " "
        
    def __str__(self):
        return f"|({self.symbol})|"

    def get_agents(self):
        if agent:
            return (agent.occupation, agent.name)

    def set_symbol(self, symbol):
        self.symbol = symbol
                    

class SubGrid:
    def __init__(self, tiles):
        self.tiles = tiles

    def print_subgrid(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                print(self.tiles[i][j], end="")
            print()



class Grid:
    def __init__(self, x_length, y_length):
        self.x_length = x_length
        self.y_length = y_length

        # Initialize Empty Grid
        self.tiles = [None] * x_length
        for i in range(self.x_length):
            self.tiles[i] = [None] * self.y_length

        # Fill grid with tiles
        for i in range(self.x_length):
            for j in range(self.y_length):
                self.tiles[i][j] = Tile(i, j)
            

    def get_tile(self, x, y):
        return self.tiles[x][y]

        
    def get_subgrid(self, origin, radius):
        # origin is (x,y) tuple denoting center of subset
        # radius is int
        x, y = origin
        # we can create a diamond subgrid but it's important that the slices
        # take into account the current position if near the top of the map
        # the slices let us make a nice diamond

        left_bound = x-radius if x-radius > 0 else 0
        right_bound = x+radius+1 if x+radius+1 < self.x_length else self.x_length
        upper_bound = y+radius+1 if y+radius+1 < self.y_length else self.y_length
        lower_bound = y-radius if y-radius > 0 else 0
        

        subgrid = self.tiles[left_bound:right_bound]
        for i in range(len(subgrid)):
            subgrid[i] = subgrid[i][lower_bound:upper_bound]
        
        new_subgrid = SubGrid(subgrid)

        return new_subgrid

    def get_dimensions(self):
        return (self.x_length, self.y_length)


    def print_grid(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                print(self.tiles[i][j], end="")
            print()



