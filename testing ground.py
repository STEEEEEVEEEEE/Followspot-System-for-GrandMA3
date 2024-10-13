from pyglet.window import key
import pyglet
from pythonosc import udp_client


MA3_IP = "192.168.1.12"  # Replace with your GrandMA3 console's IP address
MA3_OSC_PORT = 8000    # Standard OSC port for GrandMA3


client = udp_client.SimpleUDPClient(MA3_IP, MA3_OSC_PORT)

def next_step(step):
        location = []
        one = "bottom_left"
        two = "bottom_right"
        three = "Top_left"
        four = "Top_right"
        location.append((one, two, three, four))
        print(f"Please direct the Followspot-Light to the {location[0][3]} and press trigger") 
    




def check_collision(rect1, rect2):
    """Checks if two pyglet.shapes.Rectangle objects are colliding."""
        # Check for NO overlap in the x-axis (this means they DO NOT collide)
    if (rect1.x + rect1.width >= rect2.x) or (rect2.x + rect2.width >= rect1.x):
        print("Collision")
        return False

    # Check for NO overlap in the y-axis (this means they DO NOT collide)
    if (rect1.y + rect1.height <= rect2.y) or (rect2.y + rect2.height <= rect1.y):
        #print("NONE")
        return False
    else:
        # If we got here, then there is overlap on BOTH axes, meaning a collision
        #print(f"Collision")
        return True


def something():
    for i in range(fixtures):
        fix = i
        y = y_middle
        x = x_middle -  window.width // 4 + window.width // 15 * (i * fixtures)
        size = window.height // 10
        label = pyglet.text.Label(f"Fixture {i + 1}", x=x + size // 2, y=y + size // 2, font_size=window.height // 100, anchor_x='center', batch=batch, color=(0,0,0,150))
        fixture_labels.append(label)
        fixture = pyglet.shapes.Rectangle(x, y, size, size, color=(255, 255, 255), batch=batch)
        fixture_shapes.append(fixture)



window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)


def button_press_and_release_doesnt_work():
    already_pressed = False
    if already_pressed == False:
        if keys[key.SPACE]:
            already_pressed == True
            print(already_pressed)
            return already_pressed
            
        else:
            #print(already_pressed)
            return already_pressed
        
button_states = {}  # Dictionary to store button states (previous frame)
space_pressed = False
def button_press_and_release_works():
      # Allow modifying the outer variable
    global space_pressed
        # Get current button states
    current_states = keys[key.SPACE]  # Get a list of button states
    if current_states == True and space_pressed == False:
        print(f"Button pressed (single click)")

    space_pressed = current_states # Update button_states for next frame
    return current_states

class Math():

    def sine(degrees):
        """Calculates the sine of an angle given in degrees."""
        radians = math.radians(degrees)  # Convert degrees to radians
        sine_value = math.sin(radians)
        return sine_value   # Convert the result back to degrees

    def tan(degrees):
        """Calculates the tangent of an angle given in degrees"""
        radians = math.radians(degrees)
        tangent_value = math.tan(radians)
        return tangent_value

    def cosine(degrees):
        """Calculates the cosine of an angle given in degrees"""
        radians = math.radians(degrees)
        cosine_value = math.cos(radians)
        return cosine_value

    def arctan(ratio):
        """Calculates the arctan of the ratio between two cathetes, output in degrees"""
        rat = math.atan(ratio)
        tangent_angle = math.degrees(rat)
        return tangent_angle
    
    def arcsine(ratio):
        """Calculates the arcsine of the ratio between a cathetus and the hypotenuse, output in degrees"""
        rat = math.asin(ratio)
        sine_angle = math.degrees(rat)
        return sine_angle      
    

def spherical_to_cartesian():
    
    z = 4
    
    
    x = (Math.sine(pan - 90) * Math.tan(tilt) * z)
    y = (Math.cosine(pan - 90) * Math.tan(tilt) * z)
    return x, y

cart_x = -87
cart_y = -8
def cartesian_to_spherical():
    z = 4
    r = (cart_x**2 + cart_y**2)**0.5
    cart_pan = Math.arcsine(cart_x/r)
    cart_tilt = Math.arctan(r/z)

    return cart_pan, cart_tilt

def send_cartesian_OSC():

    cart_pan, cart_tilt = cartesian_to_spherical()
    
    client.send_message("/gma3/cmd", f'At {cart_pan} Attribute "Pan"')
    #print(f'{Fixture} At Pan {pan}')
    client.send_message("/gma3/cmd", f'At {cart_tilt} Attribute "Tilt"')

def run(self):    
    pass


def write_to_text_file():
    file = open("Calibration.txt", "w")
    lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
    file.writelines(lines)

def read_from_text_file():
    with open("Calibration.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            print(line, end="")


write_to_text_file()
read_from_text_file()



def create_Fixtures(fixtures):
    """
    Creates a certain amount of fixtures

    Args:
        The amount of fixtures
    """
    for i in range(fixtures):
        size = window.height // 10
        label = pyglet.text.Label(f"Fixture {i + 1}", x=0 + size // 2, y=0 + size // 2, font_size=window.height // 100, anchor_x='center', batch=batch, color=(0,0,0,150))
        fixture_labels.append(label)
        fixture = pyglet.shapes.Rectangle(0, 0, size, size, color=(255, 255, 255), batch=batch)
        fixture_shapes.append(fixture)

def center_and_distribute_fixtures(rectangles, labels):
    """Centers and distributes a list of rectangles within a window."""
    size = window.height // 10
    num_rects = len(rectangles)
    total_width = sum(rect.width for rect in rectangles)

    # Calculate spacing between rectangles
    available_space = window.width - total_width
    spacing = available_space / (num_rects + 1) if num_rects > 1 else 0

    # Calculate starting x position
    start_x = (window.width - total_width - spacing * (num_rects - 1)) / 2

    # Position each rectangle
    for i, rect in enumerate(rectangles):
        rect.x = start_x + i * (rect.width + spacing)
        rect.y = window.height // 2.5 - rect.height // 2  # Center vertically
        labels[i].x = rect.x + size // 2
        labels[i].y = rect.y + size // 2

def FixtureSelect_Collision(): 
    """Checks for all fixture rectangles if they are colliding with the jstk_rectangle"""
    for i in fixture_shapes:
        collision = check_collision(jstk_rect,i)
        if collision == True:
            #print(collision, fixture_shapes[i])
            pass

def check_collision(rect1, rect2):
    """
    Checks if two pyglet.shapes.Rectangle objects are colliding.

        Args:

        tuple containing position of rect1 and rect2

    Returns:
        True if they are colliding

        False if they are not colliding
    """

        # Check for overlap in the x-axis
    if (-rect1.anchor_position[0] + rect1.width >= rect2.x) and (rect2.x + rect2.width >= -rect1.anchor_position[0]):
    # Check for overlap in the y-axis
        if (-rect1.anchor_position[1] + rect1.height >= rect2.y) and (rect2.y + rect2.height >= -rect1.anchor_position[1]):
            #print("Collision")
            return True
        else:
            #print("None")
            return False
    else:
        #print("None")
        return False

#pyglet.clock.schedule_interval(run, 1/60.0)
#pyglet.app.run()
