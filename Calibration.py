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
        self.fixture_id = None
        self.input_text = ""
        self.fixture_rectangle = None
        self.fixture_label = None

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
        if joystick1.buttons[2] == True and joystick1.buttons[3] == True and self.step == 0 or self.step == 6:    
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
            self.coordinate.append(str((spherical_to_cartesian())))           #append the last coordinate
            self.step = (self.step + 1) % 7                                     #show the next label step (confirmation)


        elif self.step == 4 and standarddetector.button_differentiating() == 1:  #if the trigger is pulled when the fixture_id is entered:
            self.fixture_id = self.input_text
            transmanager.add_fixture_rectangle(self.fixture_id)                   #add fixture rectangle to the interface   
            self.input_text = ""
            self.step = (self.step + 1) % 7     

        elif self.step == 5 and standarddetector.button_differentiating() == 1:   
            transmanager.save_fixture_position(self.fixture_id, transmanager.fixture_rectangle.x, transmanager.fixture_rectangle.y)                                    #append last coordinate
            transmanager.create_calibration_file(self.fixture_id, self.coordinate) 
            self.coordinate = []                                              #reset the coordinate list
            self.step = (self.step + 1) % 7

        elif self.step == 6 and standarddetector.button_differentiating() == 1:                   #if already on the confirmation step but trigger is pulled:                        #delete coordinates and start from the beginning
                self.step = (self.step + 1) % 7
        else:
            if standarddetector.button_differentiating() == 1:                   #usually: on trigger pull, change to next step and store coordinates
                self.coordinate.append(str((spherical_to_cartesian())))
                self.step = (self.step + 1) % 7


    def on_key_press(self):
        numberlist = [key._0, key._1, key._2, key._3, key._4, key._5, key._6, key._7, key._8, key._9]
        if self.step == 4:  # Fixture ID input step 
            for k, key_ in enumerate(standarddetector.numbers):
                if key_.button_press_and_release(keys[numberlist[k]]) == True:
                    self.input_text += str(k)
            if backspacedetector.button_press_and_release(keys[key.BACKSPACE]) == True:
                self.input_text = self.input_text[:-1]

    def calibration_mode(self):
        """
        Handles the logic of the calibration mode and runs the necessary functions for calibration to work
        """
        if self.step == 5:
            transmanager.position_fixture()
        calibrator.on_key_press()
        spherical_to_cartesian()
        send_OSC()
        calibrator.get_coordinates()


calibrator = Calibration()          #Calibration() class instance for the calibration process