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


# define fleet class
class Fleet:
    """
    Represents a fleet consisting of support and offensive crafts.

    Attributes:
        size (int): number of ships in the fleet.
        ships (list): list of Vessel objects representing the fleet's ships.
    """

    OFFENSIVE_CRAFT = ['battleship', 'cruiser', 'destroyer']
    SUPPORT_CRAFT = ['refueling', 'mechanical assistance', 'cargo']

    def __init__(self, size):
        self.size = size
        self.ships = []
        self.create_fleet()

    # create fleet of size ships
    def create_fleet(self):
        # contains size ships, half support half offensive crafts (random vessel_types for each craft)
        for i in range(self.size):
            if i < self.size/2:
                self.ships.append(Vessel(random.choice(self.OFFENSIVE_CRAFT)))
            else:
                self.ships.append(Vessel(random.choice(self.SUPPORT_CRAFT)))
        # set 1 commandship per fleet, a battleship from the list
        for ship in self.ships:
            if ship.vessel_type == 'battleship':
                ship.commandship = True
                break



# define vessel class
class Vessel:
    """
    Represents a vessel in the fleet.

    Attributes:
        vessel_type (str): type of the vessel ('battleship', 'refueling', ...).
        coordinates (tuple): current coordinates of the vessel.
        commandship (bool): True if the vessel is the command ship of the fleet.
        medical_unit (bool): True if the vessel has one medical unit. True when support craft.
        cannons (int): number of cannons on offensive craft (0 for support craft).
        shield (bool): True if the vessel's shields are raised, False by default.
        available (bool): True if the vessel is available for pairing, False if the vessel is adjacent to its paired ship.
    """

    def __init__(self, vessel_type):
        self.vessel_type = vessel_type
        self.coordinates = (0, 0)
        self.commandship = False
        self.available = True # to pair support and offensive ships

        if self.vessel_type in Fleet.SUPPORT_CRAFT:
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

    #     attack command to fire all its cannons
    def attack(self):
        self.cannons = 0
        print('Firing cannons!')

    # raise shield command
    def raise_shield(self):
        self.shield = True
        print('Shield raised!')


fleet = Fleet(50)

for i, ship in enumerate(fleet.ships, 1):
    # find the commandship
    if ship.commandship:
        print(f"Ship {i}: {ship.vessel_type} (Command Ship)")
    # print the rest of the ships
    else:
        print(f"Ship {i}: {ship.vessel_type}")


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

# class for grid
# size
# place each ship in random positions where empty?

# display grid with ships O for offensive - S for support - _ for empty

# generate pairs of ships, where ships are closest to each other
# loop :
#   1 get location of available offensive ship
#   2 find closest support ship available
#   3 move support ship next to offensive one
#   4 set ships as unavailable

# display grid
