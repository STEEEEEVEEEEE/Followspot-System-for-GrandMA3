import pyglet
from pyglet.gl import *

joysticks = pyglet.input.get_joysticks()
assert joysticks, 'Kein Joystick verbunden'
joystick1 = joysticks[0]
joystick1.open()

window = pyglet.window.Window(height = 1000, width = 1500)
window.set_caption("Lightcontroller")
batch = pyglet.graphics.Batch()
background = pyglet.shapes.Rectangle(0,0, window.width, window.height, color=(100,100,100), batch=batch)

fixture_labels = []
fixture_shapes = []
fixtures = 3
jx = window.width // 2
jy = window.height // 2
    
def check_collision(rect1, rect2):
    """Checks if two pyglet.shapes.Rectangle objects are colliding."""
        # Check for NO overlap in the x-axis (this means they DO NOT collide)
    if (rect1.x + rect1.width <= rect2.x) or (rect2.x + rect2.width <= rect1.x):
        print("NONE")
        return False

    # Check for NO overlap in the y-axis (this means they DO NOT collide)
    if (rect1.y + rect1.height <= rect2.y) or (rect2.y + rect2.height <= rect1.y):
        print("NONE")
        return False
    else:
        # If we got here, then there is overlap on BOTH axes, meaning a collision
        print(f"Collision")
        return True



for i in range(fixtures):
    fix = i
    y = window.height // 2
    x = window.width // 2 -  window.width // 4 + window.width // 15 * (i * fixtures)
    size = window.height // 10
    label = pyglet.text.Label(f"Fixture {i + 1}", x=x + size // 2, y=y + size // 2, font_size=window.height // 100, anchor_x='center', batch=batch, color=(0,0,0,150))
    fixture_labels.append(label)
    fixture = pyglet.shapes.Rectangle(x, y, size, size, color=(255, 255, 255), batch=batch)
    fixture_shapes.append(fixture)



jstk_rect = pyglet.shapes.Rectangle(jx, jy, window.height // 15, window.height // 15, color=(255,0,0), batch=batch)
jstk_rect.anchor_position = jx, jy
def on_joyaxis_motion():
    global jx
    global jy
    
    jx = jx - (joystick1.x + 1.5259021896696368e-05) * window.height // 150
    jy = jy + (joystick1.y + 1.5259021896696368e-05) * window.height // 150      
    return jx, jy

@window.event
def on_draw():
    window.clear()
    batch.draw()
    
    collision = check_collision(jstk_rect, fixture_shapes[0])
    collision2 = check_collision(jstk_rect, fixture_shapes[1])
    collision3 = check_collision(jstk_rect, fixture_shapes[2])
    joyx, joyy = on_joyaxis_motion()
    jstk_rect.postion = joyx, joyy
    jstk_rect.anchor_position = joyx, joyy
    

        



pyglet.app.run()
