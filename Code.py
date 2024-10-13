
from pythonosc import udp_client
import pyglet
from pyglet.gl import *
import math
import ast


MA3_IP = "192.168.1.16"  # Replace with your GrandMA3 console's IP address
MA3_OSC_PORT = 8000    # OSC port for GrandMA3


client = udp_client.SimpleUDPClient(MA3_IP, MA3_OSC_PORT)

# Basic OSC message structure
Fixture = 303
pan = 0
tilt = 0
# Example: Turning on fixture 1
stick_drift_x = 1.5259021896696368e-05
stick_drift_y = 1.5259021896696368e-05
joysticks = pyglet.input.get_joysticks()
assert joysticks, 'Kein Joystick verbunden'
joystick1 = joysticks[0]
joystick2 = joysticks[1]
joystick1.open()
joystick2.open()


window = pyglet.window.Window(width = 1000, height = 500)
window.set_caption("Lightcontroller")

batch = pyglet.graphics.Batch()
label = pyglet.graphics.Batch()
calibration_batch = pyglet.graphics.Batch()
selection = pyglet.graphics.Batch()
control = pyglet.graphics.Batch()
outofbounds = pyglet.graphics.Batch()

x_middle = window.width // 2
y_middle = window.height // 2

stage_origin = window.width//6, window.height//3
background = pyglet.shapes.Rectangle(0,0, window.width, window.height, color=(100,100,100), batch=batch)
Stage = pyglet.shapes.Rectangle(stage_origin[0],stage_origin[1], window.width//1.5, window.height//1.7, color = (70,70,70), batch=batch)
stage_middle = Stage.x + Stage.width / 2, Stage.y + Stage.height / 2
origin = stage_origin[0], stage_origin[1]

fixture_labels = []
fixture_shapes = []
fixtures = 4

jx =  0
jy = 0
normalized_z = (-joystick1.z + 1) // 2
jstk_rect = pyglet.shapes.Circle(jx, jy, window.height // 25, color=(255,0,0, 150), batch=batch)

offset = 90



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

def out_of_bounds():
    """
    Checks if the pan/tilt values are close to or exceeding the maximum rotational angle of the fixture

    Slowly turns the pan/tilt labels red if the values are getting close
    and displays an "out of bounds" warning if they exceeded

    Returns:
        True if the values have not been exceeded

        False if they have been exceeded
    
    """
    state = True
    red_pan = int((abs(pan)-199)*2.857)
    red_tilt = int((abs(tilt)-79)*2.454)
    if abs(pan) <= 270 and abs(tilt) <= 135:
        state = False
    elif abs(pan) > 270 or abs (tilt) > 135:
        state = True
        outofbounds.draw()

    if 255 > abs(pan) >= 200:
        labels.pan_label.color = (255,-red_pan,-red_pan,255)
    if abs(pan) >= 255:
        labels.pan_label.color = (255,0,0,255)
    elif abs(pan) < 200:
        labels.pan_label.color = (255,255,255,255)
    if 135 > abs(tilt) > 80:
        labels.tilt_label.color = (255,-red_tilt,-red_tilt,255)
    if abs(tilt) >= 135:
        labels.tilt_label.color = (255,0,0,255)
    elif abs(tilt) < 80:
        labels.tilt_label.color = (255,255,255,255)
    return state

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

def light_parameters():
    """
    Takes the input from the joystick2 axes and converts it to usable values that
    can then be sent as an OSC command and displayed as a label in the interface

    Input:
        joystick2.rq
        joystick2.z

    the final parameters "intensity" and "zoom" are assigned as global
    """
    global intensity
    global zoom
    #normalized_rq = (-joystick2.rq + 1) / 2
    normalized_z = (joystick2.z + 1) / 2
    #intensity = normalized_rq * 100
    zoom = (normalized_z * 57.5) + 2.5


def joyaxis_motion():
    """
    Takes the input from the joystick1 axes(x, y and z) that output values between -1 and 1 and converts that to 
    a consistent increase/decrease in the value to then be used by the different ..._movement() functions

    Input:
        joystick1.x(horizontal movement)
        joystick1.y(vertical movement)
        joystick2.rq(sensitivity)

    Returns:
        jx and jy as converted x and y values that consistently increase/decrease based on joystick input

     """
    # stick_drift_x and _y serve as correction for stick drift on the joystick.
    # You can change the values on top where they are defined.
    global sens
    global jx
    global jy
    normalized_rq = (-joystick2.rq + 1.2) / 10
    sens = normalized_rq
    
    if abs(joystick1.x) > 0.1: #easier to control since it is less sensitive to small user inconsistencies 
        jx = jx - (joystick1.x * sens + stick_drift_x)
    else:
        jx = jx

    if abs(joystick1.y) > 0.1:
        jy = jy + (joystick1.y * sens + stick_drift_y)
    else:
        jy = jy
    
    return jx, jy



def send_OSC():
    """
    sends the OSC Message based on joystick input to control the designated fixture

    Adjusts and sends the jx and jy values from the joyaxis_motion() function
    """

    global pan
    global tilt


    pan = jx  
    tilt = -jy * 0.7


    client.send_message("/gma3/cmd", f'At {zoom} Attribute "Zoom"')
    client.send_message("/gma3/cmd", f'At {pan} Attribute "Pan"')
    client.send_message("/gma3/cmd", f'At {tilt} Attribute "Tilt"')


intensity = 0
zoom = 0
sens = 0

def spherical_to_cartesian():
    """
    Takes the spherical coordinates(pan/tilt) and translates them to a cartesian coordinate system

    Input(no arguments): 
        Global Pan
        Global Tilt
        z (Height: can be chosen at random since the height is constant
        and therefore cancels out when transforming back to spherical)

    Returns:
        x and y in the cartesian coordinate system
    """
    global x
    global y
    z = 4
    x = (Math.sine(pan-offset) * Math.tan(tilt) * z)
    y = (Math.cosine(pan-offset) * Math.tan(tilt) * z)
    return x, y

    
#origin1 = (-5.863388133, -0.72475178)           #the bottom-left corner of the stage
#max_x = (3.5538304, -0.408089844)               #the bottom-right corner of the stage
#max_y = (-6.963154, -9.038917)                  #the top-left corner of the stage
#max_both = (4.398541132, -8.0420626908)         #the top-right corner of the stage


#origin1 = (-4.89478, -3.77743)           #the bottom-left corner of the stage
#max_x = (2.237131, -3.968535)               #the bottom-right corner of the stage
#max_y = (-5, -7.8916922)                  #the top-left corner of the stage
#max_both = (2.62696221, -7.8916922)         #the top-right corner of the stage
class Transformation():
    def __init__(self):
        self.coordinates = []

    def create_coordinates_from_file(self):
        if self.coordinates == []:
            with open("Calibration.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.rstrip("\n")
                    line_tuple = ast.literal_eval(line)
                    print(line_tuple)
                    self.coordinates.append(line_tuple)
        return self.coordinates

transformer = Transformation()

origin1 = (-7.1160833, 5.833910)           #the bottom-left corner of the stage
max_x = (4.8003327, 4.6627282)               #the bottom-right corner of the stage
max_y = (-5.073917, -3.6413534)                  #the top-left corner of the stage
max_both = (2.5557522, -2.339679)         #the top-right corner of the stage

coordinates = [origin1, max_x, max_y, max_both]

def cartesian_movement(jstk_cart_position):
    """
    Takes the x and y values from the jstk_rectangle_movement() function and transforms them to output values in the 0-100
    range if the red jstk_rectangle is somewhere on the stage.

    Args:
        jstk_cart_position: The initial position of the rectangle on the stage
    
    Input:
        The joyx and joyy values from the jstk_rectangle_movement() function

    Returns:
        The adjusted x and y values of the jstk_rectangle to be further used in the translate_to_quadrilateral() function
    """
    global cart_x
    global cart_y
    
    cart_joyx, cart_joyy = joyaxis_motion()
    
    jstk_cart_position = jstk_cart_position[0] + cart_joyx * window.width/175, jstk_cart_position[1] + cart_joyy * window.height / 175
    
    cart_x, cart_y = (-jstk_cart_position[0] + window.width/6)/(window.width/151), (-jstk_cart_position[1] + window.height/3)/(window.height/171)
    return jstk_cart_position, cart_x, cart_y


def rectangle_movement():
    """Takes the positional value of the cartesian_movement() function and applies it to the pyglet jstk_rectangle shape"""
    position = cartesian_movement(origin)
    jstk_rect.anchor_position = position[0][0] - window.width / 3, position[0][1] - window.height / 1.5
    jstk_rect.radius = (zoom + 10) * 1.5

def translate_to_quadrilateral(corners):
    """
    Translates coordinates from a normalized 0-100 system to a quadrilateral defined by its corners.

    Args:
        corners: A list of four tuples representing the corners of the quadrilateral:
                 [(bottom_left_x, bottom_left_y), 
                  (bottom_right_x, bottom_right_y), 
                  (top_left_x, top_left_y), 
                  (top_right_x, top_right_y)]

    Input:
            The x and y values from the cartesian_movement() function

    Returns:
        A tuple (x, y) representing the translated coordinates in the quadrilateral's space.
    """

    input_x, input_y = cart_x, cart_y
    
    bl, br, tl, tr = corners
    
    # Interpolate along the bottom and top edges based on input_x
    bottom_x = bl[0] + (br[0] - bl[0]) * (input_x / 100)
    bottom_y = bl[1] + (br[1] - bl[1]) * (input_x / 100)
    top_x = tl[0] + (tr[0] - tl[0]) * (input_x / 100)
    top_y = tl[1] + (tr[1] - tl[1]) * (input_x / 100)

    # Interpolate between the bottom and top points based on input_y
    final_x = bottom_x + (top_x - bottom_x) * (input_y / 100)
    final_y = bottom_y + (top_y - bottom_y) * (input_y / 100)
    
    return final_x, final_y


state = False
overflow = False

def cartesian_to_spherical():
    """
    Transforms the interpolated values from the translate_to_quadrilateral 
    function to the spherical coordinate system.

    Input(already in the code, no arguments):
        Interpolated values from translate_to_quadrilateral() function.
        z: should be the same as in the spherical_to_cartesian() function for accurate results

    Returns:
        A tuple (cart_pan, cart_tilt) representing the transformed values in the spherical coordinate system(pan/tilt).
    """

    global cart_pan
    global cart_tilt
    global state
    cart_x, cart_y = translate_to_quadrilateral(transformer.create_coordinates_from_file())
    z = 4

    if state == False:
        if cart_y >= 0 and cart_x < 0:
            r = (cart_x**2 + cart_y**2)**0.5
            cart_pan = (((Math.arcsine(cart_x/r))+offset)+180)
            cart_tilt = -(Math.arctan(r/z))
        elif cart_y < 0 and cart_x < 0:
            r = -((cart_x**2 + cart_y**2)**0.5)
            cart_pan = ((Math.arcsine(cart_x/r))+offset)
            cart_tilt = (Math.arctan(r/z))
        elif cart_y < 0 and cart_x > 0:
            r = -((cart_x**2 + cart_y**2)**0.5)
            cart_pan = ((Math.arcsine(cart_x/r))+offset)
            cart_tilt = (Math.arctan(r/z))
        elif cart_y >= 0 and cart_x > 0:
            r = -((cart_x**2 + cart_y**2)**0.5)
            cart_pan = -((Math.arcsine(cart_x/r))+offset)
            cart_tilt = (Math.arctan(r/z))
    elif state == True:
        if cart_y >= 0 and cart_x < 0:
            r = (cart_x**2 + cart_y**2)**0.5
            cart_pan = (((Math.arcsine(cart_x/r))+offset)-180)
            cart_tilt = -(Math.arctan(r/z))
        elif cart_y < 0 and cart_x < 0:
            r = -((cart_x**2 + cart_y**2)**0.5)
            cart_pan = (((Math.arcsine(cart_x/r))+offset)-360)
            cart_tilt = (Math.arctan(r/z))
        elif cart_y < 0 and cart_x > 0:
            r = -((cart_x**2 + cart_y**2)**0.5)
            cart_pan = ((Math.arcsine(cart_x/r))+offset)
            cart_tilt = (Math.arctan(r/z))
        elif cart_y >= 0 and cart_x > 0:
            r = -((cart_x**2 + cart_y**2)**0.5)
            cart_pan = -((Math.arcsine(cart_x/r))+offset)
            cart_tilt = (Math.arctan(r/z))




def send_cartesian_OSC():
    """
    Sends the OSC command in the cartesian coordinate system and for the zoom and intensity values.
    
    Input(already in the code, no arguments): 
        cartesian value from cartesian_to_spherical() function
        zoom and intensity values from the light_parameters() function
    """
    global pan
    global tilt
    global state
    client.send_message("/gma3/cmd", f'At {zoom} Attribute "Zoom"')
    #client.send_message("/gma3/cmd", f'At {intensity}')
    if cart_pan < 0:
        state = True
        client.send_message("/gma3/cmd", f'At {cart_pan} Attribute "Pan"')
        client.send_message("/gma3/cmd", f'At {cart_tilt} Attribute "Tilt"')
    elif cart_pan >= 0:
        state = False
    client.send_message("/gma3/cmd", f'At {cart_pan} Attribute "Pan"')
    client.send_message("/gma3/cmd", f'At {cart_tilt} Attribute "Tilt"')
    pan = cart_pan
    tilt = cart_tilt



class Labels():   
    """
    A class that contains the parameters for all the labels that are displayed in the interface
    
    Also contains functions to dynamically change the values of the parameters
    """
    def __init__(self):

        self.pan_label = pyglet.text.Label(f"Pan: {pan}", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 28,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)

        self.tilt_label = pyglet.text.Label(f"Tilt: {tilt}", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 14.7,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)

        self.sens_label = pyglet.text.Label(f"Sens: {sens}", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 10,
                anchor_x="left", 
                anchor_y="top",
                batch = label)

        self.intens_label = pyglet.text.Label(f"Intens: {intensity}", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 5.94,  
                anchor_x="left", 
                anchor_y="top",
                batch = control)

        self.zoom_label = pyglet.text.Label(f"Zoom: {zoom}", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 7.5,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)
        
        self.calibration_text = pyglet.text.Label(f"Calibration", 
                font_name="Arial",
                font_size= window.height // 40,
                x= x_middle, 
                y=window.height - window.height // 14,  
                anchor_x="center", 
                anchor_y="top",
                batch = calibration_batch)
        
        self.x_label = pyglet.text.Label(f"X-Position:", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 40, 
                y= window.height // 9,  
                anchor_x="left", 
                anchor_y="top",
                batch = batch)
        
        self.y_label = pyglet.text.Label(f"Y-Position:", 
                font_name="Arial",
                font_size= window.height // 40,
                x= window.height // 40, 
                y= window.height // 14,  
                anchor_x="left", 
                anchor_y="top",
                batch = batch)
        
        self.show_mode_label = pyglet.text.Label(f"", 
                font_name="Arial",
                font_size= window.height // 20,
                x= window.height // 40, 
                y= window.height // 5,  
                anchor_x="left", 
                anchor_y="top",
                batch = batch)
        
        self.out_of_bounds_label = pyglet.text.Label(f"OUT OF BOUNDS", 
                color = (255, 0, 0, 255),
                font_name="Arial",
                bold = True,
                font_size= window.height // 15,
                x= window.height // 2.8, 
                y= window.height // 1.2,  
                anchor_x="left", 
                anchor_y="top",
                batch = outofbounds)
        
    def next_step(self, step):
        location = []
        one = f"Please direct the Followspot-Light to the bottom-left and press trigger"
        two = f"Please direct the Followspot-Light to the bottom-right and press trigger"
        three = f"Please direct the Followspot-Light to the top-left and press trigger"
        four = f"Please direct the Followspot-Light to the top-right and press trigger"
        five = "You can now leave calibration mode. If you still want to make readjustments, press trigger"
        six = "Succesfully stored, you can now leave calibration mode"
        location.append([one, two, three, four, five])
        labels.calibration_text.text = location[0][step]


    def update_labels(self):
        x, y = cartesian_movement(origin)[1], cartesian_movement(origin)[2]
        labels.pan_label.text = f"Pan: {int(pan)}"
        labels.tilt_label.text = f"Tilt: {int(tilt)}"
        labels.sens_label.text = f"Sens: {int(sens * 495 - 8) }"
        labels.intens_label.text = f"Intens: {int(intensity)}"
        labels.zoom_label.text = f"Zoom: {int(zoom)}"
        labels.x_label.text = f"X-Position: {int(x)}"
        labels.y_label.text = f"Y-Position: {int(y)}"
    
class Math():
    """
    A class with trigonometric functions that use degrees instead of radians that are used by the official math module
    """

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
    
#client.send_message("/gma3/Page1/Fader201",0)
labels = Labels()

