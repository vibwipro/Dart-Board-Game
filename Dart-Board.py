# Copyright (c) 2011 Vibhor Gupta
# A Dart-Board Game
# This work is available under the "MIT License". Please see the
# file COPYING in this distribution for license details.

import random
import shelve
from sys import exit

# Initialize the PRNG
random.seed()

# The scorefile is kept as a dictionary mapping
# username to score, stored in a "shelf".
user_scores = shelve.open("Dart")

def register(username):
    "Register a new, legal username."
    for c in username:
        if not (c.isalpha() or c.isdigit() or c in "_-"):
            print("illegal character in username " + \
                  "(legal are A-Za-z0-9_-)")
            return
    if username in user_scores:
        print("username already registered")
        return
    user_scores[username] = 0
    user_scores.sync()

# The username of the current darter
darter = None

def dart(username):
    "Set the darter to an existing username."
    global darter
    if not (username in user_scores):
        print("username unknown")
        return
    darter = username

def darter_score():
    global darter
    print("Your current score is " + str(user_scores[darter]))

# Dictionary of dartes keyed by dart and contents
# a two-tuple indicating the percent probability and
# the score of that dart.
dartes = (
    (None, 20, 0),
    ("Red", 20, 10),
    ("Blue", 30, 30),
    ("Yello", 15, 100),
    ("Green", 10, 200),
    ("White", 4, 500),
    ("Black", 1, 5000) )

def throw_result():
    """
    Get the result of a throw. Returns a tuple of dart
    description and throw score.
    """
    hit = random.randrange(100)
    for (dart, percent, score) in dartes:
        hit -= percent
        if hit < 0:
            return (dart, score)
    assert False

def dart_name(dart):
    "Return canonical name of a dart."
    if dart == None:
        return "nothing"
    return "a " + dart

def throw():
    "throw the darter's rod."
    global darter
    if darter == None:
        print('Use the "dart" command to choose a darter.')
        return
    (dart, score) = throw_result()
    print("You have Oche ", end="")
    if dart == None:
        print(dart_name(dart) + ".")
        return
    print("on " + dart_name(dart) + "!")
    print("It is worth " + str(score) + " points.")
    user_scores[darter] += score
    user_scores.sync()
    darter_score()

def scores():
    "Show everyone's score."
    global darter
    if darter != None:
        darter_score()
        print("")
    print("All scores:")
    for u in user_scores:
        print(u + ": " + str(user_scores[u]))

def quit():
    "Quit the game."
    scores()
    user_scores.close()
    exit()

def help():
    "Show help."
    print("""
    Key-Word            : Description of Key-Word
    ---------------------------------------------------------
    register <username> : Register a new darter named username
    dart <username>     : Start username darting
    throw               : Try to hit a dart board
    scores              : Find out everyone's score
    quit                : Quit the game
    point               : Points on Dart Board
    help                : This help
    """)

def point():
    "Point the darting algorithm."
    counts = {}
    for (dart, _, _) in dartes:
        counts[dart] = 0
    for i in range(10000):
        (dart, _) = throw_result()
        counts[dart] += 1
    print ("Colour" +'\t' +  ": " + "Points")
    print ("----------------")
    for dart in counts:
        print(dart_name(dart) + '\t' + ": " + str(counts[dart]))

# darting commands. Each command comes with its argument
# count and its function.
commands = { "register" : (1, register),
             "dart" : (1, dart),
             "throw" : (0, throw),
             "scores" : (0, scores),
             "quit" : (0, quit),
             "help" : (0, help),
             "point" : (0, point) }

# The main loop
print('1- darting! Please enter darting commands. "help" for help.')
while True:
    words = []
    while words == []:
        try:
            cmd = input("> ")
        except EOFError:
            print("quit")
            cmd = "quit"
        words = cmd.split()
    if words[0] in commands:
        (nargs, cmd_fun) = commands[words[0]]
        if len(words) - 1 != nargs:
            print("Wrong number of arguments to command. Please try again")
            continue
        if nargs == 0:
            cmd_fun()
        elif nargs == 1:
            cmd_fun(words[1])
        else:
            assert False
        continue
    print("2- Unknown darting command. Please try again.")