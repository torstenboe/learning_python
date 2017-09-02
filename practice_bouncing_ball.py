__author__ = 'torsten'

# A Bouncy Red Ball
# By Barron, explained: https://www.youtube.com/watch?v=iU8x33LKMnA

import simplegui

# global constants
FRAME_SIZE = [600, 400]
BALL_RADIUS = 20
BALL_COLOR = 'red'

# global variable
gravity = [0, 0] # start in "outer space!"

class Ball:

    def __init__(self, position, velocity, acceleration, radius, color):
        self.pos = position
        self.vel = velocity
        self.user_acc = acceleration # user applied acceleration
        self.acc = [0, 0] # total ball acceleration
        self.radius = radius
        self.color = color

    def update(self):
        # perform following operations for x & y dimension
        for d in range(2):

            # update acceleration
            self.acc[d] = self.user_acc[d] + gravity[d]

            # update velocity (check for collision first)
            if self.radius * 2 < self.pos[d] + self.vel[d] + self.acc[d] + gravity[d] + self.radius < FRAME_SIZE[d]:
                self.vel[d] += self.acc[d]# inside bounds - apply acceleration
            else:
                self.vel[d] = -self.vel[d] # collision - invert velocity

            # update position
            self.pos[d] += self.vel[d]

    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1, self.color, self.color)
        label_grav.set_text('Gravity Acc: ' + str(gravity))
        label_acc.set_text('Manual Acc: ' + str(self.user_acc))
        label_vel.set_text('Velocity: ' + str(self.vel))
        label_pos.set_text('Position: ' + str(self.pos))

    # apply a force to accelerate the ball
    def accelerate(self, acc):
        for d in range(2):
            self.user_acc[d] += acc[d]

def draw(canvas):
    ball.update()
    ball.draw(canvas)

def keydown(key):
    if key == simplegui.KEY_MAP['left']: ball.accelerate([-0.2, 0])
    elif key == simplegui.KEY_MAP['right']: ball.accelerate([0.2, 0])
    elif key == simplegui.KEY_MAP['up']: ball.accelerate([0, -0.2])
    elif key == simplegui.KEY_MAP['down']: ball.accelerate([0, 0.2])

def keyup(key):
    if key == simplegui.KEY_MAP['left']: ball.accelerate([0.2, 0])
    elif key == simplegui.KEY_MAP['right']: ball.accelerate([-0.2, 0])
    elif key == simplegui.KEY_MAP['up']: ball.accelerate([0, 0.2])
    elif key == simplegui.KEY_MAP['down']: ball.accelerate([0, -0.2])

def gravity_button():
    if gravity[1]: gravity[1] = 0
    else: gravity[1] = 1

def reset_button():
    global gravity, ball
    gravity = [0, 0]
    ball = Ball([FRAME_SIZE[0]/2, BALL_RADIUS + 1], [0, 0], [0, 0], BALL_RADIUS, BALL_COLOR)

# create ball
ball = Ball([FRAME_SIZE[0]/2, BALL_RADIUS + 1], [0, 0], [0, 0], BALL_RADIUS, BALL_COLOR)

# create frame
frame = simplegui.create_frame("Bouncy Ball!", FRAME_SIZE[0], FRAME_SIZE[1])
label_grav = frame.add_label('Gravity Acc: ')
label_acc = frame.add_label('Manual Acc: ')
label_vel = frame.add_label('Velocity: ')
label_pos = frame.add_label('Position: ')
frame.add_button("Toggle Gravity", gravity_button)
frame.add_button("Reset", reset_button)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
frame.start()
