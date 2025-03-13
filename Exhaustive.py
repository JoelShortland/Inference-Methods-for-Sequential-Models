import itertools

# This is the function you need to implement
def exhaustive(tokens, distributions, transitions, labels):
    # First we need to consider each possible label pair for each token
    # So here, LOC LOC LOC, to O O O because 3 tokens.
    best_probability = 0
    best_sequence = []
    for label_combo in itertools.product(labels, repeat=len(tokens)):
        probability = 1
        #First get the probability of each token lining up with its thingo
        for i in range(len(tokens)):
            probability *= distributions[i].get(label_combo[i])


        #Then,
        my_transitions = [("START", label_combo[0])]
        for i in range(len(tokens)-1):
            my_transitions.append((label_combo[i], label_combo[i+1]))
        my_transitions.append((label_combo[len(label_combo)-1], "END"))

        for transition in my_transitions:
            probability *= transitions.get(transition)


        #print(label_combo)
        #print(my_transitions)
        #print(probability)
        if probability > best_probability:
            best_probability = probability
            best_sequence = label_combo

    return best_probability, best_sequence

# Sample data test
tokens = ["Sydney", "is", "nice"]
distributions = [
    {"LOC": 0.9, "O": 0.1},
    {"LOC": 0.05, "O": 0.95},
    {"LOC": 0.05, "O": 0.95},
]
transitions = {
    ("START", "O"): 0.8,
    ("START", "LOC"): 0.2,
    ("START", "END"): 0.0,
    ("O", "END"): 0.05,
    ("O", "O"): 0.9,
    ("O", "LOC"): 0.05,
    ("LOC", "END"): 0.05,
    ("LOC", "O"): 0.8,
    ("LOC", "LOC"): 0.2,
}
labels = {"LOC", "O"}

answer = exhaustive(tokens, distributions, transitions, labels)
if answer[0] != 0.0058482000000000004:
    print("Error in score")
    print("Score was:" + str(answer[0]))
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")
