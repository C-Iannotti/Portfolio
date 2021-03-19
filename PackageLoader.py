class PackageLoader:
    """Keeps track of packages that have not been delivered and loads them."""
    def __init__(self, packages=[]):
        """ Creates a bucket data structure to hold packages and adds initialized packages.
        packages_in_inventory is a bucket data structure that stores packages that have deadlines(0),
        packages that need to be delivered together(2), and all other packages(1).
        inventory_amount keeps track of how many packages are left to load.
        """
        self.packages_in_inventory = [[], [], []]
        self.inventory_amount = 0

        for package in packages:
            self.add_package(package)

    def add_package(self, package):
        """Adds a package to inventory
        First, finds the bucket the package belongs in.
        Then, adds the package to the bucket and sorts with insertion sort by deadline(0) and address(1)
        Finally, increments the inventory_amount
        """
        bucket = 0
        if package.deliver_deadline == 'EOD':
            bucket = 1
        if package.note.startswith('Delivered with'):
            bucket = 2

        if len(self.packages_in_inventory[bucket]) == 0 and bucket != 2:
            self.packages_in_inventory[bucket].append(package)
        elif bucket == 0:
            self.packages_in_inventory[bucket].append(package)

            i = 1
            while i < len(self.packages_in_inventory[bucket]):
                j = i
                while (j > 0) and (self.packages_in_inventory[bucket][j - 1].deliver_deadline
                                   > self.packages_in_inventory[bucket][j].deliver_deadline):
                    temp = self.packages_in_inventory[bucket][j - 1]
                    self.packages_in_inventory[bucket][j - 1] = self.packages_in_inventory[bucket][j]
                    self.packages_in_inventory[bucket][j] = temp
                    j -= 1

                i += 1
        elif bucket == 1:
            self.packages_in_inventory[bucket].append(package)

            i = 1
            while i < len(self.packages_in_inventory[bucket]):
                j = i
                while (j > 0) and (self.packages_in_inventory[bucket][j - 1].address
                                   > self.packages_in_inventory[bucket][j].address):
                    temp = self.packages_in_inventory[bucket][j - 1]
                    self.packages_in_inventory[bucket][j - 1] = self.packages_in_inventory[bucket][j]
                    self.packages_in_inventory[bucket][j] = temp
                    j -= 1

                i += 1
        else:
            deliver_with = package.note[15:].split(', ')
            found = False

            for i, package_group in enumerate(self.packages_in_inventory[bucket]):
                for j, item in enumerate(package_group):
                    if type(item) is str and package.key == int(item):
                        self.packages_in_inventory[bucket][i][j] = package
                        found = True

            if not found:
                self.packages_in_inventory[bucket].append(deliver_with)
                self.packages_in_inventory[bucket][-1].append(package)

        self.inventory_amount += 1

    def load_truck(self, truck, time):
        """Loads packages in inventory onto a truck.
        Takes a truck and a time and sets the current time on the truck to the time.
        Unloads the truck of any packages still the truck and adds them to inventory.
        Loads packages in inventory onto the truck until the truck is full; first
        loads packages that need to be delivered together if there is room for all of them,
        then loads packages with deadlines, and finally loads the rest of packages.
        Each package loaded is removed form inventory.
        Before loading, the notes are checked to make certain that they cen be loaded onto
        the truck.
        """
        truck.time = time
        index = 0
        loaded_indices = []

        for i, package in enumerate(truck.packages):
            if package is not None:
                self.add_package(package)
                truck.packages[i] = None

        for i, package_group in enumerate(self.packages_in_inventory[2]):
            if len(package_group) + index < len(truck.packages):
                for package in package_group:
                    truck.packages[index] = package
                    index += 1
                    package.truck = truck.number
                    package.time_loaded = truck.time
                    self.inventory_amount -= 1
                loaded_indices.insert(0, i)

        for num in loaded_indices:
            self.packages_in_inventory[2].pop(num)
            loaded_indices = []

        for i, package in enumerate(self.packages_in_inventory[0]):
            if index < len(truck.packages):
                if package.note.startswith('truck') and int(package.note[-1]) != truck.number:
                    pass
                elif package.note.startswith('Delayed') and package.note[-5:] > time:
                    pass
                else:
                    truck.packages[index] = package
                    index += 1
                    package.truck = truck.number
                    package.time_loaded = truck.time
                    loaded_indices.insert(0, i)
                    self.inventory_amount -= 1

        for num in loaded_indices:
            self.packages_in_inventory[0].pop(num)
        loaded_indices = []

        for i, package in enumerate(self.packages_in_inventory[1]):
            if index < len(truck.packages):
                if package.note.startswith('truck') and int(package.note[-1]) != truck.number:
                    pass
                elif package.note.startswith('Delayed') and package.note[-5:] > time:
                    pass
                else:
                    truck.packages[index] = package
                    index += 1
                    package.truck = truck.number
                    package.time_loaded = truck.time
                    loaded_indices.insert(0, i)
                    self.inventory_amount -= 1

        for num in loaded_indices:
            self.packages_in_inventory[1].pop(num)
