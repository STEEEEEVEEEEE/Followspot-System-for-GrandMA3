from Code import *

class Out_of_bounds():
    """
    Class for the out_of_bounds message
    """
    def __init__(self):
        self.tilt_label_color = (255,255,255,255)
        self.pan_label_color = (255,255,255,255)

    def out_of_bounds(self):
        """
        Checks if the pan/tilt values are close to or exceeding the maximum rotational angle of the fixture

        Slowly turns the pan/tilt labels red if the values are getting close
        and displays an "out of bounds" warning if they exceeded

        Returns:
            True if the values have not been exceeded

            False if they have been exceeded
        
        """
        state = False

        red_pan = int((abs(pan)-199)*2.857)
        red_tilt = int((abs(tilt)-79)*2.454)
        if abs(pan) <= 270 and abs(tilt) <= 135:
            state = False
        elif abs(pan) > 270 or abs (tilt) > 135:
            state = True
            outofbounds.draw()                  #out_of_bounds message appears if the pan or tilt maximum is exceeded

        if 255 > abs(pan) >= 200:
            self.pan_label_color = (255,-red_pan,-red_pan,255)
        if abs(pan) >= 255:
            self.pan_label_color = (255,0,0,255)
        elif abs(pan) < 200:
            self.pan_label_color = (255,255,255,255)
        if 135 > abs(tilt) > 80:
            self.tilt_label_color = (255,-red_tilt,-red_tilt,255)
        if abs(tilt) >= 135:
            self.tilt_label_color = (255,0,0,255)
        elif abs(tilt) < 80:
            self.tilt_label_color = (255,255,255,255)
        return state, self.pan_label_color, self.tilt_label_color       #state is used in the Run.py file to control OSC output
    

outofboundser = Out_of_bounds()       #Out_of_bounds() class instance for the out_of_bounds message