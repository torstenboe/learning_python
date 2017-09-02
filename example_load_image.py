__author__ = 'torsten'

# Image positioning problem

###################################################
# Student should enter code below

import simplegui

# global constants
WIDTH = 400
HEIGHT = 300

# load test image
astroid_image = simplegui.load_image('http://i.imgur.com/P61gXGZ.png?1')
astroid_position = (WIDTH / 2, HEIGHT /2)


def get_width(image):
    return image.get_width()

def get_height(image):
    return image.get_height()


# mouseclick handler
def click(pos):
    global astroid_position
    astroid_position = pos


# draw handler
def draw(canvas):
    if get_width(astroid_image) > 0 and get_height(astroid_image) > 0:
        canvas.draw_image(astroid_image, (get_width(astroid_image) / 2, get_height(astroid_image) / 2), (get_width(astroid_image), get_height(astroid_image)), astroid_position, (get_width(astroid_image) / 10, get_height(astroid_image) / 10) )
    else:
        print "No image found"


# create frame and register draw handler
frame = simplegui.create_frame("Test image", WIDTH, HEIGHT)
frame.set_canvas_background("Gray")
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)


# start frame
frame.start()
