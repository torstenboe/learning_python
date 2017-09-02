__author__ = 'torsten'

# Cipher

import simplegui
import random

CIPHER = {}
LETTERS = "abcdefghijklmnopqrstuvwxyz"

message = ""

def init():
      letter_list = list(LETTERS)
      random.shuffle(letter_list)
      for ch in LETTERS:
            CIPHER[ch] = letter_list.pop ()

# Encode button
def encode():
    emsg = ""
    for ch in message:
        emsg += CIPHER[ch]
    print message, "encodes to", emsg

# Decode button
def decode():
    dmsg = ""
    for ch in message:
        for key, value in CIPHER.items():
            if ch == value:
                dmsg += key
    print message, "decodes to", dmsg

# Update message input
def newmsg(msg):
    global message
    message = msg
    label.set_text(msg)

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Cipher", 2, 200, 200)
frame.add_input("Message:", newmsg, 200)
label = frame.add_label("", 200)
frame.add_button("Encode", encode)
frame.add_button("Decode", decode)

init()

# Start the frame animation
frame.start()
