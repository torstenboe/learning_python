__author__ = 'torsten'

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
player = ""
dealer = ""
card_deck = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
BUSTED = "You have busted!"

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            outcome = "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        ans = "Hand contains "
        for i in range(len(self.hand)):
            ans += " " + str(self.hand[i])
        return ans

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # compute the value of the hand, count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = sum(VALUES.get(x.get_rank()) for x in self.hand)
        for x in self.hand:
            if 'A' == x.get_rank() and value <= 11:
                value = value + 10
        return value

    def draw(self, canvas, loc):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand)):
            card = Card(self.hand[i].suit, self.hand[i].rank)
            width = CARD_SIZE[0]
            card_location = [loc[0]  + i * width, loc[1]]
            card.draw(canvas, card_location)
    
# define deck class
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS if suit != rank]

    def shuffle(self):
        # shuffle the deck
        return random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return random.choice(self.deck)

    def __str__(self):
        # return a string representing the deck
        return ("Deck contains  ".join([str(card) for card in self.deck]))



#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, card_deck, outcome, score

    if in_play == False:
        card_deck = Deck()
        card_deck.shuffle()
        
        player = Hand()
        player.add_card(card_deck.deal_card())
        player.add_card(card_deck.deal_card())
        
        dealer = Hand()
        dealer.add_card(card_deck.deal_card())
        dealer.add_card(card_deck.deal_card())
        
        outcome = "Hit or stand?"
        in_play = True
    else:
        outcome = "Not allowed - you loose"
        score += 1
        in_play = True
        

def hit():
    global in_play, player, dealer, score, outcome
    if in_play == True:
        player.add_card(card_deck.deal_card())
        if player.get_value() > 21:
            outcome =  BUSTED   
            in_play = False
            score += 1
    else:
        outcome =  "Game has ended, please hit deal button to play again"

def stand():
    global in_play, player, dealer, score, outcome     
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while dealer.get_value() < 17:
            dealer.add_card(card_deck.deal_card())
    # assign a message to outcome, update in_play and score
        if dealer.get_value() > 21:
            score -= 1
            outcome =  "Dealer has busted - You win!"
        elif dealer.get_value() >= player.get_value():
            score += 1
            outcome =  str(dealer.get_value()) + " - You Loose!"
        else:
            score -= 1
            outcome =  str(dealer.get_value()) + " - You Win!"
        in_play = False
    else:
        outcome =  "Game has ended, please hit deal button to play again"

# draw handler
def draw(canvas):
    global in_play, outcome, score
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", (2 , 30) , 24, 'Lime')
    canvas.draw_text(outcome, (CARD_SIZE[0] * 5, 30), 24, 'Yellow')
    canvas.draw_text(str(score), (CARD_SIZE[0] * 9, 30), 24, 'White')
    Hand.draw(player, canvas, [2, 42])
    Hand.draw(dealer, canvas, [(CARD_SIZE[0] * 5) + 2, 42])
    if in_play == True:
        canvas.draw_image(card_back, (CARD_BACK_CENTER[0] * 3, CARD_BACK_CENTER[1]), CARD_BACK_SIZE, ((CARD_BACK_SIZE[0] * 5 + CARD_BACK_CENTER[0] + 2), CARD_SIZE[1] - 6), CARD_BACK_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", (CARD_SIZE[0] * 10) + 4, CARD_SIZE[1] + 4 + 2 * 40)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()