__author__ = 'torsten'

secret = 38


def median(numbers):
    a = numbers
    print a.sort()

print median([1, 1, 2, 2, 3, 4, 4, 3, 1])

def report_status(guess):
    ''' (number) -> str

    Return the result (You got it, to high, to low)
    for a guess that matches the secret or not.
    Pre-condition: guess within range

    >>> report_status(0)
    "to low"
    >>> report_status(100)
    "to high"
    >>> report_status(50)
    "match"
   '''

    global secret

    if guess == secret:
       return ("match!")
    elif secret < guess:
       return ("lower!")
    else:
       return ("higher!")



print report_status(24)
print report_status(40)
print report_status(38)





