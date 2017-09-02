# Stopwatch Game
# A digital stopwatch that keeps track of the time in tenths of a second. The stopwatch should contain "Start", "Stop" and "Reset" buttons.


# import basic modules
import simplegui

# define global variables
counter = 0
hit = 0
match = 0
runstat = False

width = 400 # defined as a reference for the canvas
height = width / 16 * 9 # determined to keep proportion
button_width = 150 # defined as a reference for button
letter_height = width / 12 # defined as a reference for the font
letter_width = letter_height / 2 # determined to keep proportion, however accuracy depends on selected font

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    '''in tenths of seconds into formatted string A:BC.D
    (number) -> str

    Function that returns a string of the form A:BC.D where A, C and D
    are digits in the range 0-9 and B is in the range 0-5

    format(0) = 0:00.0
    format(11) = 0:01.1
    format(321) = 0:32.1
    format(613) = 1:01.3
    '''
    minutes = t // 600
    sec_tens = (t // 100) % 6
    sec_ones = (t // 10) % 10
    tenth_o_sec = t % 10
    return str(minutes) + ":" + str(sec_tens) + str(sec_ones) + "." + str(tenth_o_sec)

# define position for the hit/match counter
def space():
    if (hit // 10 != 0) and (match // 10 != 0):
        return 6
    elif (hit // 10 != 0) or (match // 10 != 0):
        return 5
    else:
        return 4


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global runstat
    timer.start()
    runstat = timer.is_running()

def stop():
    global hit, match, runstat
    runstat = timer.is_running()
    if runstat and (counter % 10 == 0):
        hit += 1
        match += 1
    elif runstat:
        hit += 1
    timer.stop()

def reset():
    global hit, match, counter, runstat
    counter = 0
    hit = 0
    match = 0
    runstat = False

# define event handler for timer with 0.1 sec interval
def tick():
    '''
    (number) -> number

    timer with an associated interval of 0.1 seconds whose
    event handler increments a global integer

    '''
    global counter
    counter += 1


# define draw handler
def draw(canvas):
    '''
    (number) -> str

    Function for the canvas that draws the current time
    dedcuted as increment

    0:00.0
    '''
    message = format(counter)
    canvas.draw_text(str(match) + " / " + str(hit), [width - (space() * letter_width),letter_height + 4], letter_height, "Yellow")
    canvas.draw_text(message, [width / 2 - 5 * letter_width, height / 2 + letter_height / 2], 2 * letter_height, "White")

# create frame
frame = simplegui.create_frame("Stopwatch", width, height)
frame.add_button("Start", start, button_width)
frame.add_button("Stop", stop, button_width)
frame.add_button("Reset", reset, button_width)
frame.set_draw_handler(draw)


# register event handlers
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()
