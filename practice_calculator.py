__author__ = 'torsten'

# A simple caculator

# Exposing basic mathmatical functions, using simplegui

import simplegui

# Step 1: Initialize global variables (define program state)
store = 0
operand = 0

# Step 2: Define helper functions

# Step 3: Classes (later)

# Step 4: Define event handler functions
# Manipulate store and operand
def output():
    ### print output contents of store and operand ###
    print "Store ", store
    print "Operand ", operand
    print ""

def swap():
    ### swap contents of store and operand ###
    global store, operand
    store operand = operand, store
    output()

def add():
    ### add operand to store ###
    global store, operand
    store = store + operand
    output()

def sub():
    ### subtract operand from store ###
    global store, operand
    store = store - operand
    output()

def mult():
    ### multiply store by operand ###
    global store, operand
    store = store * operand
    output()

def div():
    ### divide store by operand ###
    global store, operand
    store = store / operand
    output()

def exp():
    ### expone store by operand ###
    global store, operand
    store = store ** operand
    output()

def enter(inp):
    global operand
    operand = float(inp)
    output()

# Step 5: Create a frame
frame = simple_gui.create_frame("Calculator", 200, 200)

# Step 6: Register event handlers
frame.add_button("Print", output, 100)
frame.add_button("swap", swap, 100)
frame.add_button("Add", add, 100)
frame.add_button("Sub", sub, 100)
frame.add_button("Mult", mult, 100)
frame.add_button("Div", div, 100)
frame.add_button("Exp", exp, 100)

frame.add_input("Enter operand", enter, 100)

# Step 7; start frame & timers
frame.start()

