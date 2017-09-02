# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    #pass

    # convert name to number using if/elif/else
    # don't forget to return the result!
    names_n_numbers = {'rock':0,
                       'Spock':1,
                       'paper':2,
                       'lizard':3,
                       'scissors':4
                       }
    if name in names_n_numbers:
        return names_n_numbers[name]
    else:
        print name, """is an invalid input for name_to_number.
please use string: rock, Spock, paper, lizard, scissors
"""

def number_to_name(number):
    # delete the following pass statement and fill in your code below
    #pass
    
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    numbers_n_names = {0:'rock',
                       1:'Spock',
                       2:'paper',
                       3:'lizard',
                       4:'scissors'
                       }
    if number in numbers_n_names:
        return numbers_n_names[number]
    else:
        print number, """is an invalid input for number_to_name.
please use integer: 1-5
"""

def rpsls(player_choice): 

    # print a blank line to separate consecutive games
    print ''
    # print out the message for the player's choice
    print 'Player chooses', player_choice
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(5)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print 'Computer chooses', comp_choice
    # compute difference of comp_number and player_number modulo five
    if type(player_number) == int:
        difference_mod_5 = (comp_number - player_number)%5
        # use if/elif/else to determine winner, print winner message
        ####"Player and computer tie!", "Player wins!" or "Computer wins!"
        if difference_mod_5 == 0:
            print "Player and computer tie!"
        elif difference_mod_5 == 3 or difference_mod_5 == 4:
            print "Player wins!"
#        elif: difference_mod_5 == 1 or difference_mod_5 == 2:
#            print "Computer wins!"
        else:
            print "Computer wins!"
    else:
        print "Invalid player choice, no result"


# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


