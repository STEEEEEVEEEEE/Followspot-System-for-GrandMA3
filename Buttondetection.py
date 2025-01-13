from Code import *

class Buttondetection:
    """
    Class for handling single-input button presses (built-in pyglet function handles continuous button presses)
    """
    def __init__(self):
        self.button_pressed = False
        self.button_type = 0
        self.detectors = []
        self.numberlist = [key._0, key._1, key._2, key._3, key._4, key._5, key._6, key._7, key._8, key._9]
        self.numbers = []

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

    def create_number_instances(self):
        """
        Assigns the button_press_and_release() function to the different number keys on the keyboard
        """
        for i in self.numberlist:
            i = Buttondetection()
            self.numbers.append(i)

standarddetector = Buttondetection()
seconddetector = Buttondetection()
backspacedetector = Buttondetection()