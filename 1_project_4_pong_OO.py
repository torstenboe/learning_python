# A version of Pong

import simplegui
import random
import math

class GameState:
    def __init__(self, screen, level, score = 0, lives = 3, time = 0, started = False):
        self.screen = screen if screen is not None else 'small'
        self.screen_sizes = {'xsmall': [600, 400], 'small': [800, 600], 'medium': [1024, 768], 'large': [1440, 1080]}
        self.ball_radius = self.screen_sizes[self.screen][1] / 20
        self.paddle_length = self.screen_sizes[self.screen][1] / 5
        self.paddle_width = self.screen_sizes[self.screen][1] / 50
        self.color = 'White'
        self.level = level
        self.stages = (5, 10, 15, 25, 30, 35, 50, 75)
        self.score = score
        self.lives = lives
        self.time = time
        self.started = started
        
    def screen_width(self):
        return self.screen_sizes[self.screen][0]

    def screen_height(self):
        return self.screen_sizes[self.screen][1]

    def ball_radius(self):
        return self.ball_radius

    def paddle_length(self):
        return self.paddle_length

    def paddle_width(self):
        return self.paddle_width

    def set_level(self, level):
        self.level = level

    def add_level(self, level):
        self.level += level

    def get_level(self):
        return self.level

    def get_stages(self):
        return self.stages

    def set_lives(self, lives):
        self.lives = lives

    def sub_lives(self):
        self.lives -= 1

    def get_lives(self):
        return self.lives

    def set_score(self, score):
        self.score = score

    def add_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def set_started(self, started):
        self.started = started

    def is_started(self):
        return self.started

game = GameState('small', 1)

# math helper function
def dot(v, w):
    return v[0] * w[0] + v[1] * w[1]

def paddle_range(ball):
    hit = False
    radius = ball.get_radius() + game.paddle_width
    center = ball.get_position()
    paddle_range = game.paddle_length
    for paddle in paddles:
        paddle_pos = paddle.get_position()
        if (abs(paddle_pos[0] - center[0]) < radius) and (0 <= center[1] - paddle_pos[1]  <= paddle_range):
            hit = True
    return hit
    
class RectangularDomain:
    def __init__(self):
        self.width = game.screen_width()
        self.height = game.screen_height()
        self.border = 1
        
    # return if ball is inside the domain    
    def in_width(self, center, radius):
        return ((radius + self.border) < center[0] < (self.width - self.border - radius))

    def in_height(self, center, radius):
        return ((radius + self.border) < center[1] < (self.height - self.border - radius))

    # return a unit normal to the domain boundary point nearest center
    def normal(self, center):
        left_dist = center[0]
        right_dist = self.width - center[0]
        top_dist = center[1]
        bottom_dist = self.height - center[1]
        if left_dist < min(right_dist, top_dist, bottom_dist):
            return (1, 0)
        elif right_dist < min(left_dist, top_dist, bottom_dist):
            return (-1, 0)
        elif top_dist < min(bottom_dist, left_dist, right_dist):
            return (0, 1)
        else:
            return (0, -1)

    # return random location
    def random_pos(self, radius):
        x = random.randrange(radius, self.width - radius - self.border)
        y = random.randrange(radius, self.height - radius - self.border)
        return [x, y]

    # Draw boundary of domain
    def draw(self, canvas):
        canvas.draw_polygon([[0, 0], [self.width, 0], 
                             [self.width, self.height], [0, self.height]], self.border*2, "Black")
            
class Ball:
    def __init__(self, domain, vel = 3):
        self.radius = game.ball_radius
        self.color = game.color
        self.domain = domain
        self.pos = [game.screen_width()/2, game.screen_height()/2]
#        self.pos = self.domain.random_pos(self.radius)
        self.vel = [random.random() + vel, random.random() + vel]
        
    # reflect ball from walls
    def reflect(self):
        norm = self.domain.normal(self.pos)
        norm_length = dot(self.vel, norm)
        self.vel[0] = self.vel[0] - 2 * norm_length * norm[0]
        self.vel[1] = self.vel[1] - 2 * norm_length * norm[1]
        
    # update ball position
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if not self.domain.in_height(self.pos, self.radius):
            self.reflect()
        elif paddle_range(self):
            self.reflect()

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    # draw
    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1, 
                           self.color, self.color)
        
class Paddle:
    def __init__(self, pos, incr = 10):
        self.pos = [pos[0], pos[1]]
        self.vel = 0
        self.incr = incr
        self.width = game.paddle_width
        self.length = game.paddle_length
    
    def update(self):
        if self.length / 2 <= self.pos[1] + self.vel <= game.screen_height() - self.length / 2:
            self.pos[1] = (self.pos[1] + self.vel)

    def draw(self, canvas):
        canvas.draw_line([self.pos[0], self.pos[1] - self.length / 2], [self.pos[0], self.pos[1] + self.length / 2], 
                         self.width, "White")
    def move_up(self):
        self.vel -= self.incr

    def move_down(self):
        self.vel += self.incr

    def stop_moving(self):
        self.vel = 0

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def get_position(self):
        return self.pos
        
# generic update code for ball physics
def draw(canvas):

    canvas.draw_line([game.screen_width() / 2, game.screen_height()], [game.screen_width() / 2, 0], 
                     1, game.color)
    canvas.draw_line([game.paddle_width, game.screen_height()], [game.paddle_width, 0], 
                     4, game.color)
    canvas.draw_line([game.screen_width() - game.paddle_width, game.screen_height()], 
                     [game.screen_width() - game.paddle_width, 0], 4, game.color)

    ball.update()
    for paddle in paddles:
        paddle.update()    

    field.draw(canvas)
    ball.draw(canvas)
    for paddle in paddles:
        paddle.draw(canvas)


def keydown(key):
    for i in move_up:
        if key == simplegui.KEY_MAP[i]:
            move_up[i]()

    for i in move_down:
        if key == simplegui.KEY_MAP[i]:
            move_down[i]()

def keyup(key):
    for i in stop_moving:
        if key == simplegui.KEY_MAP[i]:
            stop_moving[i]()

frame = simplegui.create_frame("Pong", game.screen_width(), game.screen_height())

# create two paddle instances
paddle_l = Paddle([game.paddle_width / 2, game.screen_height() / 2])
paddle_r = Paddle([game.screen_width() - game.paddle_width / 2, game.screen_height() / 2])
paddles = set([paddle_l, paddle_r])

# Inputs for keyboard handler
move_up = {"up": paddle_r.move_up, "w": paddle_l.move_up}
move_down = {"down": paddle_r.move_down, "s": paddle_l.move_down}
stop_moving = {"up": paddle_r.stop_moving, "down": paddle_r.stop_moving, 
       "w": paddle_l.stop_moving, "s": paddle_l.stop_moving}

# register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

# get things rolling
field = RectangularDomain()
ball = Ball(field)
frame.start()