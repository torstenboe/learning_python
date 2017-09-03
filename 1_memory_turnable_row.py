import random
import simplegui

start = (50,75);
CARDS = 8;
deck = [];
expose = {};

# Mouseclick
def mouseclick(pos):
    x = start[0];
    select = pos[0] / (2 * x);
    expose[select] = True;
    print select;

# Create card deck
def card_deck():
    global deck,ser;
    for n in range(CARDS / 2):
        deck.append(n+1);
        deck.append(n+1);
    random.shuffle(deck);
    for j in range(CARDS):
        expose[j] = False;
    return deck;


# Handler to draw on canvas
def draw_handler(canvas):
    x = start[0];
    y = start[1];
    for i in range (0, CARDS):
        mid = (x + (2 * x *  i), y);
        if expose[i] == True:
            canvas.draw_text(str(deck[i]), mid, 36, 'white');
        else:
            canvas.draw_polygon([(mid[0]-40, mid[1]-65), (mid[0]+40, mid[1]-65), (mid[0]+40, mid[1]+65), (mid[0]-40, mid[1]+65)], 12, 'Green', 'Orange');

# Main code
card_deck();
print deck;

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame('Testing', 2 * start[0] * CARDS, 2 * start [1])
frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(mouseclick)

# Start the frame animation
frame.start()
