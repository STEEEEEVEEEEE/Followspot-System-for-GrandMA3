from Code import *
from out_of_bounds import *
from Math_trigonometry import *
import ast


class Transformation():
    """
    Class for the entire Transformation from cartesian to spherical. 
    Used for running multiple instances and being able to control multiple calibrated lights at once.(not implemented yet)
    """
    def __init__(self):
        self.coordinates = []
        self.cart_x, self.cart_y = 0, 0
        self.cart_pan = 0
        self.cart_tilt = 0

    def get_cart_pan(self):
        return self.cart_pan

    def get_cart_tilt(self):
        return self.cart_tilt
    
    def create_coordinates_from_file(self):
        """
        Takes the content of the Calibration.txt file and converts it to a list of the 4 stage-corner coordinates.

        Input(no arguments):
            Calibration.txt file
        
        Returns:
            self.coordinates list
        """
        if self.coordinates == []:
            with open('c:/Users/stefa/OneDrive/Matura Arbeit/Repository Clone/MA/Calibration.txt', "r") as file:
                lines = file.readlines()
                for line in lines:                          #iterates over lines in .txt file
                    line = line.rstrip("\n")                #removes newline character from string
                    line_tuple = ast.literal_eval(line)     #converts string to tuple
                    self.coordinates.append(line_tuple)   
        print(self.coordinates) 
        return self.coordinates


                                                                                       # bottom-left of the stage is 0,0 and top-right 100,100




    def translate_to_quadrilateral(self, corners):
        """
        Translates coordinates from a normalized 0-100 system to a quadrilateral defined by its corners.

        Args:
            corners: A list of four tuples representing the corners of the quadrilateral:
                    [(bottom_left_x, bottom_left_y), 
                    (bottom_right_x, bottom_right_y), 
                    (top_left_x, top_left_y), 
                    (top_right_x, top_right_y)]

        Input:
                The x and y values from the cartesian_movement() function

        Returns:
            A tuple (x, y) representing the translated coordinates in the quadrilateral's space.
        """
        self.cart_x, self.cart_y = rectangle_movement()[0], rectangle_movement()[1]
        input_x, input_y = self.cart_x, self.cart_y
        print(corners)
        bl, br, tl, tr = corners
        
        # Interpolate along the bottom and top edges based on input_x
        bottom_x = bl[0] + (br[0] - bl[0]) * (input_x / 100)
        bottom_y = bl[1] + (br[1] - bl[1]) * (input_x / 100)
        top_x = tl[0] + (tr[0] - tl[0]) * (input_x / 100)
        top_y = tl[1] + (tr[1] - tl[1]) * (input_x / 100)

        # Interpolate between the bottom and top points based on input_y
        final_x = bottom_x + (top_x - bottom_x) * (input_y / 100)
        final_y = bottom_y + (top_y - bottom_y) * (input_y / 100)
        
        return final_x, final_y


    state = False
    overflow = False

    def cartesian_to_spherical(self):
        """
        Transforms the interpolated values from the translate_to_quadrilateral 
        function to the spherical coordinate system.

        Input(already in the code, no arguments):
            Interpolated values from translate_to_quadrilateral() function.
            z: should be the same as in the spherical_to_cartesian() function for accurate results

        Returns:
            A tuple (cart_pan, cart_tilt) representing the transformed values in the spherical coordinate system(pan/tilt).
        """

        global state
        state = outofboundser.out_of_bounds(pan, tilt)[0]
        self.cart_x, self.cart_y = transformer.translate_to_quadrilateral(transformer.create_coordinates_from_file())
        z = 4

        if state == False:             #checks where the moving head is positioned to adjust the mathematical functions so that it can seamlessly move to 
            if self.cart_y >= 0 and self.cart_x < 0:              #negative or positive values without weird jumps/inconsistencies
                r = (self.cart_x**2 + self.cart_y**2)**0.5
                self.cart_pan = (((Math_Trigo.arcsine(self.cart_x/r))+offset)+180)
                self.cart_tilt = -(Math_Trigo.arctan(r/z))
            elif self.cart_y < 0 and self.cart_x < 0:
                r = -((self.cart_x**2 + self.cart_y**2)**0.5)
                self.cart_pan = ((Math_Trigo.arcsine(self.cart_x/r))+offset)
                self.cart_tilt = (Math_Trigo.arctan(r/z))
            elif self.cart_y < 0 and self.cart_x > 0:
                r = -((self.cart_x**2 + self.cart_y**2)**0.5)
                self.cart_pan = ((Math_Trigo.arcsine(self.cart_x/r))+offset)
                self.cart_tilt = (Math_Trigo.arctan(r/z))
            elif self.cart_y >= 0 and self.cart_x > 0:
                r = -((self.cart_x**2 + self.cart_y**2)**0.5)
                self.cart_pan = -((Math_Trigo.arcsine(self.cart_x/r))+offset)
                self.cart_tilt = (Math_Trigo.arctan(r/z))
        elif state == True:
            if self.cart_y >= 0 and self.cart_x < 0:
                r = (self.cart_x**2 + self.cart_y**2)**0.5
                self.cart_pan = (((Math_Trigo.arcsine(self.cart_x/r))+offset)-180)
                self.cart_tilt = -(Math_Trigo.arctan(r/z))
            elif self.cart_y < 0 and self.cart_x < 0:
                r = -((self.cart_x**2 + self.cart_y**2)**0.5)
                self.cart_pan = (((Math_Trigo.arcsine(self.cart_x/r))+offset)-360)
                self.cart_tilt = (Math_Trigo.arctan(r/z))
            elif self.cart_y < 0 and self.cart_x > 0:
                r = -((self.cart_x**2 + self.cart_y**2)**0.5)
                self.cart_pan = ((Math_Trigo.arcsine(self.cart_x/r))+offset)
                self.cart_tilt = (Math_Trigo.arctan(r/z))
            elif self.cart_y >= 0 and self.cart_x > 0:
                r = -((self.cart_x**2 + self.cart_y**2)**0.5)
                self.cart_pan = -((Math_Trigo.arcsine(self.cart_x/r))+offset)
                self.cart_tilt = (Math_Trigo.arctan(r/z))




    def send_cartesian_OSC(self):
        """
        Sends the OSC command in the cartesian coordinate system and for the zoom and intensity values.
        
        Input(already in the code, no arguments): 
            cartesian value from cartesian_to_spherical() function
            zoom and intensity values from the light_parameters() function
        """
        global pan
        global tilt
        global state
        client.send_message("/gma3/cmd", f'At {light_parameters.zoom} Attribute "Zoom"')
        if self.cart_pan < 0:
            state = True
        elif self.cart_pan >= 0:
            state = False
        client.send_message("/gma3/cmd", f'At {self.cart_pan} Attribute "Pan"')
        client.send_message("/gma3/cmd", f'At {self.cart_tilt} Attribute "Tilt"')
        pan = self.cart_pan
        tilt = self.cart_tilt


    
transformer = Transformation()      #class instance of Transformation class
