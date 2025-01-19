from Code import *
import os
# Load the PNG image
image = pyglet.image.load((os.path.join('Sprites','logo_white1.png')))
sprite = pyglet.sprite.Sprite(image,x=window.width//1.17,y=window.height//60,batch=batch)
sprite.scale = window.width/window.height/3.75