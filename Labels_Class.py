from Code import window, origin, pan, tilt, sens, intensity, cartesian_movement
from Code import label, control, calibration_batch, batch, outofbounds, x_middle
from Transformation_Class import transformer
from out_of_bounds import *
import pyglet


class Labels():   
    """
    A class that contains the parameters for all the labels that are displayed in the interface
    
    Also contains functions to dynamically change the values of the parameters
    """
    def __init__(self, trans_instance):
        self.trans_instance = trans_instance

        self.pan_label = pyglet.text.Label(f"Pan: {pan}", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 28,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)

        self.tilt_label = pyglet.text.Label(f"Tilt: {tilt}", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 14.7,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)

        self.sens_label = pyglet.text.Label(f"Sens: {sens}", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 10,
                anchor_x="left", 
                anchor_y="top",
                batch = label)

        """self.intens_label = pyglet.text.Label(f"Intens: {intensity}", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 5.94,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)"""

        self.zoom_label = pyglet.text.Label(f"Zoom: {light_parameters.zoom}", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 50, 
                y=window.height - window.height // 7.5,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)
        
        self.calibration_text = pyglet.text.Label(f"", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= x_middle, 
                y=window.height - window.height // 14,  
                anchor_x="center", 
                anchor_y="top",
                batch = calibration_batch)
        
        self.x_label = pyglet.text.Label(f"X-Position:", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 40, 
                y= window.height // 9,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)
        
        self.y_label = pyglet.text.Label(f"Y-Position:", 
                font_name="helvetica",
                font_size= window.height // 40,
                x= window.height // 40, 
                y= window.height // 14,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)
        
        self.show_mode_label = pyglet.text.Label(f"", 
                font_name="helvetica",
                font_size= window.height // 20,
                x= window.height // 40, 
                y= window.height // 5,  
                anchor_x="left", 
                anchor_y="top",
                batch = label)
        
        self.out_of_bounds_label = pyglet.text.Label(f"OUT OF BOUNDS", 
                color = (255, 0, 0, 255),
                font_name="helvetica",
                bold = True,
                font_size= window.height // 15,
                x= x_middle, 
                y= window.height // 1.2,  
                anchor_x="left", 
                anchor_y="top",
                batch = outofbounds)
        
        self.fixture_id_label = pyglet.text.Label("",
                font_name="helvetica",
                font_size= window.height // 40,
                x= x_middle,
                y=window.height - window.height // 8,
                anchor_x="center",
                anchor_y="top",
                batch = fixture_id_batch)
        
    def next_step(self, step):
        """
        Label text for the different calibration stages
        """
        location = []
        one = f"Please direct the Followspot-Light to the bottom-left and press trigger"
        two = f"Please direct the Followspot-Light to the bottom-right and press trigger"
        three = f"Please direct the Followspot-Light to the top-left and press trigger"
        four = f"Please direct the Followspot-Light to the top-right and press trigger"
        five = "Now please enter the Patch Address (keyboard input) of the fixture and press trigger"
        six = "Now please move the fixture (using arrow keys) to where it is rigged and press trigger"
        seven = "The coordinates have been saved, you may now exit the calibration mode"
        location.append([one, two, three, four, five, six, seven])
        labels.calibration_text.text = location[0][step]

    def update_labels(self):

        """
        Updates labels continuously to show the current values of the different parameters
        """
        x, y = cartesian_movement(origin)[1], cartesian_movement(origin)[2]
        pan = self.trans_instance.get_cart_pan()
        tilt = self.trans_instance.get_cart_tilt()
        labels.pan_label.text = f"Pan: {int(pan)}"
        labels.tilt_label.text = f"Tilt: {int(tilt)}"
        labels.sens_label.text = f"Sens: {int(sens * 495 - 8) }"
        """labels.intens_label.text = f"Intens: {int(intensity)}"""
        labels.zoom_label.text = f"Zoom: {int(light_parameters.zoom)}"
        labels.x_label.text = f"X-Position: {int(x)}"
        labels.y_label.text = f"Y-Position: {int(y)}"
        labels.pan_label.color = outofboundser.pan_label_color
        labels.tilt_label.color = outofboundser.tilt_label_color     
        



labels = Labels(transformer) #labels instance for the Labels() class