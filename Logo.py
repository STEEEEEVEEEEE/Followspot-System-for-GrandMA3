from Code import *
import os
# Load the PNG image
image = pyglet.image.load((os.path.join('MA','Sprites','logo_white1.png')))
sprite = pyglet.sprite.Sprite(image,x=window.width//1.21,y=window.height//60,batch=batch)
sprite.scale = window.height/2160