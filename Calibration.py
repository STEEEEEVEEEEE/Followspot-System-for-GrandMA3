import pyglet
from pyglet.gl import *
from Code import pan, tilt

joysticks = pyglet.input.get_joysticks()
assert joysticks, 'Kein Joystick verbunden'
joystick1 = joysticks[0]
joystick2 = joysticks[1]
joystick1.open()
joystick2.open()
current_step = 1

trigger = joystick1.buttons[0]
trigger_pressed = False

def button_press_and_release(button):
      # Allow modifying the outer variable
    global trigger_pressed
        # Get current button states
    current_state = button  # Get a list of button states
    if current_state == True and trigger_pressed == False:
        print(f"Button {button} pressed (single click)")

    trigger_pressed = current_state # Update button_states for next frame
    return current_state


def calibration(pan, tilt):
    step = 0
    z = 4
    x = 0
    y = 0
    
    

    pass




def get_coordinates():
    coordinates = []
    if button_press_and_release(trigger) == True:
        coordinates.append[pan, tilt]
    return coordinates




