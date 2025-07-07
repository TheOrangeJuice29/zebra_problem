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