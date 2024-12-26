import math

class Math_Trigo():
    """
    A class with trigonometric functions that use degrees instead of radians that are used by the official math module
    """

    def sine(degrees):
        """Calculates the sine of an angle given in degrees."""
        radians = math.radians(degrees)  # Convert degrees to radians
        sine_value = math.sin(radians)
        return sine_value   # Convert the result back to degrees

    def tan(degrees):
        """Calculates the tangent of an angle given in degrees"""
        radians = math.radians(degrees)
        tangent_value = math.tan(radians)
        return tangent_value

    def cosine(degrees):
        """Calculates the cosine of an angle given in degrees"""
        radians = math.radians(degrees)
        cosine_value = math.cos(radians)
        return cosine_value

    def arctan(ratio):
        """Calculates the arctan of the ratio between two cathetes, output in degrees"""
        rat = math.atan(ratio)
        tangent_angle = math.degrees(rat)
        return tangent_angle
    
    def arcsine(ratio):
        """Calculates the arcsine of the ratio between a cathetus and the hypotenuse, output in degrees"""
        rat = math.asin(ratio)
        sine_angle = math.degrees(rat)
        return sine_angle      