def my_sort(x):
    return x[0], ' '.join(x[1])

# This is the function you need to implement
def beam(tokens, distributions, transitions, labels, k):
    if k == 0:
        return None, None

    best_vals = []
    for i in range(len(tokens)):
        for label in labels:
            #Treat first instance seperately
            if i == 0:
                probability = transitions.get(("START", label))
                probability *= distributions[i].get(label)
                best_vals.append((probability, [label]))

            for start in best_vals:
                if len(start[1]) != i: #Sanity check to avoid inf recursion
                    pass
                else:
                    probability = start[0]           
                    probability *= transitions.get((start[1][-1], label))
                    probability *= distributions[i].get(label)
                    rtn = start[1].copy()
                    rtn.append(label) 
                    best_vals.append((probability, rtn))

        #Remove extra entries    
        num = 1
        for e in best_vals:
            if len(e[1]) > num:
                num = len(e[1])
        temp = []
        for val in best_vals:
            if len(val[1]) == num:
                temp.append(val)
        best_vals = temp

        best_vals = sorted(best_vals, key=my_sort, reverse=True)
        
        if len(best_vals) > k:
            best_vals = best_vals[0:k]

    return_vals = []
    for val in best_vals:
        return_vals.append((val[0] * transitions.get((val[1][-1], "END")), val[1]))
    return_vals = sorted(return_vals, key=my_sort, reverse=True)
    return return_vals[0][0], return_vals[0][1]

# Sample data test
tokens = ["Sydney", "is", "great"]
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
k = 1

answer = beam(tokens, distributions, transitions, labels, k)
if answer[0] != 0.0058482000000000004:
    print("Error in score")
    print(answer[0])
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")
    print(' '.join(answer[1]))


#print(sorted([[1, ["Z"]], [2, ["C"]], [1, ["E"]]], key=my_sort, reverse=True))
