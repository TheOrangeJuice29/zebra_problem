import math
import logging
from gemini_api import model
import time


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

    if any("drinks water" in fact for fact in state):
        score += 10

    if any("owns the zebra" in fact for fact in state):
        score += 10

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
    parent_visits = node.visits #vists to the parent node
    return max(node.children, key = lambda child: child.uct_score(parent_visits, exploration_const)) #lambda function for getting the uct score

def tree_policy(root):
    node = root
    while node.children: #goes through the children, picking the best one
        node = select_best_child(node)
    return node






def llm_call(state):
    formatted_state = "\n".join(f"- {statement}" for statement in state)

    #this is the prompt instructing the model to generate a solution
    prompt = f"""You are solving the Zebra Puzzle. The current known facts are:

    {formatted_state}

    Based only on these facts, deduce one new logically valid fact.
    Prioritize figuring out:
    - Who drinks water
    - Who owns the zebra

    If no deduction is possible yet, infer any fact logically implied by the current state.

    Respond with a single new fact in natural language, no explanation.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

llm_cache = {}

def cached_llm_call(state):
    state_key = tuple(sorted(state))
    if state_key in llm_cache:
        return llm_cache[state_key]
    
    result = llm_call(state)
    llm_cache[state_key] = result
    return result


def mock_llm_reasoner(state):
    """Dummy function for testing — replace with actual LLM later."""
    all_possible_facts = [
        "The Englishman lives in the red house.",
        "The Spaniard owns the dog.",
        "The person in the green house drinks coffee.",
        "The Ukrainian drinks tea.",
        "The person in the middle house drinks milk.",
        "The Norwegian lives in the first house.",
        "The Japanese person plays chess.",
        # Add more if needed
    ]
    # Return a new fact not already in state
    for fact in all_possible_facts:
        if fact not in state:
            return fact
    return None  # no new facts left

def expand_node(node, llm_func):
    time.sleep(5)
    new_fact = llm_func(node.state)

    if new_fact in node.state:
        return None
    
    new_state = node.state.copy()
    new_state.append(new_fact)

    child = TreeNode(state = new_state, parent = node)
    node.children.append(child)
    return child


def simulate_full_solution(state):
    formatted_state = "\n".join(f"- {statement}" for statement in state)
    
    #this is the prompt instructing the model to generate a solution
    prompt = f"""These are the current facts:
    
    {formatted_state}
    
    Based on this, complete the full assignment of all five houses.
    List each house with its color, nationality, drink, smoke, and pet.

    Format it exactly as a Python-style list of 5 dictionaries. For example:
    [
    {{"color": "red", "nationality": "Englishman", "drink": "milk", "smoke": "Pall Mall", "pet": "dog"}},
    ...
    ]

    Make sure your answer is logically consistent with the facts.
    """

    response = model.generate_content(prompt)

    try:
        full_solution = response.text.strip()
        return full_solution
    except Exception:
        logging.info("Parsing was unsuccessful")
        return None

def back_prop(node, reward):
    while node:
        node.visits += 1
        node.value += reward
        node = node.parent

def best_final_state(root):
    best_state = max(root.children, key = lambda c: 
                     c.value / c.visits if c.visits 
                     else 0, 
                     default = None)
    
    return best_state.state if best_state else root.state

def run_mcts(root, iterations, llm_func):
    for iter in range(iterations):
        leaf = tree_policy(root)
        child = expand_node(leaf, llm_func)

        if child is None:
            continue

        reward = evaluate_zebra_state(child.state)
        back_prop(child, reward)

        if any("drinks water" in fact for fact in child.state) and any("owns the zebra" in fact for fact in child.state):
            print(f"Early stopping at iteration {iter}")
            return child.state

    return best_final_state(root)