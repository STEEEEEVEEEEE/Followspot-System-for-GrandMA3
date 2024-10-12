import pyglet
from pyglet.gl import *
from Code import *



class Calibration:
    def __init__(self):
        self.step = 0
        self.calib_state = False
        self.coordinate = []

    def initialization(self):
        if joystick1.buttons[2] == True and joystick1.buttons[3] == True:
            self.calib_state = True
        else:
            self.calib_state = False
        if standarddetector.button_press_and_release(self.calib_state) == True:
            self.step = 0
            return 2

    def write_to_file(self, line1, line2, line3, line4):
        with open("Calibration.txt", "w") as file:
            line1 = line1 + "\n"
            line2 = line2 + "\n"
            line3 = line3 + "\n"
            line4 = line4 + "\n"
            file.write(line1)
            file.write(line2)
            file.write(line3)
            file.write(line4)


    def get_coordinates(self):
        labels.next_step(self.step)
        if self.step == 3 and standarddetector.button_differentiating() == 1:
            self.coordinate.append(str((spherical_to_cartesian())))
            calibrator.write_to_file(str(self.coordinate[0]), str(self.coordinate[1]), str(self.coordinate[2]), str(self.coordinate[3]))
            print("hell yeah")
            self.step = (self.step + 1) % 5          

        if self.step == 4:
            if standarddetector.button_differentiating() == 1:
                self.coordinate = []
                self.step = (self.step + 1) % 5

        else:
            if standarddetector.button_differentiating() == 1:
                self.coordinate.append(str((spherical_to_cartesian())))
                self.step = (self.step + 1) % 5
        

    def calibration_mode(self):
        calibration_batch.draw()
        spherical_to_cartesian()
        send_OSC()
        calibrator.get_coordinates()




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













