import math
import openai
import logging


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
    parent_visits = node.visits #vists to the parent node
    return max(node.children, key = lambda child: child.uct_score(parent_visits, exploration_const)) #lambda function for getting the uct score

def tree_policy(root):
    node = root
    while node.children: #goes through the children, picking the best one
        node = select_best_child(node)
    return node


openai.api_key = "sk-proj-Gs9DbSOuwieZWV9nP_" \
                "qTJIvlmrt02m68R0C8S3jSYI1zGrmuk5XTmek67-8By4GfOG2y-_" \
                "dg9QT3BlbkFJzzKBKg73kFfudXJ8xyWPH7SZAO42w7VpjQ-jsn9So3rW-" \
                "5NgQPfttS8AiLkTSTzmOtpfrDhlcA"


def llm_call(state):
    formatted_state = "\n".join(f"-{statement}" for statement in state)

    prompt = f"""
    You are solving the Zebra Puzzle. The current known facts are:

    {formatted_state}

    What is one new logical deduction you can make based on this state?
    Respond with a single fact in natural language (e.g., "The Spaniard owns the dog.") without explanation.
    """

    gpt_response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = [
            {"role": "system", "content": "You are an expert logic reasoner."},
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7, #more random
        max_tokens = 50
        )
    

    new_fact = gpt_response["choices"][0]["message"]["content"].strip()
    return new_fact


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
    new_fact = llm_func(node.state)

    if new_fact in node.state:
        return None
    
    new_state = node.state.copy()
    new_state.append(new_fact)

    child = TreeNode(state = new_state, parent = node)
    node.children.append(child)
    return child


def simulate_full_solution(state):
    formatted_state = "\n".join(f"-{statement}" for statement in state)
    
    prompt = f"""These are the current facts:
    
    {formatted_state}
    """

    gpt_response = openai.ChatCompletion.create(
    model = "gpt-4",
    messages = [
        {"role": "system", "content": "You are an expert logic reasoner."},
        {"role": "user", "content": prompt}
    ],
    temperature = 0.2, #less random
    max_tokens = 500
    )

    try:
        full_solution = gpt_response["choices"][0]["message"]["content"].strip()
        return full_solution
    except Exception:
        logging.info("Parsing was unsuccessful")
        return None