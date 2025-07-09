import main_func



#scores = main_func.evaluate_zebra_state(sample_state)
#print(scores)
#print("Hello")


test_state = [
    "The Englishman lives in the red house.",
    "The Norwegian lives in the first house.",
    "The Ukrainian drinks tea."
]




scores = main_func.evaluate_zebra_state(test_state)
print(scores)


root = main_func.TreeNode(state = test_state)
root.visits = 100


child_a = main_func.TreeNode(state = test_state + ["The person in the middle house drinks milk."], parent = root)
child_a.visits = 50
child_a.value = 33.

child_b = main_func.TreeNode(state = test_state + ["The Spaniard owns the dog."], parent = root)
child_b.visits = 10
child_b.value = 8

child_c = main_func.TreeNode(state=test_state + ["The Japanese person plays chess."], parent=root)
child_c.visits = 0
child_c.value = 0.0

root.children = [child_a, child_b, child_c]

selected = main_func.select_best_child(root)
print("Selected child: ")

for character in selected.state:
    print(character)