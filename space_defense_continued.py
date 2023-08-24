import random

# WAS MADE AFTER TEST ALLOTED TIME
# TO FIX THE MISTAKES
#

# Define the classes for the vessels
class Vessel:
    def __init__(self, vessel_type):
        self.vessel_type = vessel_type
        self.coordinates = (0, 0)

    def __str__(self):
        return self.vessel_type

    # command to move to coordinates
    def move(self, x , y ):
        self.coordinates = (x, y)

class Support(Vessel):
    allowed_tasks = ["refueling", "assistance", "cargo"]

    def __init__(self, vessel_type, task):
        super().__init__(vessel_type)

        if task not in Support.allowed_tasks:
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

    def __init__(self, vessel_type):
        super().__init__(vessel_type)
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

    def __str__(self):
        return self.vessel_type

# create a fleet of 50 vessels
fleet = []
# print("fleet created")

command_ship = Offensive("battleship")
command_ship.vessel_type = "CommandShip"
fleet.append(command_ship)
# print("CommandShip added")
# print(fleet)


allowed_tasks = ["refueling", "assistance", "cargo"]

for _ in range(25):
    random_task = random.choice(allowed_tasks)
    support_vessel = Support("support", random_task)
    fleet.append(support_vessel)

print("support vessels added")

for _ in range(24):
    random_offensive = random.choice(Offensive.allowed_vessel_types)
    offensive_vessel = Offensive(random_offensive)
    fleet.append(offensive_vessel)

print("offensive vessels added")

print("fleet created")
print(len(fleet))
# print(fleet)


# Define the class for the grid
class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [[0 for x in range(size)] for y in range(size)]

    def place_ship(self, ship, x, y):
        self.grid[x][y] = ship
        ship.move(x, y)


# Initialize the grid
# Place the ships on the grid at random positions

grid = Grid(size=100)

for ship in fleet:
    while True:
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        if grid.grid[x][y] == 0:
            grid.place_ship(ship, x, y)
            break

# Generate pairs of ships for formation (one support one offensive)
pairs = []
offensive_ships = [ship for ship in fleet if isinstance(ship, Offensive)]
support_ships = [ship for ship in fleet if isinstance(ship, Support)]

for offensive, support in zip(offensive_ships, support_ships):
    pairs.append((offensive, support))

print(pairs)

# Iterate through the pairs and have their positions to be in adjacent cells, the offensive ship doesn't move, only the support ship
for offensive, support in pairs:
    o_x, o_y = offensive.coordinates
    s_x, s_y = support.coordinates

    # Define possible adjacent positions around the offensive ship
    possible_positions = [
        (o_x, o_y + 1),
        (o_x, o_y - 1),
        (o_x + 1, o_y),
        (o_x - 1, o_y)
    ]

    for s_x, s_y in possible_positions:
        if (
            0 <= s_x < 100
            and 0 <= s_y < 100
            and grid.grid[s_x][s_y] == 0
        ):
            grid.place_ship(support, s_x, s_y)
            break
    else:
        # move the both ships for them to be adjacent
        grid.place_ship(offensive, s_x, o_y + 1)




# Update the grid with new positions, print grid where the ships are X for offensive and S for support, 0 for empty cells
for row in grid.grid:
    print(" ".join(
        str(cell).ljust(10) if cell != 0 else "0".ljust(10)
        for cell in row
    ))
