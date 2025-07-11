import main_func



initial_state = []
root = main_func.TreeNode(state=[])
best_state = main_func.run_mcts(root, iterations=20, llm_func=main_func.llm_call)  # try 50–75
print("\nFinal deduced state:")
for fact in best_state:
    print(f"- {fact}")

solution = main_func.simulate_full_solution(best_state)
print("\nFull solution:")
print(solution)
