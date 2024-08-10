from pythonosc import udp_client
import pyglet
from pyglet.gl import *
from Code import *
from Calibration import *


state = 0

def cycle(state):
    f = state
    switch_button = joystick1.buttons[1]
    button_press = button_press_and_release(switch_button)
    if button_press == True:
        if f != 2:
            f = f + 1
    return f

def show_mode():
    
    mode = cycle(state)
    #print(mode)
    if mode == 0:
        light_parameters()
        send_OSC()
        jstk_rect.postion = jstk_rectangle_movement()
        jstk_rect.anchor_position = jstk_rectangle_movement()[0] - x_middle, jstk_rectangle_movement()[1] - y_middle
        labels.update_labels()
        labels.show_mode_label.text = f"Show"
    if mode == 1:
        labels.update_labels()
        labels.show_mode_label.text = f"No_Output"
    if mode == 2:
        labels.show_mode_label.text = f"Edit"
        pass  

jstk_rect = pyglet.shapes.Rectangle(jx, jy, window.height // 15, window.height // 15, color=(255,0,0), batch=batch)


create_Fixtures(fixtures)
center_and_distribute_fixtures(fixture_shapes, fixture_labels)
def update():
    show_mode()
    

def on_draw(dt):
    window.clear()
    batch.draw()
    label.draw()
    update()    

on_draw(1)



pyglet.clock.schedule_interval(on_draw, 1/60.0)
pyglet.app.run()