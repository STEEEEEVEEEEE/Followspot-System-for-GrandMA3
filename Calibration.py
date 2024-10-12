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
        self.calib_state = False

    def initialization(self):
        if joystick1.buttons[2] == True and joystick1.buttons[3] == True:
            self.calib_state = True
        else:
            self.calib_state = False
        if standarddetector.button_press_and_release(self.calib_state) == True:
            return 2

    def get_coordinates(self):
        trigger = joystick1.buttons[0]
        if standarddetector.button_differentiating() ==  1:
            coordinate.append((spherical_to_cartesian()))
            self.step = (self.step + 1) % 4
            Labels.next_step(self.step)
            return coordinate[self.step]
        
    def calibration_mode(self):
        calibration_batch.draw()
        spherical_to_cartesian()
        send_OSC()


class Buttondetection:

    def __init__(self):
        self.button_pressed = False
        self.button_type = 0
        self.detectors = []

    def button_press_and_release(self, button):
        # Allow modifying the outer variable
        # Get current button states
        current_state = button  # Get a list of button states
        if current_state == True and self.button_pressed == False:
            press = True
        else: 
            press = False
        self.button_pressed = current_state # Update button_states for next frame
        return press

    def button_differentiating(self):
        trigger = joystick1.buttons[0]
        switchbutton = joystick1.buttons[1]

        for i, detector in enumerate(self.detectors):
            if detector.button_press_and_release(joystick1.buttons[i]) == True:
                self.button_type = i + 1
                print(f"Button {self.button_type} pressed (single click)")
                return self.button_type      
        
    def create_button_instances(self):
        for i in joystick1.buttons:
            i = Buttondetection()
            self.detectors.append(i)


standarddetector = Buttondetection()
seconddetector = Buttondetection()
calibrator = Calibration()


def calibration(pan, tilt):
    z = 4
    x = -148
    y = 11
    Calibration.get_coordinates()

    
    

    pass



def test(dt):
    pass










