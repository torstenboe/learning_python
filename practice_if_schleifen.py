__author__ = 'torsten'

def report_status(scheduled_time, estimated_time):
    ''' (number, number) -> str

    Return the flight status (on time, early, delayed)
    for a flight that was scheduled to arrive at
    scheduled time, but now estimated to arrive
    at estimated time

    Pre-condition: 0.0 <= scheduled time < 24 and
    0.0 <= estimated_time < 24

    >>> report_status(14.3, 14.3)
    /"on time/"
    >>> report_status(12.5, 11.5)
    /"early/"
    >>> report_status(9.0, 9.5)
    /"delayed/"
   '''
    if scheduled_time == estimated_time:
        return 'on time'
    elif scheduled_time < estimated_time:
        return 'early'
    else:
        return 'delayed'

print (report_status(14.3, 14.3))
print (report_status(12.5, 11.5))
print (report_status(9.0, 9.5))

print "=== short if using boolean logic ==="

def is_even(num):
    ''' (int) -> bool

    Return whether num is even

    >>> is_even(4)
    True
    >>> is_even(77)
    False '''

    if num % 2 == 0:
       return True
    else:
       return False

print is_even(4)
print is_even(3)

def is_even_short(num):

    return num % 2 == 0

print is_even_short(4)
print is_even_short(3)

print "=== avoid nested if ==="

precipitation = False
temperature = 8

def clothes_nested():
    if precipitation:
        if temperature > 0:
            return ("Bring your umbrella!")
        else:
            return ("Wear your boots and winter coat!")

print clothes_nested()
print "=== not nested ==="

def clothes():
    if precipitation and temperature > 0:
        return ("Bring your umbrella!")
    elif precipitation:
        return ("Wear your boots and winter coat!")
    else:
        return ("Sunshine!")
print clothes()


print "=== isBetween ==="

secret = 38

def isBetween(guess, upper_limit, lower_limit):
    '''Return Direction if guess is between the ends and not equal to secret.
    The ends do not need to be in increasing order.'''

    global secret

    if guess == secret:
        return ("you got it!")
    elif secret < guess < upper_limit:
        return ("to high!")
    elif lower_limit < guess < secret:
        return ("to low!")
    else:
        return ("Really? Try again !")

print isBetween(24,100,0)
print isBetween(40,100,0)
print isBetween(38,100,0)
