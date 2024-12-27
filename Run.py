from pythonosc import udp_client
import pyglet
from pyglet.gl import *
from Code import *
from Calibration import *
from Labels_Class import *
from out_of_bounds import *
from Transformation_Class import *

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
        bounds_state = outofboundser.out_of_bounds(pan, tilt)[0]

        if bounds_state == False:           #out_of_bounds is false
            
            transformer.cartesian_to_spherical()
            transformer.send_cartesian_OSC()
            
        elif bounds_state == True:          #out_of_bounds is true
            cartesian_movement(origin)

    elif showstate == 1:                    #showmode is set to no-OSC-output
        labels.show_mode_label.text = f"No_Output"
        rectangle_movement()


def update(dt):
    """
    Handles the differentiation between showmode and calibration mode and is also the main logic function. Is run 30 times per second.
    """

    update.calib_cycler_state = calibration_cycler.cycle(calibrator.initialization())  #To be in calibration or not to be in calibration, that is the question
    if update.calib_cycler_state == 0:
        calibrator.calibration_mode()
        rectangle_movement()
    elif update.calib_cycler_state == 1:
        show_mode()
    light_parameters()
    labels.update_labels()

update.calib_cycler_state = 1 #safety measure to ensure that the code doesn't crash if the update.calib_cycler_state is called in "ondraw" before the update() function is called

def on_draw(dt):
    """
    Responsible for drawing the different elements of the user-interface 
    Is run 60 times per second.
    """

    window.clear() 
    batch.draw()
    label.draw()
    if update.calib_cycler_state == 0:
        calibration_batch.draw()
     
    



pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.clock.schedule_interval(on_draw, 1/60.0)   #runs the on_draw() function on an interval of 60 hz
pyglet.app.run()                                  #runs the code