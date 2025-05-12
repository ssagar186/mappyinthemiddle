import sys
from src.validate_address import validate_address

class AddressInputLookup:
    def __init__(self):
        self.location = None
        self.addresses = []
        self.address = None

    def user_input(self):
        while True:
            if len(self.addresses) < 1:
                string = "Please enter an address (or type 'quit' to exit): "
            else:
                string = "Please enter another address (or type 'done' to finish): "
            address = input(string)
            if address == 'quit':
                sys.exit()
            if address.lower() == 'done' and len(self.addresses) > 1:
                break
            if address.lower() == 'done' and len(self.addresses) < 2:
                continue
            try:
                self.address = validate_address(address)
                if self.confirm_input():
                    self.addresses.append(self.address)
                else:
                    continue
            except AttributeError:
                print(f'Address not found')
            except Exception as e:
                print('Unknown error occurred: ' + string(e))

    def confirm_input(self):
        while True:
            option = input("Is this the correct address?").lower()
            if option in ['yes', 'y', '1', 'done']:
                return True
            elif option in ['no', 'n', '2']:
                return False
            else:
                print("Invalid input.")