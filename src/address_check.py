import geopy
import sys

class AddressCheck:
    def __init__(self):
        self.option = None
        self.location = None
        self.addresses = []
        self.address = None

    def lookup_address(self):
        geolocator = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        self.location = geolocator.geocode(self.address)
        print(f"Validated Address: {self.location.address}")
        return self.location.address

    def validate_input(self):
        while True:
            self.option = input("Is this the correct address?").lower()
            if self.option in ['yes', 'y', '1', 'done']:
                return True
            elif self.option in ['no', 'n', '2']:
                return False
            else:
                print("Invalid input.")

    def user_input(self):
        while True:
            if len(self.addresses) < 1:
                string = "Please enter an address (or type 'quit' to exit): "
            else:
                string = "Please enter another address (or type 'done' to finish): "
            self.address = input(string)
            if self.address == 'quit':
                sys.exit()
            if self.address.lower() == 'done' and len(self.addresses) > 1:
                break
            if self.address.lower() == 'done' and len(self.addresses) < 2:
                continue
            try:
                self.address = self.lookup_address()
                if self.validate_input():
                    self.addresses.append(self.address)
                else:
                    continue
            except AttributeError:
                print(f'Address not found')
            except Exception as e:
                print('Unknown error occurred: ' + string(e))