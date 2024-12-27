import pyglet
from pyglet.gl import *
from Code import *
from Labels_Class import *
from Transformationmanager import *
from Buttondetection import *


class Calibration:
    """
    Calibration Class responsible for the entire calibration process
    """
    def __init__(self):
        self.step = 0               
        self.calib_state = False
        self.coordinate = []

    def initialization(self):
        """
        Handles the joystick input of the 3rd and 4th button on the joystick.
        If both are pressed simultaneously it will return 2 for the Cycler in the Run.py file to be used

        Input(no arguments):
            Joystick1 3rd Button (joystick1.buttons[2])
            Joystick1 4th Button (joystick1.buttons[3])

        Returns:
            2 (True) if the condition is met
        """
        if joystick1.buttons[2] == True and joystick1.buttons[3] == True:
            self.calib_state = True
        else:
            self.calib_state = False
        if standarddetector.button_press_and_release(self.calib_state) == True:
            self.step = 0
            return 2


    def get_coordinates(self):
        """
        Cycles through the different calibration steps on each trigger pull and takes the transformed cartesian coordinates to
        write them to a Calibration.txt file with the write_to_file() function
        """

        labels.next_step(self.step)                         
        if self.step == 3 and standarddetector.button_differentiating() == 1:    #if the trigger is pulled when 3 of the coordinates have been collected:
            self.coordinate.append(str((spherical_to_cartesian())))  
            transmanager.add_transformation()            #append last coordinate
            transmanager.create_calibration_file(self.coordinate)                            #write the coordinates to the calibration file                                   #
            self.step = (self.step + 1) % 5                                      #show the next label step (confirmation)
                                                      #transform the coordinates to spherical

            if standarddetector.button_differentiating() == 1:                   #if already on the confirmation step but trigger is pulled:
                self.coordinate = []                                             #delete coordinates and start from the beginning
                self.step = (self.step + 1) % 5

        else:
            if standarddetector.button_differentiating() == 1:                   #usually: on trigger pull, change to next step and store coordinates
                self.coordinate.append(str((spherical_to_cartesian())))
                self.step = (self.step + 1) % 5
        

    def calibration_mode(self):
        """
        Handles the logic of the calibration mode and runs the necessary functions for calibration to work
        """
        
        spherical_to_cartesian()
        send_OSC()
        calibrator.get_coordinates()


calibrator = Calibration()













