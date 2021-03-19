class Location:
    """Creates a location to use for a map."""
    def __init__(self, address):
        self.address = address
        self.distance = float('inf')
        self.prev_location = None


class Map:
    """Creates a map to use to travel between locations."""
    def __init__(self):
        """Initializes an empty graph with a center initialized to none."""
        self.adjacency_list = {}
        self.distances = {}
        self.center = None

    def add_location(self, new_location):
        """Adds a location to the map."""
        self.adjacency_list[new_location] = []

    def add_directed_edge(self, from_location, to_location, distance):
        """Adds an edge from one location to another."""
        self.distances[(from_location, to_location)] = distance
        self.adjacency_list[from_location].append(to_location)

    def add_undirected_edge(self, location1, location2, distance):
        """Adds an edge between two locations."""
        self.add_directed_edge(location1, location2, distance)
        self.add_directed_edge(location2, location1, distance)

    def find_path(self, start_location, end_location):
        """Finds a path between two locations.
        Uses Dijkstra's Shortest Path Algorithm to find the shortest between start_location and end_location.
        Adds each location to path, in order of start_location to end_location.
        Resets all locations' distance and prev_locations to original values.
        Returns path.
        """
        unvisited_queue = []
        for location in self.adjacency_list:
            unvisited_queue.append(location)

        start_location.distance = 0

        while len(unvisited_queue) > 0:
            smallest_index = 0
            for i in range(1, len(unvisited_queue)):
                if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                    smallest_index = i
            current_location = unvisited_queue.pop(smallest_index)

            for adj_location in self.adjacency_list[current_location]:
                distance_between_locations = self.distances[(current_location, adj_location)]
                alternative_path_distance = current_location.distance + distance_between_locations

                if alternative_path_distance < adj_location.distance:
                    adj_location.distance = alternative_path_distance
                    adj_location.prev_location = current_location

        path = []
        current_location = end_location
        while current_location is not start_location:
            path.insert(0, current_location)
            current_location = current_location.prev_location
        path.insert(0, start_location)

        for location in self.adjacency_list:
            location.prev_location = None
            location.distance = float('inf')

        return path

    def find_path_to_center(self, start_location):
        """Finds a path from start_location to the center of the map."""
        return self.find_path(start_location, self.center)
