# First Name: Conner
# Last Name: Iannotti
# Student ID: 001363048

from Map import Map, Location
from Truck import Truck
from PackageLoader import PackageLoader
from ChainingHashTable import ChainingHashTable
from Package import Package
import csv

packages = ChainingHashTable()
area_map = Map()

# Adds each package to packages.
with open('WGUPS Package File.csv') as package_file:
    package_file_reader = csv.reader(package_file)
    next(package_file_reader)
    for row in package_file_reader:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        packages.insert(package)

# Creates locations for the map and adds edges between them.
with open('WGUPS Distance Table.csv') as map_file:
    map_file_reader = csv.reader(map_file)
    next(map_file_reader)
    location_row = next(map_file_reader)
    locations = []

    for i, location in enumerate(location_row):
        new_location = Location(location)
        area_map.add_location(new_location)
        locations.append(new_location)

        if i == 0:
            area_map.center = new_location

    for i, row in enumerate(map_file_reader):
        for j, location in enumerate(locations):
            if row[j] != '':
                area_map.add_undirected_edge(locations[i], locations[j], float(row[j]))

# Corrects the package that is known to have incorrect information, and is treated as delayed.
package_to_correct = packages.search(9)
if package_to_correct is not None:
    package_to_correct.address = '410 S State St'
    package_to_correct.city = 'Salt Lake City'
    package_to_correct.state = 'UT'
    package_to_correct.add_zip = '84111'

# Initializes trucks.
truck_1 = Truck(area_map.center)
truck_2 = Truck(area_map.center)

# Initializes the package loader with all packages.
package_loader = PackageLoader(packages.get_all_items())

# Sets each truck's time to the time they will leave the Hub.
truck_1.time = '08:00'
truck_2.time = '09:05'

# Loads trucks.
package_loader.load_truck(truck_1, truck_1.time)
package_loader.load_truck(truck_2, truck_2.time)

# Delivers packages on truck 1.
while truck_1.packages.count(None) < len(truck_1.packages):
    next_location = None
    package_address = None
    for package in truck_1.packages:
        if package is not None:
            package_address = package.address
            break

    for location in area_map.adjacency_list.keys():
        if location.address == package_address:
            next_location = location
            break

    truck_1.travel_path(area_map, area_map.find_path(truck_1.current_location, next_location))

# Delivers packages on truck 2.
while truck_2.packages.count(None) < len(truck_2.packages):
    next_location = None
    package_address = None
    for package in truck_2.packages:
        if package is not None:
            package_address = package.address
            break

    for location in area_map.adjacency_list.keys():
        if location.address == package_address:
            next_location = location
            break

    truck_2.travel_path(area_map, area_map.find_path(truck_2.current_location, next_location))
# Returns truck 2 to Hub.
truck_2.travel_path(area_map, area_map.find_path_to_center(truck_2.current_location))

# Loads truck 2.
package_loader.load_truck(truck_2, truck_2.time)

# Delivers packages on truck 2.
while truck_2.packages.count(None) < len(truck_2.packages):
    next_location = None
    package_address = None
    for package in truck_2.packages:
        if package is not None:
            package_address = package.address
            break

    for location in area_map.adjacency_list.keys():
        if location.address == package_address:
            next_location = location
            break

    truck_2.travel_path(area_map, area_map.find_path(truck_2.current_location, next_location))

# Prints total miles to deliver the packages
print('Total miles traveled:', truck_1.miles_traveled + truck_2.miles_traveled)

# Creates interface to check the packages
user_input = 0
while user_input != 'q' and user_input != 'Q':
    print('Enter t to check all packages at a specific time, k to check a specific package, and q' +
          ' to exit the application: ', end='')
    user_input = input()

    if user_input == 't' or user_input == 'T':
        print('Enter a time between 00:00 and 24:00: ', end='')
        user_time = input()
        if len(user_time) == 5:
            for package in packages.get_all_items():
                print()
                package.status(user_time)
        else:
            print('Improper time entered!')
    elif user_input == 'k' or user_input == 'K':
        print('Enter the key of the package: ', end='')
        user_key = int(input())

        print('Enter a time between 00:00 and 24:00: ', end='')
        user_time = input()
        if len(user_time) == 5:
            print()
            package = packages.search(user_key)
            if package is None:
                print('Package not found!')
            else:
                package.status(user_time)
        else:
            print('Improper time entered!')

    elif user_input != 'q' and user_input != 'Q':
        print('Invalid input!')
