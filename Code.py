
from pythonosc import udp_client
import pyglet
from pyglet.gl import *

MA3_IP = "192.168.1.12"  # Replace with your GrandMA3 console's IP address
MA3_OSC_PORT = 8000    # Standard OSC port for GrandMA3


client = udp_client.SimpleUDPClient(MA3_IP, MA3_OSC_PORT)

# Basic OSC message structure
Fixture = 303
tilt = 0
pan = 0
# Example: Turning on fixture 1
stick_drift_x = 1.5259021896696368e-05
stick_drift_y = 1.5259021896696368e-05
joysticks = pyglet.input.get_joysticks()
assert joysticks, 'Kein Joystick verbunden'
joystick1 = joysticks[0]
joystick1.open()

window = pyglet.window.Window(height = 500, width = 750)
window.set_caption("Lightcontroller")
batch = pyglet.graphics.Batch()
selection = pyglet.graphics.Batch()
control = pyglet.graphics.Batch()
background = pyglet.shapes.Rectangle(0,0, window.width, window.height, color=(100,100,100), batch=batch)

fixture_labels = []
fixture_shapes = []
fixtures = 5
x_middle = window.width // 2
y_middle = window.height // 2
jx =  0
jy = 0

def create_Fixtures(fixtures):
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
        rect.y = window.height // 2 - rect.height // 2  # Center vertically
        labels[i].x = rect.x + size // 2
        labels[i].y = rect.y + size // 2


jstk_rect = pyglet.shapes.Rectangle(jx, jy, window.height // 15, window.height // 15, color=(255,0,0), batch=batch)


def FixtureSelect_Collision(): 

    for i in fixture_shapes:
        collision = check_collision(jstk_rect,i)
        if collision == True:
            #print(collision, fixture_shapes[i])
            pass
    
def check_collision(rect1, rect2):
    """Checks if two pyglet.shapes.Rectangle objects are colliding."""
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



def joyaxis_motion():
    # stick_drift_x and _y serve as correction for stick drift on the joystick.
    # You can change the values on top where they are defined.
    global jx
    global jy
    if abs(joystick1.x) > 0.1: #easier to control since it is less sensitive to small user inconsistencies 
        jx = jx - (joystick1.x + stick_drift_x) 
    else:
        jx = jx

    if abs(joystick1.y) > 0.1:
        jy = jy + (joystick1.y + stick_drift_y) 
    else:
        jy = jy
    #print(joystick1.x, joystick1.y)  
    return jx, jy    

def jstk_rectangle_movement():

    joyx, joyy = joyaxis_motion()
    
    rectx = joyx * window.width // 700
    recty = joyy * window.height // 700
    
    return rectx, recty

def send_OSC():
    """sends the OSC Message based on joystick input to control the designated fixture"""
    global pan
    global tilt
    sens = 0.5
    pan = jx  * sens
    tilt = jy * sens * 0.7

    client.send_message("/gma3/cmd", f'At {pan} Attribute "Pan"')
    #print(f'{Fixture} At Pan {pan}')
    client.send_message("/gma3/cmd", f'At {tilt} Attribute "Tilt"')
    #print(f'{Fixture} At Tilt {tilt}')


pan_position_label = pyglet.text.Label(f"Pan: {pan}", 
    font_name="Arial",
    font_size= window.height // 58,
    x= window.height // 50, 
    y=window.height - window.height // 50,  # Position at the top-left
    anchor_x="left", 
    anchor_y="top",
    batch = batch)

tilt_position_label = pyglet.text.Label(f"Tilt: {tilt}", 
    font_name="Arial",
    font_size= window.height // 58,
    x= window.height // 50, 
    y=window.height - window.height // 20,  # Position at the top-left
    anchor_x="left", 
    anchor_y="top",
    batch = batch)


create_Fixtures(fixtures)
center_and_distribute_fixtures(fixture_shapes, fixture_labels)
def update():


    collision = check_collision(jstk_rect, fixture_shapes[0])
    FixtureSelect_Collision()
    #print(joyx, joyy)
    jstk_rect.postion = jstk_rectangle_movement()
    jstk_rect.anchor_position = jstk_rectangle_movement()[0] - x_middle, jstk_rectangle_movement()[1] - y_middle
    pan_position_label.text = f"Pan: {int(pan)}"
    tilt_position_label.text = f"Tilt: {int(tilt)}"
    send_OSC()

def on_draw(dt):
    window.clear()
    batch.draw()
    
    update()    
    pass

on_draw(1)



pyglet.clock.schedule_interval(on_draw, 1/60.0)
pyglet.app.run()
#client.send_message("/gma3/Page1/Fader201",0)

