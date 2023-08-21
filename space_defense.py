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
        self.medical_unit = True
        self.task = task # refueling, mechanical assistance, cargo

    def __str__(self):
        return self.task


class Offensive(Vessel):
    def __init__(self, vessel_type, cannons):
        super().__init__(vessel_type)
        self.cannons = cannons # battleships have 24, destroyers have 12, cruisers have 6
        self.shield = False

    # command to attack
    def attack(self):
        print("Fire cannons")
        self.cannons = 0

    # command to raise shield
    def raise_shield(self):
        self.shields = True


fleet = []
command_ship = Offensive("CommandShip", (0, 0), cannon_count=24)
fleet.append(command_ship)
