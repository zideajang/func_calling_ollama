from rich.console import Console

console = Console()

def add(a:float,b:float)->float:
    """useful for cacluate the sum of a and b"""
    return a + b

def mul(a:float,b:float)->float:
    """useful for cacluate the mutiply of a and b"""
    return a + b

def sub(a:float,b:float)->float:
    """useful for cacluate the substraction of a and b"""
    return  a - b

class Direction:
    pass

class Weather:
    pass

def get_weather(city_name:str)->str:
    """Get the current weather given a city"""
    console.print(f"Fetching weather for {city_name}...")
    #TODO implement this to actually call it later
    return f"Weather in {city_name}: Sunny with mild temperatures."


def get_directions(start:str,destination:str)->Direction:
    """Get directions from Google Directions API.
    start: start address as a string including zipcode (if any)
    destination: end address as a string including zipcode (if any)"""

    #TODO implement this to actually call it later


# TODO call tool 推广到更加通用
def call_tool(data,func):

    tool_name = data['tools']['tool']
    tool_input = data['tools']['tool_input']
    
    # TODO 导入 function 所在模块
    tool_mapping = {
        'get_weather': get_weather,
        'get_directions' : get_directions 
    }
    
    if tool_name in tool_mapping:
        result = tool_mapping[tool_name](**tool_input)
        print(result)
        if func:
            func(result)
        return result
    else:
        print("No such tool found.")
