import main_func



initial_state = main_func.known_constraints.copy()
root = main_func.TreeNode(state = initial_state)

best_state = main_func.run_mcts(root, iterations=20, llm_func=main_func.cached_llm_call)

print("\nFinal deduced state:")
for fact in best_state:
    print(f"- {fact}")

solution = main_func.simulate_full_solution(best_state)
print("\nFull solution:")
print(solution)


