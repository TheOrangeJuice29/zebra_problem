known_constraints = ["There are five houses.",
"The Englishman lives in the red house.",
"The Spaniard owns the dog.",
"The person in the green house drinks coffee.",
"The Ukrainian drinks tea.",
"The green house is immediately to the right of the ivory house.",
"The snail owner likes to go dancing.",
"The person in the yellow house is a painter.",
"The person in the middle house drinks milk.",
"The Norwegian lives in the first house.",
"The person who enjoys reading lives in the house next to the person with the fox.",
"The painter's house is next to the house with the horse.",
"The person who plays football drinks orange juice.",
"The Japanese person plays chess.",
"The Norwegian lives next to the blue house."]

state = [
    "The Englishman lives in the red house.",
    "The Norwegian lives in the first house.",
    "The Ukrainian drinks tea."
]

def count_constraints(state):
    pass

def evaluate_zebra_state(state):
    """Take a list of natural langauage facts that are strings
        and returns how many of those match the constraints"""

    score = 0

    for constraint in known_constraints:
        if constraint in state:
            score += 1
        else:
            continue
    return score