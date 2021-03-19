class Package:
    """Creates a package to use in deliveries."""
    def __init__(self, package_id, address, city, state, add_zip, deliver_deadline, mass, note):
        """Creates a package that holds all the data passed into it.
        time_loaded keeps track of the last time the package was loaded.
        time_delivered keeps track of the time the package was delivered.
        truck keeps track of the truck that the package was loaded onto.
        """
        self.key = int(package_id)
        self.address = address
        self.city = city
        self.state = state
        self.add_zip = add_zip
        self.deliver_deadline = deliver_deadline
        self.mass = int(mass)
        self.note = note
        self.time_delivered = '00:00'
        self.time_loaded = '00:00'
        self.truck = 'In Hub'

    def current_deliver_status(self, time_checked):
        """Gets the status of the package at the time checked.
        Returns 0 if the package was delivered.
        Returns 1 if not but was loaded.
        Returns 2 if the package is still In Hub.
        """
        if time_checked >= self.time_delivered:
            return 0

        if time_checked >= self.time_loaded:
            return 1

        return 2

    def status(self, time_checked='24:00'):
        """Prints the information and status of the package at the time_checked.
        Prints the information of the package, then prints a message based on the status
        of the package at the time_checked.
        """
        delivered_status = self.current_deliver_status(time_checked)

        print(self.key, '|', self.address, '|', self.city, '|', self.state, '|', self.add_zip, '|',
              self.deliver_deadline, '|', self.mass, end=' | ')

        if delivered_status == 0:
            print('Delivered', self.time_delivered)
        elif delivered_status == 1:
            print('On route - Truck', self.truck)
        else:
            print('In Hub')


