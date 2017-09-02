__author__ = 'torsten'

# An Inspiring Moment in the History of Physics
# By Barron, explained: https://www.youtube.com/watch?v=iU8x33LKMnA

import simplegui

# global constant
FRAME_SIZE = [300, 550]

# global variable
gravity = [0, 0.05]

class Apple:

    def __init__(self, position, velocity):
        self.pos = position
        self.vel = velocity
        self.acc = gravity

    def update(self):

        # perform following operations for x & y dimension
        for d in range(2):

            # update acceleration
            self.acc[d] = gravity[d]

            # update velocity
            self.vel[d] += self.acc[d]

            # update position
            self.pos[d] += self.vel[d]

    def draw(self, canvas):
        canvas.draw_image(image_apple, (285/2, 299/2), (285, 299), self.pos, (285/8, 299/8))

def draw(canvas):

    # draw Isaac
    canvas.draw_image(image_newton, (407/2, 559/2), (407, 559), (FRAME_SIZE[0]/2, FRAME_SIZE[1]-50), (407/3, 559/3))

    # draw apple
    apple.update()
    apple.draw(canvas)

    # update acceleration and velocity labels
    acc_label.set_text("Gravity Acc: " + str(gravity))
    vel_label.set_text("Velocity: " + str(apple.vel))

def gravity_button():
    # toggle gravity on/off
    if gravity[1] == 0: gravity[1] = 0.05
    else: gravity[1] = 0

def reset_button():
    global apple
    gravity[1] = 0
    apple = Apple([FRAME_SIZE[0]/2, 30], [0, 0])

# create apple
apple = Apple([FRAME_SIZE[0]/2, 30], [0, 0])

# load images
image_apple = simplegui.load_image("http://www.clker.com/cliparts/3/7/5/6/11949861182029597463an_apple_01.svg.med.png")
image_newton = simplegui.load_image("http://upload.wikimedia.org/wikipedia/commons/3/39/GodfreyKneller-IsaacNewton-1689.jpg")

# create frame
frame = simplegui.create_frame("An Inspiring Moment", FRAME_SIZE[0], FRAME_SIZE[1])
frame.set_draw_handler(draw)
acc_label = frame.add_label("Gravity Acc:")
vel_label = frame.add_label("Velocity:")
frame.add_button("Toggle Gravity", gravity_button)
frame.add_button("Reset", reset_button)

# start frame
frame.start()

