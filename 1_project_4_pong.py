# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT]
paddle1_vel = [0,0]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2  - HALF_PAD_HEIGHT]
paddle2_vel = [0,0]
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    vel_h_range = random.randrange(120, 240)
    vel_v_range = random.randrange(60, 180)
    if direction == RIGHT:
        ball_vel = [vel_h_range / 60.0,  -vel_v_range / 60.0]
    else:
        ball_vel = [-vel_h_range / 60.0,  -vel_v_range / 60.0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, left_counter, right_counter
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # collide and reflect off of border of canvas
    if ball_pos[1] <= (BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT-(BALL_RADIUS - 1):
        ball_vel[1] = - ball_vel[1]
               
    # collide and reflect off of paddle
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        if (ball_pos[1] >= paddle1_pos[1]) and (ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT):
            ball_vel[0] = - (ball_vel[0] *1.1)
        else:
            score1 += 1
            spawn_ball(RIGHT)
    elif ball_pos[0] >= (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if (ball_pos[1] >= paddle2_pos[1]) and (ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT):
            ball_vel[0] = - (ball_vel[0] *1.1)
        else:
            score2 += 1
            spawn_ball(LEFT)   
    elif (ball_pos[1] == 0) or (ball_pos[1] >= HEIGHT-(BALL_RADIUS + 1)):
        ball_vel[1] = - ball_vel[1]
    else:
        ball_vel == ball_vel
        
    # update paddle's vertical position, keep paddle on the screenD_HEIGHT):
    paddle1_pos[1] += paddle1_vel[1]
    paddle2_pos[1] += paddle2_vel[1]
    
    if paddle1_pos[1] <= 0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
        
    if paddle2_pos[1] <= 0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] >= HEIGHT - PAD_HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT
         
    # draw paddles
    canvas.draw_line(paddle1_pos, [HALF_PAD_WIDTH, paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos, [WIDTH - HALF_PAD_WIDTH, paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH, "White")
    
    # draw scores
    canvas.draw_text(str(score2), (20, 30), 30, 'Grey')
    canvas.draw_text(str(score1), (WIDTH - 30, 30), 30, 'Grey')

def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 10
    if  key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] += acc
    elif  key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] -= acc

def keyup(key):
    global paddle1_vel, paddle2_vel
    if  key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    elif  key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0

def reset():
    global score1, score2
    score1 = 0
    score2 = 0
    new_game()     
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", reset, 200)

# start frame
new_game()
frame.start()