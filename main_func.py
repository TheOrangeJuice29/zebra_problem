import math
exploration_const = math.sqrt(2)
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


def evaluate_zebra_state(state):
    """Take a list of natural langauage facts that are strings
        and returns how many of those match the constraints"""

    score = 0

    for constraint in known_constraints: #iterates through known constraints
        if constraint in state: #check if the constraint in in the state_list
            score += 1
        else:
            continue
    return score


class TreeNode: #this creates node used in the MCTS.
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent #link to the parent node
        self.children = [] #list of children
        self.visits = 0 #visit count of i
        self.value = 0 #total reward from those simulations

    def uct_score(self, parent_visits, exploration_const):
        if self.visits == 0:
            return float('inf') #this prioritizes the simulation on unexplored nodes

        average_reward = self.value / self.visits
        exploitation = exploration_const * math.sqrt((math.log(parent_visits))/self.visits)
        uct_value = average_reward + exploitation
        return uct_value


def select_best_child(node): #function to choos the the best child node 
    parent_visits = node #vists to the parent node
    key = lambda child: child.uct_score(parent_visits, exploration_const) #lambda function for getting the uct score
    return max(node.children, key)

def tree_policy(root):
    node = root
    while node.children: #goes through the children, picking the best one
        node = select_best_child(node)
    return node

