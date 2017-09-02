__author__ = 'torsten'


# One player game "Guess the number"

# The game let's player guess a number out of a range with a limited number of guesses. Input will come from buttons
# and an input field. All output for the game will be printed in the console

import simplegui
import random

# Initialize global variables that contain the state of the gam
guess_number = 0
counter = 0

# Define helper functions

def new_game():
    # initialize global variables used in your code here
    global secret_number, counter
    secret_number = 0
    counter = 0

def report_status(guess_number):
    ''' (number) -> str

    Return the result (You got it, to high, to low)
    for a guess that matches the secret or not.
    Pre-condition: guess within range

    >>> report_status(0)
    "higher"
    >>> report_status(100)
    "lower"
    >>> report_status(50)
    "match"
    '''
    if counter > 0:
        if guess_number == secret_number:
            return "match"
        elif secret_number < guess_number:
            return "lower"
        else:
            return "higher"
    else:
        return "You lost"

# Define event handler functions
def range100():
    ### Button that changes the value range to range (0,100)and restarts
    global secret_number, counter
    secret_number = random.randint(1, 100)
    counter = 7
    print "Selected range: 0 - 100, number of guesses: 7"


def range1000():
    ### Button that changes the value range to range (0,1000)and restarts
    global secret_number
    global counter
    secret_number = random.randint(1, 1000)
    counter = 10
    print "Selected range: 0 - 100, number of guesses: 10"


def input_guess(guess):
    # main game logic
    global guess_number, counter
    guess_number = int(guess)
    counter -= 1
    if counter < 0:
        print "Select a range to start the game"
        return new_game()
    else:
        print "Guesses left:", counter
        print report_status(guess_number)

# Create a frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# Register event handlers

frame.add_button("0 - 100", range100, 200)
frame.add_button("0 - 1000", range1000, 200)
frame.add_input("Enter Guess", input_guess, 200)
frame.add_button("New Game", new_game, 100)


# start frame & timers
new_game()