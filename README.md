# Followspot System for GrandMA3

This system serves as a tool to make controlling movers on a grandMA3 faster and easier, which also lets them be used as followspots.

Setup:

The IP-Adress and Console Port are defined at the top of the *Code.py* file.
Standard values are at 192.168.1.33 and Port 8000

In the grandMA3 software settings the OSC prefix has to be set to "gma3" (and of course OSC input has to be enabled).
You can find more information on the setup process under: https://help2.malighting.com/Page/grandMA3/remote_inputs_osc/en/1.8

The system can also be used with other consoles that support OSC, but the sent OSC message syntax has to be changed in the send_OSC() and send_cartesian_OSC() functions. Additionally, the setup process will be different.

The Joystick that was used to create this software is the Thrustmaster T.16000M
https://www.thrustmaster.com/en-gb/products/t-16000m-fcs-hotas/

It comes as a Joystick and a Throttle, and the throttle is used to control sensitivity and zoom.
Therefore the system will not work(not even run) if only one Joystick is used.
Also, the axes are mapped to this specific controller so the control scheme might be unintuitive on other joysticks.

Support for other varieties of joysticks might come later.

Running the system:

This system is intended to be run on a PC or Laptop that is connected to the grandMA3 Network (preferably via Ethernet).

To start the software, run the *Run.py* file. A fullscreen window of the user-interface should appear.

Now press the 3rd and 4th button on the main joystick simultaneously (pressing the 2nd will, at the time of writing this, probably crash the software). You should enter a calibration mode and it will tell you to direct the mover to the bottom-left of the stage(from your perspective, not stage-right). Press the 1st button(probably the trigger). 

If you did everything right, you should now be able to control the pan and tilt axes directly with the joystick. Otherwise, there might be something wrong with the grandMA3 or some Network settings.

Everytime you position the light you will have to press trigger(or 1st button) and it will go to the next step.
Finally, it will tell you that you can leave calibration mode by pressing the 3rd and 4th button again and the stage-corner-coordinates should be stored in a Calibration.txt file. Doing the calibration procedure again will create a new calibration file, but the assignment to fixture numbers has not been done yet.

Now you can press the 2nd Button of the main Joystick. The showmode should change from *No_Output* to *Show.*
Since the mover has been calibrated, you should be able to control it on the x- and y-axis and the system will automatically calculate the pan and tilt values.

If you move too closely to the maximum or minimum pan value(-270 or 270) it will automatically reset to a safer number, so the mover will spin around one time.
