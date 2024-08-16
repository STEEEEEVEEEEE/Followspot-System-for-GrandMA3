import pyglet
from pyglet.gl import *
from Code import *


current_step = 1
pan = 1
tilt = 1
coordinate = []
pantilt = []

trigger = joystick1.buttons[0]
trigger_pressed = False
press = False
def button_press_and_release(button):
      # Allow modifying the outer variable
    
    global trigger_pressed
        # Get current button states
    current_state = button  # Get a list of button states
    if current_state == True and trigger_pressed == False:
        print(f"Button {button} pressed (single click)")
        press = True
    else: 
        press = False
    trigger_pressed = current_state # Update button_states for next frame
    
    return press

def get_coordinates(step):
    trigger = joystick1.buttons[0]
    button_press = button_press_and_release(trigger)
    if button_press == True:
        coordinate.append((spherical_to_cartesian()))
        pantilt. append((pan, tilt))
        

        print(coordinate)
        print(pantilt)
    return coordinate[step], pantilt[step]


def calibration(pan, tilt):
    step = 0
    z = 4
    x = -148
    y = 11
    
    

    pass



def test(dt):
    pass










