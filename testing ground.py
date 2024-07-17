def check_collision(rect1, rect2):
    """Checks if two pyglet.shapes.Rectangle objects are colliding."""
        # Check for NO overlap in the x-axis (this means they DO NOT collide)
    if (rect1.x + rect1.width >= rect2.x) or (rect2.x + rect2.width >= rect1.x):
        print("Collision")
        return False

    # Check for NO overlap in the y-axis (this means they DO NOT collide)
    if (rect1.y + rect1.height <= rect2.y) or (rect2.y + rect2.height <= rect1.y):
        #print("NONE")
        return False
    else:
        # If we got here, then there is overlap on BOTH axes, meaning a collision
        #print(f"Collision")
        return True
    



for i in range(fixtures):
    fix = i
    y = y_middle
    x = x_middle -  window.width // 4 + window.width // 15 * (i * fixtures)
    size = window.height // 10
    label = pyglet.text.Label(f"Fixture {i + 1}", x=x + size // 2, y=y + size // 2, font_size=window.height // 100, anchor_x='center', batch=batch, color=(0,0,0,150))
    fixture_labels.append(label)
    fixture = pyglet.shapes.Rectangle(x, y, size, size, color=(255, 255, 255), batch=batch)
    fixture_shapes.append(fixture)