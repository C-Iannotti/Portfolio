from math import ceil


class Truck:
    """Creates a truck to hold packages and deliver them.
    Current_num keeps track of the number of the truck"""
    current_num = 0

    def __init__(self, location, mph=18, capacity=16):
        """Creates a truck based on the arguments.
        Args:
            location, used to initialize the truck at a location
            mph, how fast the truck can travel in miles per hour
            capacity, how many packages the truck can hold
        number is the number of the truck
        packages holds the packages and is initialized with each package as None
        """
        Truck.current_num += 1
        self.number = Truck.current_num
        self.time = '00:00'
        self.mph = mph
        self.miles_traveled = 0
        self.packages = []
        self.current_location = location

        for num in range(capacity):
            self.packages.append(None)

    def travel_path(self, g, path):
        """Makes the truck follow a path and deliver packages along it.
        For each location in the path, the truck travels there, updates
        the current time and delivers packages with the location address and
        updates their time delivered."""
        current_hour = int(self.time[0:2])
        current_min = int(self.time[-2:])

        for loc in range(len(path) - 1):
            dist = g.distances[(path[loc], path[loc + 1])]
            self.miles_traveled += dist

            current_min += ceil(dist / (self.mph / 60))
            current_hour += current_min // 60
            current_min = current_min % 60

            for i, package in enumerate(self.packages):
                if package is not None and package.address == path[loc + 1].address:
                    time = str(current_hour).zfill(2) + ':' + str(current_min).zfill(2)
                    package.time_delivered = time
                    self.packages[i] = None

        self.current_location = path[-1]
        self.time = str(current_hour).zfill(2) + ':' + str(current_min).zfill(2)
