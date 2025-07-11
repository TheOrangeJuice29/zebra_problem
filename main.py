import main_func


def main():

    initial_state = main_func.known_constraints.copy() #intitializes the root state with the already known constraits
    root = main_func.TreeNode(state = initial_state)

    best_state = main_func.run_mcts(root, iterations=20, llm_func=main_func.cached_llm_call) #MCTS with caching

    print("\nFinal deduced state:") #prints the final deduced state after the MCTS search
    for fact in best_state:
        print(f"- {fact}")


    solution = main_func.simulate_full_solution(best_state) #the solution to the two questions found

    print("\Final solution:")
    print(solution)


if __name__ == "__main__":
    main()