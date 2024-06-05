from rich.console import Console

console = Console()

def add(a:int,b:int)->int:
    """useful for cacluate the sum of a and b"""
    return a + b


class Direction:
    pass

class Weather:
    pass

def get_weather(city_name:str)->Weather:
    """Get the current weather given a city"""
    #TODO implement this to actually call it later


def get_directions(start:str,destination:str)->Direction:
    """Get directions from Google Directions API.
    start: start address as a string including zipcode (if any)
    destination: end address as a string including zipcode (if any)"""

    #TODO implement this to actually call it later
