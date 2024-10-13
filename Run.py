from pythonosc import udp_client
import pyglet
from pyglet.gl import *
from Code import *
from Calibration import *

standarddetector.create_button_instances()      #generally used instance for Buttondetection() class



class Cycle():
    """Cycle class to enable multiple instances of cycling states"""
    def __init__(self):
        self.current_state = 1
        self.num_states = 2

    def cycle(self, input):
        """
        Cycles between multiple states
        
        Input: the num_states variable
        
        Changes the global current_state variable from state 0 to 
        """
        if input == 2:
            self.current_state = (self.current_state + 1) % self.num_states
        return self.current_state


showstate_cycler = Cycle()          #Cycle() class instances for different cycling purposes
calibration_cycler = Cycle()

def show_mode():
    """
    Handles the different showmode states and hierarchy of the different functions.
    """
    showstate = showstate_cycler.cycle(standarddetector.button_differentiating())

    if showstate == 0:                      #showmode is set to Show(OSC output enabled)
        labels.show_mode_label.text = f"Show"
        bounds_state = out_of_bounds()

        if bounds_state == False:           #out_of_bounds is false
            rectangle_movement()
            cartesian_to_spherical()
            send_cartesian_OSC()
            
        elif bounds_state == True:          #out_of_bounds is true
            cartesian_movement(origin)

    elif showstate == 1:                    #showmode is set to no-OSC-output
        labels.show_mode_label.text = f"No_Output"
        rectangle_movement()


def update():
    """
    Handles the differentiation between showmode and calibration mode.
    """
    calib_cycler_state = calibration_cycler.cycle(calibrator.initialization())  #To be in calibration or not to be in calibration, that is the question
    if calib_cycler_state == 0:
        calibrator.calibration_mode()
        rectangle_movement()
        spherical_to_cartesian()
        send_OSC()
    elif calib_cycler_state == 1:
        show_mode()
    

def on_draw(dt):
    """
    Responsible for drawing the different elements of the user-interface and runs the update() function
    Is the main function that is run 60 times per second
    """
    light_parameters()
    labels.update_labels()
    window.clear()
    batch.draw()
    label.draw()
    update()    

on_draw(1)


pyglet.clock.schedule_interval(on_draw, 1/60.0)   #runs the on_draw() function on an interval of 60 hz
pyglet.app.run()                                  #runs the code