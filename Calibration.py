import pyglet
from pyglet.gl import *
from Code import *



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
        Handles the joystick input of the 3rd and 4th button on the joystick
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

    def write_to_file(self, lines):
        """
        Writes the list of 4 stage-corner coordinates to a Calibration.txt file

        Arguments:
            list with 4 tuples (x/y coordinates)
        """
        with open("Calibration.txt", "w") as file:
            for line in lines:
                line = str(line) + "\n"
                file.write(line)


    def get_coordinates(self):
        """
        Cycles through the different calibration steps on each trigger pull and takes the transformed cartesian coordinates to
        write them to a Calibration.txt file with the write_to_file() function
        """

        labels.next_step(self.step)                         
        if self.step == 3 and standarddetector.button_differentiating() == 1:    #if the trigger is pulled when 3 of the coordinates have been collected:
            self.coordinate.append(str((spherical_to_cartesian())))              #append last coordinate
            calibrator.write_to_file(self.coordinate)                            #write the coordinates to the calibration file                                   #
            self.step = (self.step + 1) % 5                                      #show the next label step (confirmation)

        if self.step == 4:                                                       
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
        calibration_batch.draw()
        spherical_to_cartesian()
        transformer.send_OSC()
        calibrator.get_coordinates()




class Buttondetection:
    """
    Class for handling single-input button presses (built-in pyglet function handles continuous button presses)
    """
    def __init__(self):
        self.button_pressed = False
        self.button_type = 0
        self.detectors = []

    def button_press_and_release(self, button):
        """
        Changes a continuous True state into a single-input event

        Input: 
            Button or bool to detect state

        Returns:
            single True state when button is pressed(otherwise False)
        """
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
        """
        Uses the button_press_and_release() function to universally detect which button is pressed

        Input(no arguments):
            joystick1 Buttons

        Returns:
            Index of the pressed button (!starts counting from 1, not 0!)
        """

        for i, detector in enumerate(self.detectors):
            if detector.button_press_and_release(joystick1.buttons[i]) == True:
                self.button_type = i + 1
                print(f"Button {self.button_type} pressed (single click)")
                return self.button_type      
        
    def create_button_instances(self):
        """
        creates the amount of button instances to be used in the button_differentiating() function
        amount created is proportional to amount present on the joystick
        """
        for i in joystick1.buttons:
            i = Buttondetection()
            self.detectors.append(i)


standarddetector = Buttondetection()
seconddetector = Buttondetection()
calibrator = Calibration()













