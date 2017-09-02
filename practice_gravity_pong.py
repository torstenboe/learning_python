__author__ = 'torsten'

# GRAVITY PONG!!!
# By Barron, explained: https://www.youtube.com/watch?v=iU8x33LKMnA

import simplegui
import random

# global constants
FRAME_SIZE = [600, 400]
BALL_RADIUS = 20
BALL_COLOR = 'white'
PLAYER1_COLOR = 'white'
PLAYER2_COLOR = 'white'
PAD_WIDTH = 8
PAD_HEIGHT = 80
LEFT = False
RIGHT = True
PADDLE_ACC = 5 # accelerate rate of paddle
GRAVITY = [0, 1]
DAMPEN = .1 # friction due to deformation

class Ball:

    def __init__(self, radius, color):
        self.radius = radius
        self.color = color
        self.pos = [FRAME_SIZE[0]/2, FRAME_SIZE[1]/2]
        self.vel = [0, 0]
        self.acc = [0, 0]

    def update(self):

        # update y velocity (check for collision with top/bottom first)
        if self.radius * 2 < self.pos[1] + self.vel[1] + self.acc[1] + GRAVITY[1] + self.radius < FRAME_SIZE[1]:
            self.vel[1] += self.acc[1] + GRAVITY[1]
        else:
            self.vel[1] = -self.vel[1] * (1 - DAMPEN) # invert velocity for collision & apply friction

        # update position
        for d in range(2):
            self.pos[d] += self.vel[d]

        # check for ball collision with gutters
        if (self.pos[0] - self.radius < PAD_WIDTH): #left side collision
            if (self.pos[1] >= player1.get_pos()) and (self.pos[1] <= player1.get_pos() + PAD_HEIGHT): # is the paddle there?
                self.vel[0] = -self.vel[0] * 1.1 # invert x velocity and increase 10%
                self.vel[1] -= 1000 / (FRAME_SIZE[1] - self.pos[1]) # hit ball "upwards a bit" depending on how low it is
            else:
                player2.inc_score(1) # player 2 scored!
                self.spawn(RIGHT)
        elif (self.pos[0] + self.radius >= FRAME_SIZE[0] - PAD_WIDTH): # right side collision
            if (self.pos[1] >= player2.get_pos()) and (self.pos[1] <= player2.get_pos() + PAD_HEIGHT): # is the paddle there?
                self.vel[0] = -self.vel[0] * 1.1 # invert x velocity and increase 10%
                self.vel[1] -= 1000 / (FRAME_SIZE[1] - self.pos[1]) # hit ball "upwards a bit" depending on how low it is
            else:
                player1.inc_score(1) # player 1 scored!
                self.spawn(LEFT)

    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1, self.color, self.color)

    def spawn(self, direction):

        # place ball in middle of field
        self.pos = [FRAME_SIZE[0]/2, self.radius + 1]

        # generate random velocities
        self.vel[0] = random.randrange(2, 5) # 120 to 240 pixels/second @ 60Hz refresh
        self.vel[1] = random.randrange(-3, 0) # 60 to 180 pixels/second @ 60Hz refresh

        # configure initial velocities based on direction
        if direction == LEFT:
            self.vel[0] = -self.vel[0]

class Paddle:

    def __init__(self, side, pad_width, pad_height, color):
        self.side = side
        self.width = pad_width
        self.height = pad_height
        self.color = color
        self.pos = FRAME_SIZE[1]/2 - pad_height
        self.vel = 0
        self.score = 0

    def update(self):
        # update pos
        self.pos += self.vel

        # check for paddle position being off the screena nd adjust accordingly
        if self.pos < 1: # check if at top
            self.pos = 0
        elif self.pos + self.height >= FRAME_SIZE[1]: # check if at bottom
            self.pos = FRAME_SIZE[1] - self.height - 1

    def draw(self, canvas):
        # draw paddle & score
        if self.side == LEFT:
            canvas.draw_line((self.width/2, self.pos), (self.width/2, self.pos + self.height), self.width, self.color)
            canvas.draw_text(str(self.score), (FRAME_SIZE[0]/4, FRAME_SIZE[1]/6), 40, self.color)
        else:
            canvas.draw_line((FRAME_SIZE[0] - self.width/2, self.pos), (FRAME_SIZE[0] - self.width/2, self.pos + self.height), self.width, self.color)
            canvas.draw_text(str(self.score), (FRAME_SIZE[0]*3/4, FRAME_SIZE[1]/6), 40, self.color)

    def accelerate(self, acc):
           self.vel += acc

    def get_pos(self):
        return self.pos

    def inc_score(self, num):
        self.score += num

    def reset(self):
        self.pos = FRAME_SIZE[1]/2 - self.height
        self.vel = 0
        self.score = 0

class Field:

    def __init__(self):
        pass

    def draw(self, canvas):
        # draw mid line and gutters
        canvas.draw_line([FRAME_SIZE[0]/2, 0],[FRAME_SIZE[0]/2, FRAME_SIZE[1]], 1, "White")
        canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, FRAME_SIZE[1]], 1, "White")
        canvas.draw_line([FRAME_SIZE[0] - PAD_WIDTH, 0],[FRAME_SIZE[0] - PAD_WIDTH, FRAME_SIZE[1]], 1, "White")
        canvas.draw_text("GRAVITY PONG", (FRAME_SIZE[0]/4+16, FRAME_SIZE[1]/2), 40, "Grey")

def draw(canvas):

    # draw the field
    field.draw(canvas)

    # draw the paddles & scores
    player1.update()
    player2.update()
    player1.draw(canvas)
    player2.draw(canvas)

    # draw the ball
    ball.update()
    ball.draw(canvas)

def keyup(key):
    # inc/dec the paddle velocities accordingly
    if key == simplegui.KEY_MAP['w']: player1.accelerate(PADDLE_ACC)
    elif key == simplegui.KEY_MAP['s']: player1.accelerate(-PADDLE_ACC)
    elif key == simplegui.KEY_MAP['up']: player2.accelerate(PADDLE_ACC)
    elif key == simplegui.KEY_MAP['down']: player2.accelerate(-PADDLE_ACC)

def keydown(key):
    # inc/dec the paddle velocities accordingly
    if key == simplegui.KEY_MAP['w']: player1.accelerate(-PADDLE_ACC)
    elif key == simplegui.KEY_MAP['s']: player1.accelerate(PADDLE_ACC)
    elif key == simplegui.KEY_MAP['up']: player2.accelerate(-PADDLE_ACC)
    elif key == simplegui.KEY_MAP['down']: player2.accelerate(PADDLE_ACC)

def new_game():
    player1.reset()
    player2.reset()
    ball.spawn(LEFT)

# create game objects
field = Field()
ball = Ball(BALL_RADIUS, BALL_COLOR)
player1 = Paddle(LEFT, PAD_WIDTH, PAD_HEIGHT, PLAYER1_COLOR)
player2 = Paddle(RIGHT, PAD_WIDTH, PAD_HEIGHT, PLAYER2_COLOR)

# create frame
frame = simplegui.create_frame("Pong", FRAME_SIZE[0], FRAME_SIZE[1])
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.add_button("Restart", new_game)

new_game()
frame.start()
