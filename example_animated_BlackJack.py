# K
# Coursera/Rice IIPP 2
# Mini-project #6 - Blackjack
# April, 2015

# This implements the Blackjack game as specified in the 
# grading rubric.
# 
# With this project, I decided to get into the true spirit
# of object-oriented programming.  That explains the name 
# of the program: O'Blackjack.
#     
# I put in a couple enhancements: animation and a 
# parameterized geometry.  They tripled the length of the 
# code and multiplied the development time by nine.  Funny 
# how that works. :)  But after several redesigns, I'm 
# fairly satisfied with the code, and even a little proud of 
# it.  Here I give an overview, hopefully suitable for beginners.
# 
# I made it easy to vary the absolute and relative sizes of 
# the canvas and objects to suit your taste and screen size.  
# It works pretty well, despite some imperfections in the 
# placement of messages on the canvas.  If you change the 
# proportions, there may be a need to tidy things up a little.  
# The main geometric parameters are O_MAG, C_MAG, CANVAS_X, 
# and CANVAS_Y.  The constructors of the deck and hands determine 
# the placements of those objects on the canvas.
# 
# The bigger job was implementing animation.  
# 
# One of the basic concepts used is that of sending an object.  
# A Card has both a location and a destination.  If the two are 
# the same, then the card is stationary.  If they differ, the 
# object moves toward the destination in a straight line, at a 
# velocity determined at the time the send method is applied.  
# Of course the incrementing of the position is done in Card.draw(), 
# as controlled ultimately by the draw handler registered with 
# the simplegui frame.  When the object is within a certain 
# radius of its destination, the position becomes the destination, 
# and movement stops.
# 
# The other big idea I needed relates to sequencing of movements 
# and maintaining the logical state of the game, and the relations 
# between those two.  Some movements happen in parallel.  In the 
# opening animation (see scatter_and_regather(), below) all 52 cards 
# move simultaneously from random locations toward the deck.  Other 
# movements, such as dealing four cards one card at a time, have to 
# happen sequentially.  I used a scheme of callbacks and event handling.
# 
# There is an Event_handler object, and its method proc() contains 
# the main logic for the game and the animations.  proc() is called 
# when the user presses a button, and also when animation events 
# are completed.  It maintains a variable "state", by which it 
# knows whether it is dealing, waiting for the player to hit or stand, 
# waiting for the completion of an animation operation, etc.  Button 
# presses and completions of movements result in signals being sent 
# to proc().  When invoked, proc() performs operations and changes 
# the state according to the current state, the signal received, and 
# other conditions.
# 
# As an example, consider the cards in the two hands at the end of a 
# round of the game.  They have to be gathered up and restored to the 
# deck before dealing the next hand, and the animation should show that. 
# When the handler is in the state "ready" and the user has just 
# pressed the "Deal" button, proc() receives the signal "deal".  See 
# the code for proc(), below.  
# 
# In the redeck_cards() method, the cards are, one at a time, discarded 
# from the hands and immediately added back into the deck.  The 
# add_card() method of the deck sends each card to the position of 
# the deck.
# 
# proc() needs to get a signal when all the cards have arrived at the 
# deck.  and it creates a Callback_manager object for that purpose.  
# The code:
# 
# self.callback_mgr = Callback_manager(redecked_list, self.proc, "redecked")
# 
# places the name callback_mgr.callback into each card on redecked_list, 
# exactly the cards that have already been sent on their way from the 
# hands to the deck.  proc() changes its own state to "dealing", and 
# proc() finishes, until it gets its next signal.  Each time a card 
# arrives at the deck, its draw function calls callback_mgr.callback.  
# When the last card arrives at the deck, callback_mgr calls self.proc 
# with the signal "redecked".  Then the event handler shuffles, and 
# deals the first card in the state "dealing", under the signal "redecked".
# 
# #############################################
# Here are some points to remember in understanding the code. 
# 
# Executions of proc() are not interrupted, since it is called either: 
# 1) pursuant to handling a simplegui event, namely: (a) a press of one 
# of the four buttons, or (b) a call to the draw handler, or 2) before 
# the simplegui frame is created.
# 
# At a given time, at most one Callback_manager object has outstanding 
# callbacks.
# 
# proc() may be called recursively, but should not be so called when 
# a Callback_manager has outstanding callbacks, as that could unexpectedly
# overwrite that Callback_manager.
# 
# Unless there is a reset, each callback assigned to an object is 
# expected to execute, and each Callback_manager is expected to deliver
# exactly one signal to proc().



import math
import random
import simplegui

LOGO_STRING = "O'Blackjack"

# load card sprite - 936x384 - source: jfitz.com
# Assume card face and card back are the same size.
CARD_IMAGE_SIZE = (72, 96)
CARD_IMAGE_CENTER = (36, 48)
card_images = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
card_back = simplegui.load_image(
    "http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# Object magnifier
O_MAG = 2.0

# Canvas magnifier
C_MAG = 1.0

CARD_X = O_MAG*CARD_IMAGE_SIZE[0]   
CARD_Y = O_MAG*CARD_IMAGE_SIZE[1]

CARD_CENTER_X = O_MAG*CARD_IMAGE_CENTER[0]
CARD_CENTER_Y = O_MAG*CARD_IMAGE_CENTER[1]

CANVAS_X = C_MAG * 1000
CANVAS_Y = C_MAG * 600


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7',
         '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
          '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

DEAL_PROMPT_1 = 'Please press "Deal" to play a hand.'



class Card:    
    card_speed = 12.0
    
    def __init__(self, suit, rank, pos_x, pos_y):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            
            self.face_up = False
            
            self.pos_x = pos_x
            self.pos_y = pos_y
            
            # "dest" means destination, used in sending a card
            self.dest_x = self.pos_x
            self.dest_y = self.pos_y           
            
            self.vel_x = 0
            self.vel_y = 0
            
            self.callback = None
        else:
            print "Invalid card: ", suit, rank
            raise AssertionError

    def __str__(self):
        return self.suit + self.rank
    
    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
    
    def set_face_up(self, TorF):
        self.face_up = TorF
        return self
    
    def dist_to_dest(self):
        return math.sqrt(
            (self.pos_x - self.dest_x)**2 + 
            (self.pos_y - self.dest_y)**2)    
  
    def send(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y
        norm = self.dist_to_dest()
        if norm != 0:
            self.vel_x = C_MAG * Card.card_speed * (self.dest_x - self.pos_x) / norm
            self.vel_y = C_MAG * Card.card_speed * (self.dest_y - self.pos_y) / norm
        return self
        
    def move(self, new_pos_x, new_pos_y):
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.dest_x = self.pos_x
        self.dest_y = self.pos_y
        return self
        
    def is_still(self):
        return (self.pos_x == self.dest_x) and (self.pos_y == self.dest_y)
    
    def set_callback(self, f):
        self.callback = f
        return self

    # When a sent-moving object is within the snap radius of 
    # its destination, it is considered to have arrived.
    def snap_radius(self):
        return self.card_speed/1.5
    
    def draw(self, canvas):
        card_loc = (CARD_IMAGE_CENTER[0] + CARD_IMAGE_SIZE[0] * RANKS.index(self.rank), 
                    CARD_IMAGE_CENTER[1] + CARD_IMAGE_SIZE[1] * SUITS.index(self.suit))
        if self.face_up:
            canvas.draw_image(
                card_images, card_loc, CARD_IMAGE_SIZE, 
                [self.pos_x + CARD_CENTER_X, 
                 self.pos_y + CARD_CENTER_Y],
                (CARD_X, CARD_Y)
            )
        else:
            canvas.draw_image(
                card_back, CARD_IMAGE_CENTER, CARD_IMAGE_SIZE, 
                (self.pos_x + CARD_CENTER_X, 
                 self.pos_y + CARD_CENTER_Y),
                (CARD_X, CARD_Y)
            )
        if  self.dist_to_dest() < C_MAG * self.snap_radius():
        # when the card is approximately where it was sent or placed
            self.pos_x = self.dest_x
            self.pos_y = self.dest_y    
            if (self.vel_x != 0 or self.vel_y != 0):            
                self.vel_x = 0
                self.vel_y = 0
                cb = self.callback
                if cb != None:
                    self.callback = None
                    cb()
        else:
        # when the card has not arrived where it was sent
            self.pos_x += self.vel_x
            self.pos_y += self.vel_y

            

            
def draw_card_frame(canvas, pos_x, pos_y, width):
    border = O_MAG * 4
    canvas.draw_polygon(
        [(pos_x - border,	 		pos_y - border), 
         (pos_x + CARD_X + border, 	pos_y - border),
         (pos_x + CARD_X + border, 	pos_y + CARD_Y + border),
         (pos_x - border,	 		pos_y + CARD_Y + border)],
        width,
        "Black"
        )


class Hand:
    def __init__(self, pos_x, pos_y, grow_x, grow_y):
        self.cards = []
        self.pos_x = pos_x
        self.pos_y = pos_y
        # (grow_x, grow_y) provides for varying a regular layout of 
        #   the hand's cards on the canvas.
        self.grow_x = grow_x
        self.grow_y = grow_y
        self.score = 0
        
    def __str__(self):
        s = "Hand:"
        for c in self.cards:
            s += " " + str(c)
        return s    
        
    def add_card(self, card):  
        self.cards.append(card)
        card.send(            
            self.pos_x + self.grow_x * (len(self.cards)-1) * CARD_X, 
            self.pos_y + self.grow_y * (len(self.cards)-1) * CARD_Y)
     
    def get_value(self):
        # count aces as 1, if the hand has an ace, 
        # then add 10 to hand value if it doesn't bust
        val = 0
        has_ace = False
        for c in self.cards:
            rank = c.get_rank()
            if rank == 'A':
                has_ace = True
            val += VALUES[rank]
        val += 10 if (has_ace and val + 10 <= 21) else 0
        return val
    
    def is_busted(self):
        return self.get_value() > 21
 
    def is_empty(self):
        return len(self.cards) == 0
    
    def discard(self):
        if self.is_empty():
            print "attempted discard from empty deck"
            raise AssertionError
        else:
            return self.cards.pop(-1)

    def get_score(self):
        return self.score
    
    def set_score(self, new_score):
        self.score = new_score

    def draw(self, canvas):
        draw_card_frame(canvas, self.pos_x, self.pos_y, 1)
        canvas.draw_text(
            (" " if self.score >= 0 else "") +
            (" " if self.score < 10 else "") + str(self.score),
            (self.pos_x - 1.3 *CARD_X,
             self.pos_y + 0.65*CARD_Y),
            CARD_Y/2,
            "White"
            )
        for c in self.cards: 
            c.draw(canvas)

            
            
class Deck:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.cards = [Card(s,r, pos_x, pos_y) for s in SUITS for r in RANKS]
        for c in self.cards:
            c.send(self.pos_x, self.pos_y)
 
    def __str__(self):
        s = "Deck:"
        for c in self.cards:
            s += " " + str(c)
        return s

    def shuffle(self):
        for c in self.cards:
            c.set_face_up(False)
        random.shuffle(self.cards)
        # print "shuffled: ", self
        return self

    def is_empty(self):
        return len(self.cards) == 0
        
    def deal_card(self):
        if self.is_empty():
            print "attempted to deal from an empty deck."
            raise AssertionError
        else:    
            return self.cards.pop(-1)
    
    def add_card(self, card):
        self.cards.append(card)
        card.send(self.pos_x, self.pos_y)       
 
    def draw(self, canvas):
        draw_card_frame(canvas, self.pos_x, self.pos_y, O_MAG*4)
        canvas.draw_image(
            card_back, CARD_IMAGE_CENTER, CARD_IMAGE_SIZE, 
            (self.pos_x + CARD_CENTER_X, 
             self.pos_y + CARD_CENTER_Y),
            (CARD_X, CARD_Y))
        for c in self.cards:
            if not c.is_still():
                c.draw(canvas)    

          
 
class Callback_manager:
    # class attribute manager_count is 
    # used to ensure that there are no outstanding
    # callbacks when a new Callback_manager instance is created.
    manager_count = 0
    
    def __init__(self, callbacker_list, requester, signal):
        if self.__class__.manager_count > 0:
            print ("Only one Callback_manager is allowed at one time.\n" +
                   "Request was for function: " + str(requester) + 
                   "\nand signal: " + signal)
            raise AssertionError
        self.__class__.manager_count += 1        
        self.requester = requester
        self.signal = signal
        self.callback_count = len(callbacker_list)
        if self.callback_count != 0:    
            for cb_er in callbacker_list:
                cb_er.set_callback(self.callback)
        else:
            print "empty list passed when constructing " + str(self)
            raise AssertionError
  
    def __str__(self):
        return (" Callback_manager(" + 
                self.signal + ", " +
                str(self.callback_count) + ")")

    def reset(self):
        # Called only upon a reset of the event handler
        self.__class__.manager_count = 0
    
    def callback(self):
        self.callback_count -= 1
        if self.callback_count < 0:
            print "negative callback count: ", str(self)
            raise AssertionError
        elif self.callback_count == 0:
            self.__class__.manager_count -= 1
            self.requester(self.signal)

    def get_callback_count(self):
        return self.callback_count
    
    def get_signal(self):
        return self.signal

    
    
def scatter_and_send_back(deck):
    cards = []
    while not deck.is_empty():
        cards.append(deck.deal_card().set_face_up(True))
    for c in cards:
        deck.add_card(
            c.move(
                random.random() * (CANVAS_X - 1 - CARD_X), 
                random.random() * (CANVAS_Y - 1 - CARD_Y)))
    return cards    
                
    
        
class Event_handler:
    def __init__(self):
        self.callback_mgr = None
        self.state = None
        self.hand_count = None
        self.message_0 = None
        self.message_1 = None
                        
    def __str__(self):
        return ("Event_handler: " + self.state + 
                " " + str(self.callback_mgr) + 
                ", hand_count == " + str(self.hand_count) +
                ", message_0 ==" + self.message_0 + 
                ", message_1 ==" + self.message_1)

    # Reset button handler.
    # Called at startup and whenever the user presses the reset button.
    # Resets are processed unconditionally.
    def reset(self):
        player_hand.set_score(0)
        dealer_hand.set_score(0)
        self.hand_count = 0
        self.message_0 = "It's ..."
        self.message_1 = ""
        self.state = "initial"
        self.proc("reset")

    # Deal button handler.    
    # When cards are moving, any deal event is suspended until
    # cards have stopped moving.        
    def deal(self):
        if not self.state in ["initial", "ready", "deal_pending"]:
            self.update_score(-1, "Player folded.  Dealer won.")
        if self.callback_mgr.get_callback_count() > 0:
            self.change_state("deal_pending")
        else:    
            self.change_state("ready")
            self.proc("deal")

    # Hit button handler.        
    # When cards are moving, any Hit event is ignored.        
    def hit(self):
        if self.callback_mgr.get_callback_count() == 0:
            self.proc("hit")
        else:
            self.message_1 = "Hit ignored."

    # Stand button handler.
    # When cards are moving, any Stand event is ignored.
    def stand(self):
        if self.callback_mgr.get_callback_count() == 0:
            self.proc("stand")
        else:
            self.message_1 = "Stand ignored."
    
    def get_hand_count(self):
        return self.hand_count
   
    def redeck_cards(self):
        cards = []
        while not player_hand.is_empty():
            cards.append(player_hand.discard())
            deck.add_card(cards[-1])
        while not dealer_hand.is_empty():
            cards.append(dealer_hand.discard())
            deck.add_card(cards[-1])
        return cards
   
    def update_score(self, increm, msg):
        player_hand.score += increm
        dealer_hand.score -= increm
        self.hand_count += 1
        self.message_0 = "Deal " + str(self.hand_count) + ":  " + msg
 
    def change_state(self, new_state):
        # a good place for print statements when debugging
        self.state = new_state
    
    # for debugging
    def show_proc_info(self, msg, signal):
        print (s + " signal == " + signal + 
            "; state == " + self.state + 
            "; " + str(self.callback_mgr))
        
    def proc_fatal_error(self, signal):
        print "proc_fatal_error: " + str(self) + " received signal " + signal
        raise AssertionError
  
    def proc(self, signal):
        if self.state not in ["initial", "ready", "deal_pending",
                              "dealing", "players_move", "dealers_move"]:
            self.proc_fatal_error(
                "unexpected state: " + str(self) + " " + signal)
       
        # The following state is entered only 1) at startup, via self.reset(), 
        # and 2) via the handler for the "Reset" button.    print 
        if self.state == "initial":
            if signal == "reset":                
                self.redeck_cards()
                deck.shuffle()
                Card.card_speed /= 3.0
                cards = scatter_and_send_back(deck)
                Card.card_speed *= 3.0
                # It's safe to reset the callback manager because
                # all the cards are about to get new callbacks.
                if self.callback_mgr != None:
                    self.callback_mgr.reset()
                self.callback_mgr = Callback_manager(
                    cards, self.proc, "scattered_and_regathered")
            elif signal == "scattered_and_regathered":
                self.change_state("ready")
                # set_card_speed(2*get_card_speed())
                self.message_0 = "... O'Blackjack."
                self.message_1 = "        Deal?"

        # Entered 1) immediately after a reset (via the "initial" state),
        # or 2) after the user
        # presses the "Deal" button (directly if there were no outstanding
        # callbacks, or via the "deal_pending" state, after waiting for 
        # the callbacks to complete).    
        elif self.state == "ready":
            if (signal == "deal"): 
                self.message_1 = "Shuffle." 
                self.change_state("dealing")
                redecked_list = self.redeck_cards()
                if len(redecked_list) > 0:
                    self.callback_mgr = Callback_manager(
                        redecked_list, self.proc, "redecked")
                else:    
                    self.proc("redecked")    
            elif signal == "hit" or signal == "stand":
                self.message_1 = DEAL_PROMPT_1
            else:
                self.proc_fatal_error(signal)
            
        # Entered exactly when a deal is requested while 
        # there are outstanding callbacks.        
        elif self.state == "deal_pending":
            if signal == self.callback_mgr.get_signal():
                self.change_state("ready")
                self.proc("deal")
                
        elif self.state == "dealing":
            if (signal == "redecked"):
                deck.shuffle()
                self.message_0 = ""
                self.message_1 = "Dealing."                
                card = deck.deal_card().set_face_up(True)
                player_hand.add_card(card)
                self.callback_mgr = Callback_manager(
                    [card], self.proc, "dealt_first_card_to_player")
            elif (signal == "dealt_first_card_to_player"):
                card = deck.deal_card().set_face_up(False)
                dealer_hand.add_card(card)
                self.callback_mgr = Callback_manager(
                    [card], self.proc, "dealt_first_card_to_dealer")
            elif (signal == "dealt_first_card_to_dealer"):
                card = deck.deal_card().set_face_up(True)
                player_hand.add_card(card)
                self.callback_mgr = Callback_manager(
                    [card], self.proc, "dealt_second_card_to_player")
            elif (signal == "dealt_second_card_to_player"):
                card = deck.deal_card().set_face_up(True)
                dealer_hand.add_card(card)
                self.callback_mgr = Callback_manager(
                    [card], self.proc, "dealt_second_card_to_dealer")
            elif (signal == "dealt_second_card_to_dealer"):
                self.change_state("players_move")
                self.message_1 = "Hit or Stand?"
            elif signal in ["hit", "stand"]:
                pass
            else:
                self.proc_fatal_error(signal)
                
        elif self.state == "players_move":                
            if (signal == "hit"):
                card = deck.deal_card().set_face_up(True)
                player_hand.add_card(card)
                self.callback_mgr = Callback_manager(
                                    [card], 
                                    self.proc, 
                                    "player_was_hit")
            elif (signal == "player_was_hit"):    
                if player_hand.is_busted():
                    dealer_hand.cards[0].set_face_up(True)
                    self.update_score(-1, "Player busted.  Dealer won.")
                    self.change_state("ready")
                    self.message_1 = "Deal again?"
                else:
                    self.message_1 = "Hit or Stand?"
            elif signal == "stand":
                dealer_hand.cards[0].set_face_up(True)
                self.change_state("dealers_move")
                self.message_1 = "Dealer's turn."
                self.proc("decisions")
            else:
                self.proc_fatal_error(signal)
                
        elif self.state == "dealers_move":
            if signal == "decisions":                
                if dealer_hand.get_value() < 17:
                    card = deck.deal_card().set_face_up(True)
                    dealer_hand.add_card(card)
                    self.callback_mgr = Callback_manager(
                        [card], self.proc, "decisions")                    
                elif dealer_hand.is_busted():
                    self.update_score(+1, "Dealer busted.  Player won.")
                    self.message_1 = "Deal again?"
                    self.change_state("ready")
                elif player_hand.get_value() > dealer_hand.get_value():
                    self.update_score(+1, (
                        "Player: " + str(player_hand.get_value()) +
                        ",  Dealer: " + str(dealer_hand.get_value()) +
                        ".  Player won."
                        ))
                    self.change_state("ready")
                    self.message_1 = "Deal again?"
                else:
                    self.update_score(-1, 
                        ("Player: " + str(player_hand.get_value()) + 
                         ",  Dealer: " + str(dealer_hand.get_value()) + 
                         ".  Dealer won."))
                    self.change_state("ready")
                    self.message_1 = "Deal again?"
            elif signal in ["hit", "stand"]:
                pass
            else:
                self.proc_fatal_error(signal)
        else:
            pass
        
        
    def draw(self, canvas):
        canvas.draw_text(
            LOGO_STRING, 
            (0.10*CANVAS_X + CARD_X, 
             CANVAS_Y/2 + 0.36*logo_font_size),
            logo_font_size, "Gray", "sans-serif")
        canvas.draw_text(
            self.message_0, 
            (0.05*CANVAS_X + 3.5*CARD_X, 0.92*CANVAS_Y),
            message_font_size, "White")
        canvas.draw_text(
            self.message_1,
            (0.05*CANVAS_X + 3.5*CARD_X, 0.97*CANVAS_Y),
            message_font_size, "White")
        player_hand.draw(canvas)
        dealer_hand.draw(canvas)
        deck.draw(canvas)

                                   

# find the font size that brings a given string to a given width, in pixels        
def font_size(frame, s, width, type_face):
    f_size = 2
    while True:
        if type_face == None:
            w = frame.get_canvas_textwidth(s, f_size)
        else:    
            w = frame.get_canvas_textwidth(s, f_size, type_face)
        if w >= width:
            break
        else:
            f_size += 1
    return f_size       
    

    
deck = Deck(0.05*CANVAS_X, CANVAS_Y/2 - CARD_Y/2)
dealer_hand = Hand(
    0.05*CANVAS_X + 1.5*CARD_X, 0.05*CANVAS_Y,  		0.75,  0.10)
player_hand = Hand(
    0.05*CANVAS_X + 1.5*CARD_X, 0.95*CANVAS_Y - CARD_Y,	0.75, -0.10) 

event_handler = Event_handler()
event_handler.reset()


# initialization of frame
frame = simplegui.create_frame("Blackjack", CANVAS_X, CANVAS_Y)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Reset", event_handler.reset, 50)
frame.add_button("Deal", event_handler.deal, 200)
frame.add_button("Hit",  event_handler.hit, 200)
frame.add_button("Stand", event_handler.stand, 200)

frame.set_draw_handler(event_handler.draw)

logo_font_size = font_size(
    frame,
    LOGO_STRING, 
    CANVAS_X - 0.15*CANVAS_X - CARD_X,
    "sans-serif"
)    

message_font_size = font_size(
    frame,
    "Deal xx:  Player: xx,  Dealer xx: Player wins.", 
    0.90*CANVAS_X - 3.5*CARD_X, None)


# get things rolling
frame.start()


#Blackjack is a simple, popular card game that is played in many casinos. 
#Cards in Blackjack have the following values: an ace may be valued as 
#either 1 or 11 (player's choice), face cards (kings, queens and jacks) 
#are valued at 10 and the value of the remaining cards corresponds to their 
#number. During a round of Blackjack, the players plays against a dealer 
#with the goal of building a hand (a collection of cards) whose cards have 
#a total value that is higher than the value of the dealer's hand, but not 
#over 21.  (A round of Blackjack is also sometimes referred to as a hand.)
#
#The game logic for our simplified version of Blackjack is as follows. The 
#player and the dealer are each dealt two cards initially with one of the 
#dealer's cards being dealt faced down (his hole card). The player may then 
#ask for the dealer to repeatedly "hit" his hand by dealing him another card. 
#If, at any point, the value of the player's hand exceeds 21, the player is 
#"busted" and loses immediately. At any point prior to busting, the player 
#may "stand" and the dealer will then hit his hand until the value of his 
#hand is 17 or more. (For the dealer, aces count as 11 unless it causes the 
#dealer's hand to bust). If the dealer busts, the player wins. Otherwise, 
#the player and dealer then compare the values of their hands and the hand 
#with the higher value wins. The dealer wins ties in our version.

#Grading rubric - 18 pts total (scaled to 100)
#You must implement the simplified rules of Blackjack specified in this description. Small variations from our demo version are acceptable such as displaying the value of a hand or implementing a betting system. But, you may not change the logic of the game. After the submission deadline, you are welcome to post enhanced versions of Blackjack to the Hall of Fame with more realistic game logic such as pushes on ties, splitting pairs and doubling down.
#
#    1 pt - The program displays the title "Blackjack" on the canvas.
#    1 pt - The program displays 3 buttons ("Deal", "Hit" and "Stand") in the control area.
#    2 pts - The program graphically displays the player's hand using card images. (1 pt if text is displayed in the console instead)
#    2 pts - The program graphically displays the dealer's hand using card images. Displaying both of the dealer's cards face up is allowable when evaluating this bullet. (1 pt if text displayed in the console instead)
#    1 pt - The dealer's hole card is hidden until the current round is over. After the round is over, it is displayed.
#    2 pts - Pressing the "Deal" button deals out two cards each to the player and dealer. (1 pt per player)
#    1 pt - Pressing the "Deal" button in the middle of the round causes the player to lose the current round.
#    1 pt - Pressing the "Hit" button deals another card to the player.
#    1 pt - Pressing the "Stand" button deals cards to the dealer as necessary.
#    1 pt - The program correctly recognizes the player busting.
#    1 pt - The program correctly recognizes the dealer busting.
#    1 pt - The program correctly computes hand values and declares a winner. Evaluate based on messages.
#    2 pts - The program accurately prompts the player for an action with messages similar to "Hit or stand?" and "New deal?". (1 pt per message)
#    1 pt - The program implements a scoring system that correctly reflects wins and losses. Please be generous in evaluating this item.
