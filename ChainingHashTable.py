class ChainingHashTable:
    """Creates a chaining hash table to hold objects with keys."""
    def __init__(self, size=10):
        """Creates an empty hash table with a number of buckets equal to size."""
        self.size = size
        self.table = []

        for num in range(self.size):
            self.table.append([])

    def search(self, key):
        """Uses a key to find an item in the hash table.
        Returns item if found and None if not.
        """
        hashed_key = hash(key) % self.size

        for item in self.table[hashed_key]:
            if item.key == key:
                return item

        return None

    def insert(self, item):
        """Inserts an item into the hash table."""
        hashed_key = hash(item.key) % self.size
        self.table[hashed_key].append(item)

    def remove(self, key):
        """Uses a key to find an item in the hash table and removes it."""
        hashed_key = hash(key) % self.size

        for item in self.table[hashed_key]:
            if item.key == key:
                self.table[hashed_key].remove(item)

    def get_all_items(self):
        """Gets all the items in the hash table.
        Creates a list and extends it with each bucket in the hash table.
        Sorts the list by the items' keys.
        Returns the list.
        """
        item_list = []

        for num in range(self.size):
            item_list.extend(self.table[num])

        item_list.sort(key=lambda item: item.key)
        return item_list
