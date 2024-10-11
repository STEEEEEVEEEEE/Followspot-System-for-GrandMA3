import pyglet
from pyglet.gl import *
from Code import *


current_step = 1
pan = 1
tilt = 1
coordinate = []

class Calibration:
    def __init__(self):
        self.step = 0

    def get_coordinates(self):

        trigger = joystick1.buttons[0]
        if triggerdetector.button_press_and_release(trigger) == True:
            coordinate.append((spherical_to_cartesian()))
            self.step = (self.step + 1) % 4
            Labels.next_step(self.step)
            return coordinate[self.step]

    class Buttondetection:

        def __init__(self):
            self.button_pressed = False

        def button_press_and_release(self, button):
            # Allow modifying the outer variable
            
                # Get current button states
            current_state = button  # Get a list of button states
            if current_state == True and self.button_pressed == False:
                print(f"Button {button} pressed (single click)")
                press = True
            else: 
                press = False
            self.button_pressed = current_state # Update button_states for next frame
            
            return press
            
triggerdetector = Calibration.Buttondetection()
switchdetector = Calibration.Buttondetection()



def calibration(pan, tilt):
    z = 4
    x = -148
    y = 11
    Calibration.get_coordinates()

    
    

    pass



def test(dt):
    pass










