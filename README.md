# zebra_problem
This project implements a Monte Carlo Tree Search (MCTS) algorithm enchanced with a Large Language Model (LLM)
reasoner to solve the calssic Zebra puzzle. Primary goal is to find out:

Who drinks water?
Who owns the Zebra?

The MCTS first builds a search tree by selecting the most promising nodes using the Upper Confidence Bound (UCB) score.
Expands on new fact by calling to an LLM to deduce logically consistent based on current known constraints. Propagates 
rewards based on how many constraints are satisfied and whether the key facts were deduced. Early stops if both target 
facts are found.

The LLM integration uses very carefulyl made prompt to guid the LLM, Gemini API, to deduce one new fact per state, and
caches LLM responses to avoid redundant calls and reduce computation time.

Starts with the 15 constraints. It then selects a promising node using UCT, deduces a new fact using the LLM, and adds the new state
as a child node.
There is reward evaluation as well, rewarding based on how many known constraints they satisfy, and there is extra reward if the key facts are deduced.

In order to run, we need to install dependencies in the terminal with installing google-generativeai. The solver is run via python main.py, and you'll have to
obtain a Gemini API key and creating a cloud project.

After running it, it will print a final deduced state, and the final solution like: "The Ukrainian drinks water, and the Spaniard owns the zebra."

Dependencies include:
google-generativeai
math
hashlib
jason
os
time
logging