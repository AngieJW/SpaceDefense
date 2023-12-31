import random
import math

# define fleet class
class Fleet:
    """
    Represents a fleet consisting of vessels, half support and half offensive crafts.

    Attributes:
        size (int): number of ships in the fleet.
        ships (list): list of Vessel objects representing the fleet's ships.

    Methods:
        create_fleet(): creates a fleet of size ships, half support and half offensive crafts.
    """
    def __init__(self, size):
        self.size = size
        self.ships = []
        self.create_fleet()

    # create fleet of size ships
    def create_fleet(self):
        # contains size ships, half support half offensive crafts (random vessel_types for each craft)
        for i in range(self.size):
            if i < self.size/2:
                self.ships.append(Vessel(random.choice(Vessel.OFFENSIVE_CRAFT)))
            else:
                self.ships.append(Vessel(random.choice(Vessel.SUPPORT_CRAFT)))
        # set 1 commandship per fleet, a battleship from the list
        for ship in self.ships:
            if ship.vessel_type == 'battleship':
                ship.commandship = True
                break

# define vessel class
class Vessel:
    """
    Represents a vessel.

    Attributes:
        vessel_type (str): type of the vessel ('battleship', 'refueling', ...).
        coordinates (tuple): current coordinates of the vessel.
        commandship (bool): True if the vessel is the command ship of the fleet.
        available (bool): True if the vessel is available for pairing, False if the vessel is adjacent to its paired ship.
        medical_unit (bool): True if the vessel has one medical unit. True when support craft.
        cannons (int): number of cannons on offensive craft (0 for support craft).
        shield (bool): True if the vessel's shields are raised, False by default.

    Methods:
        move(x, y): moves the vessel to coordinates (x, y).
        attack(): fires the vessel's cannons.
        raise_shield(): raises the vessel's shields.
    """
    OFFENSIVE_CRAFT = ['battleship', 'cruiser', 'destroyer']
    SUPPORT_CRAFT = ['refueling', 'mechanical assistance', 'cargo']

    def __init__(self, vessel_type):
        self.vessel_type = vessel_type
        self.coordinates = (0, 0)
        self.commandship = False
        self.available = True # to pair support and offensive ships

        if self.vessel_type in self.SUPPORT_CRAFT:
            # has medical unit
            self.medical_unit = True
            # task command = vessel_type
            self.task = self.vessel_type
        else:
            # has cannons : battleships 24, cruisers 12, destroyers 6
            if self.vessel_type == 'battleship':
                self.cannons = 24
            elif self.vessel_type == 'cruiser':
                self.cannons = 12
            elif self.vessel_type == 'destroyer':
                self.cannons = 6
            else:
                self.cannons = 0
            self.shield = False  # Initialize shield

    # move command
    def move(self, x, y):
        self.coordinates = (x,y)

    # attack command only for offensive craft, to fire all its cannons
    def attack(self):
        if self.vessel_type in self.OFFENSIVE_CRAFT:
            if self.cannons > 0:
                print(f"{self.vessel_type} fired {self.cannons} cannons")
                self.cannons = 0
            else:
                print(f"{self.vessel_type} has no cannons left")
        else:
            print(f"{self.vessel_type} is not an offensive craft")

    # raise shield command
    def raise_shield(self):
        if self.vessel_type in self.OFFENSIVE_CRAFT:
            self.shield = True
            print('Shields raised!')
        else:
            print(f"{self.vessel_type} is not an offensive craft")


fleet = Fleet(50)

for i, ship in enumerate(fleet.ships, 1):
    # find the commandship
    if ship.commandship:
        print(f"Ship {i}: {ship.vessel_type} (Command Ship)")
    # print rest of the ships
    else:
        print(f"Ship {i}: {ship.vessel_type}")

# define class for grid
class Grid:
    """
    Represents a two-dimensional grid with specified length and height.

    Attributes:
        length (int): length (number of rows) of the grid.
        height (int): height (number of columns) of the grid.
        grid (list): two-dimensional list representing the grid, initialized with '_'.

    Methods:
        create_grid(): creates the grid with specified length and height.
        is_empty(x, y): returns True if the grid spot at coordinates (x, y) is empty.
        place_ship(x, y, vessel_type): places a vessel_type ship at coordinates (x, y).
        remove_ship(x, y): removes the ship at coordinates (x, y).
        __str__(): returns a string representation of the grid.
    """

    def __init__(self, length, height):
        if length > 100 or height > 100:
            raise ValueError("Grid maximum size is 100x100")

        self.length = length
        self.height = height
        self.ship_letter = {
            'battleship': 'B',
            'cruiser': 'C',
            'destroyer': 'D',
            'refueling': 'R',
            'mechanical assistance': 'M',
            'cargo': 'O'
        }
        self.create_grid()

    # format grid with two-dimensional layout
    def create_grid(self):
        self.grid = []
        for i in range(self.length):
            self.grid.append([])
            for j in range(self.height):
                self.grid[i].append('_')

    # bool if spot is empty
    def is_empty(self, x, y):
        if self.grid[x][y] == '_':
            return True
        else:
            return False

    def place_ship(self, x, y, vessel_type):
        if self.is_empty(x, y):
            # assign ship letter to grid spot
            self.grid[x][y] = self.ship_letter.get(vessel_type, '_')

    def remove_ship(self, x, y):
        self.grid[x][y] = '_'

    def __str__(self):
        grid_str = ""
        for row in self.grid:
            grid_str += " ".join(row) + "\n"
        return grid_str

grid = Grid(100, 100)

# place each ship from fleet in random positions where is_empty
for ship in fleet.ships:
    while True:
        x = random.randint(0, grid.length - 1)
        y = random.randint(0, grid.height - 1)
        if grid.is_empty(x, y):
            grid.place_ship(x, y, ship.vessel_type)
            ship.move(x, y)
            break

# print(grid)

# generate pairs of ships :
        #   get location of available offensive ship
        #   get its adjacent is_empty spot in the grid, check row first then column
        #   find closest support ship available
        #   move support ship to adjacent spot
        #   set both ships as unavailable
        #   update grid
        #   repeat until all ships are paired
print( "Pairing ships...")

# get location of available offensive ship
for ship in fleet.ships:
    if ship.available and ship.vessel_type in Vessel.OFFENSIVE_CRAFT:
        x, y = ship.coordinates
        # find adjacent is_empty spot in the grid, check row first then column
        if x < grid.length - 1 and grid.is_empty(x + 1, y):
            available_spot = (x + 1, y)
        elif x > 0 and grid.is_empty(x - 1, y):
            available_spot = (x - 1, y)
        elif y < grid.height - 1 and grid.is_empty(x, y + 1):
            available_spot = (x, y + 1)
        elif y > 0 and grid.is_empty(x, y - 1):
            available_spot = (x, y - 1)
        else:
            print(f"No available spot for support ship next to offensive ship{ship.vessel_type} at {x}, {y}")

        # find closest support ship available
        closest_support_ship = None
        closest_distance = math.inf
        for support_ship in fleet.ships:
            if support_ship.available and support_ship.vessel_type in Vessel.SUPPORT_CRAFT:
                x2, y2 = support_ship.coordinates
                # calculate distance between offensive ship and support ship - euclidean coordinates
                distance = math.sqrt((x2 - x)**2 + (y2 - y)**2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_support_ship = support_ship

        # get coordinates of closest support ship to remove it from grid
        closest_support_ship_x, closest_support_ship_y = closest_support_ship.coordinates

        # move support ship to available spot
        closest_support_ship.move(available_spot[0], available_spot[1])

        # set both ships as unavailable
        ship.available = False
        closest_support_ship.available = False

        # update grid : new coordinates + remove former coordinates of support ship
        grid.place_ship(available_spot[0], available_spot[1], closest_support_ship.vessel_type)
        grid.remove_ship(closest_support_ship_x, closest_support_ship_y)

# print grid with paired ships
print(grid)
