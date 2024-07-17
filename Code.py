
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

window = pyglet.window.Window(height = 1000, width = 1500)
window.set_caption("Lightcontroller")
batch = pyglet.graphics.Batch()
selection = pyglet.graphics.Batch()
control = pyglet.graphics.Batch()
background = pyglet.shapes.Rectangle(0,0, window.width, window.height, color=(100,100,100), batch=batch)

fixture_labels = []
fixture_shapes = []
fixtures = 3
x_middle = window.width // 2
y_middle = window.height // 2
jx =  0
jy = 0

jstk_rect = pyglet.shapes.Rectangle(jx, jy, window.height // 15, window.height // 15, color=(255,0,0), batch=batch)
    
def distancesq(me,target):
  return (me.x-target.x)**2 + (me.y-target.y)**2

def check_collision(target):
    #print(distancesq(jstk_rect,i))
    # Square this distance to compensate
    if distancesq(jstk_rect,target) < (jstk_rect.width/2 + target.width/2)**2: 
        return True


for i in range(fixtures):
    fix = i
    y = y_middle
    x = x_middle -  window.width // 4 + window.width // 15 * (i * fixtures)
    size = window.height // 10
    label = pyglet.text.Label(f"Fixture {i + 1}", x=x + size // 2, y=y + size // 2, font_size=window.height // 100, anchor_x='center', batch=batch, color=(0,0,0,150))
    fixture_labels.append(label)
    fixture = pyglet.shapes.Rectangle(x, y, size, size, color=(255, 255, 255), batch=batch)
    fixture_shapes.append(fixture)


def joyaxis_motion():
    # stick_drift_x and _y serve as correction for stick drift on the joystick.
    # You can change the values on top where they are defined.
    global jx
    global jy
    if abs(joystick1.x) > 0.05:
        jx = jx - (joystick1.x + stick_drift_x) 
    else:
        jx = jx

    if abs(joystick1.y) > 0.05:
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

    client.send_message("/gma3/cmd", f'Fixture {Fixture} At {pan} Attribute "Pan"')
    #print(f'{Fixture} At Pan {pan}')
    client.send_message("/gma3/cmd", f'Fixture {Fixture} At {tilt} Attribute "Tilt"')
    #print(f'{Fixture} At Tilt {tilt}')


pan_position_label = pyglet.text.Label(f"Pan: {pan}", 
    font_name="Arial",
    font_size=17,
    x=20, 
    y=window.height - 20,  # Position at the top-left
    anchor_x="left", 
    anchor_y="top",
    batch = batch)

tilt_position_label = pyglet.text.Label(f"Tilt: {tilt}", 
    font_name="Arial",
    font_size=17,
    x=20, 
    y=window.height - 50,  # Position at the top-left
    anchor_x="left", 
    anchor_y="top",
    batch = batch)




def update():
    collision = check_collision(fixture_shapes[1])
    
    
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

