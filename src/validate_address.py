import geopy

def validate_address(address):
    geolocator = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
    location = geolocator.geocode(address)
    print(f"Validated Address: {location.address}")
    return location.address