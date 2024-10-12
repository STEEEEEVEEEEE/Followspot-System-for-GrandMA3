from pythonosc import udp_client
import pyglet
from pyglet.gl import *
from Code import *
from Calibration import *

trigger = joystick1.buttons[0]
standarddetector.create_button_instances()



class Cycle():
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


showstate_cycler = Cycle()
calibration_cycler = Cycle()

def show_mode():
    showstate = showstate_cycler.cycle(standarddetector.button_differentiating())

    if showstate == 0:
        bounds_state = out_of_bounds()

        if bounds_state == False:
            rectangle_movement()
            cartesian_to_spherical()
            send_cartesian_OSC()
            #send_OSC()
            #spherical_to_cartesian()
            labels.show_mode_label.text = f"Show"

        elif bounds_state == True:
            cartesian_movement(origin)
        #send_cartesian_OSC()
        labels.show_mode_label.text = f"Show"

    elif showstate == 1:
        labels.show_mode_label.text = f"No_Output"
        rectangle_movement()





#create_Fixtures(fixtures)
#center_and_distribute_fixtures(fixture_shapes, fixture_labels)
def update():
    
    calib_cycler_state = calibration_cycler.cycle(calibrator.initialization())
    if calib_cycler_state == 0:
        calibrator.calibration_mode()
        rectangle_movement()
        spherical_to_cartesian()
        send_OSC()
    elif calib_cycler_state == 1:
        show_mode()
    

def on_draw(dt):
    light_parameters()
    labels.update_labels()
    window.clear()
    batch.draw()
    label.draw()
    update()    

on_draw(1)



pyglet.clock.schedule_interval(on_draw, 1/60.0)
pyglet.app.run()