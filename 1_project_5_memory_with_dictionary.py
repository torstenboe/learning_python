__author__ = 'torsten'

import random
import simplegui

HEIGHT = 100
WIDTH = 800
CARDS = 16
exposed = {}
card_deck = []
state = 0
card_1 = 0
card_2 = 0
turns = 0

# Handler for new card
def new_game():
    global state, turns
    state = 0
    turns = 0
    mix_cards()
    return state, turns

def mix_cards():
    del card_deck[:]
    for n in range(CARDS / 2):
        card_deck.append(n+1)
        card_deck.append(n+1)
    random.shuffle(card_deck)
    for i in range(CARDS):
        exposed[i] = False

def click(pick):
    global state, card_1, card_2, turns
    select = pick[0] / (WIDTH / CARDS)
    if state == 0:
        state = 1
        card_1 = select
    elif state == 1 and exposed[select] == False:
        state = 2
        card_2 = select
        turns += 1
    elif state == 2 and exposed[select] == False:
#    else:
        state = 1
        if card_deck[card_1] != card_deck[card_2]:
            exposed[card_1] = False
            exposed[card_2] = False
        card_1 = select
    exposed[select] = True
    label.set_text('Turns: ' + str(turns))
    return state, card_1, card_2, turns

def draw(canvas):
    pos = [12, 64]
    counter = 0
    for x in card_deck:
        canvas.draw_text(str(card_deck[counter]), pos, (WIDTH / CARDS), "White")
        if exposed[counter] == True:
            canvas.draw_polygon([(pos[0]-12, 2), (pos[0]-12, (HEIGHT - 2)),  (pos[0]+38, (HEIGHT - 2)), (pos[0]+38, 2)], 2, 'Black')
        else:
            canvas.draw_polygon([(pos[0]-12, 2), (pos[0]-12, (HEIGHT - 2)),  (pos[0]+38, (HEIGHT - 2)), (pos[0]+38, 2)], 2, 'Black', 'Green')
        pos[0] += WIDTH / CARDS
        counter += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label('Turns: ')

# register event handlers
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

# get things rolling
new_game()
frame.start()