import random

# You are the admiral of a mighty space fleet of 50 vessels. Your fleet consists of two major
# types of vessels - support craft and offensive craft. Vessels can all receive a command
# that tells them to move to given coordinates.
# There are three different types of support craft - refueling, mechanical assistance and
# cargo. They all carry a medical unit. Each vessel can receive orders related to each of the
# tasks it can carry out.
# There are also three different types of offensive craft - battleships, cruisers and destroyers.
# Battleships have 24 cannons, destroyers have 12 and cruisers have 6. Each offensive craft
# can receive an attack command, which will fire all its cannons. They can also be instructed
# to raise their shields.
# Finally, the fleet has a command ship, which is where you are. The command ship is one of
# the battleships, and there is only one per fleet.

# Define a set of data structures to accurately reflect this fleet. Make sure that new types
# of vessels can be added to your fleet with minimal effort.


# Define the class for the vessels
class Vessel:
    def __init__(self, vessel_type):
        self.vessel_type = vessel_type
        self.coordinates = (0, 0)

    def __str__(self):
        return self.vessel_type

    # command to move to coordinates
    def move(self, coordinates):
        self.coordinates = coordinates

class Support(Vessel):
    def __init__(self, vessel_type, task):
        super().__init__(vessel_type)

        allowed_tasks = ["refueling", "assistance", "cargo"]
        if task not in allowed_tasks:
            raise ValueError("Task must be one of {}".format(allowed_tasks))

        self.medical_unit = True
        self.task = task

    def __str__(self):
        return self.task

class Offensive(Vessel):
    allowed_vessel_types = ["battleship", "destroyer", "cruiser"]
    cannon_numbers = {
        "battleship": 24,
        "destroyer": 12,
        "cruiser": 6
    }

    def __init__(self, vessel_type, cannons):
        super().__init__(vessel_type)
        # self.cannons = cannons  # battleships have 24, destroyers have 12, cruisers have 6
        self.shield = False

        if vessel_type not in self.allowed_vessel_types:
            raise ValueError("Vessel type must be one of {}".format(self.allowed_vessel_types))

        self.cannons = self.cannon_numbers[vessel_type]

    # command to attack
    def attack(self):
        print("Fire cannons")
        self.cannons = 0

    # command to raise shield
    def raise_shield(self):
        self.shield = True

# create a fleet of 50 vessels
fleet = []
command_ship = Offensive("CommandShip", cannons=24)
fleet.append(command_ship)
print(fleet)

for _ in range(25):
    random_task = random.choice(allowed_tasks)
    support_vessel = Support("support", random_task)
    fleet.append(support_vessel)

for _ in range(24):
    offensive_vessel = Offensive("offensive", cannons=24)
    fleet.append(offensive_vessel)


# You are taking your fleet, made up of an equal number of offensive and support ships, to
# your assigned deployment point when you are ambushed by enemy forces. Your defense
# tactic is to pair each support ship with one offensive ship in order to share the offensive
# ship's shield.
# Assuming a two-dimensional layout with a maximum size of 100x100, write some code that
# is able to represent your fleet location data and populate it with your 50 ships in random
# positions. Then, implement an algorithm that generates 25 pairs of ships, and issues the
# commands to make the pairs occupy adjacent positions on the grid by moving one or both
# ships. Your vessels need to assume this defensive formation as quickly as possible, so you
# will need to find an algorithm that gives an optimized set of pairs, but that is also quick to
# generate them


# Define the class for the grid
class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for x in range(size)] for y in range(size)]

    def place_ship(self, ship, x, y):
        self.grid[x][y] = ship
        ship.move((x, y))

# Initialize the grid
# Place the ships on the grid at random positions
# Generate pairs of ships for formation (one support + one offensive)
# Iterate through the pairs and have their positions to be in adjacent cells
# Update the grid with new positions

grid = Grid(size=100)

for ship in fleet:
    while True:
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        if grid.grid[x][y] == 0:
            grid.place_ship(ship, x, y)
            break

# Generate pairs of ships for formation (one support one offensive).
pairs = []
offensive_ships = [ship for ship in fleet if isinstance(ship, Offensive)]
support_ships = [ship for ship in fleet if isinstance(ship, Support)]

for offensive, support in zip(offensive_ships, support_ships):
    pairs.append((offensive, support))
