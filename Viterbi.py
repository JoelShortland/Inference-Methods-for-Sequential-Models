def my_sort(x):
    return x[0], ' '.join(x[1])
import itertools
# This is the function you need to implement
def viterbi(tokens, distributions, transitions, labels):
    #Observations = transitions
    #First get transitions x distributions matrix
    viterbi_matrix = [[None for j in range(len(tokens))] for i in range(len(labels))]
    backpointer = [[None for j in range(len(tokens))] for i in range(len(labels))]
    labels = list(sorted(labels)) # Use sorted to prevent RNG

    for s in range(len(labels)):
        viterbi_matrix[s][0] = transitions.get(("START", labels[s])) * distributions[0].get(labels[s])
        if len(tokens) == 1:
            viterbi_matrix[s][0]*= transitions.get((labels[s], "END"))

        backpointer[s][0] = None
        
    for t in range(1, len(distributions)):
        for s in range(len(labels)):
            #Max viterbi_matrix Statement
            viterbi_matrix[s][t] = -1
            current_s = -1
            for s_dash in range(len(labels)):
                if t == len(distributions)-1:
                    temp = viterbi_matrix[s_dash][t-1] * distributions[t].get(labels[s]) * transitions.get((labels[s_dash], labels[s])) * transitions.get((labels[s], "END"))
                else:
                    temp = viterbi_matrix[s_dash][t-1] * distributions[t].get(labels[s]) * transitions.get((labels[s_dash], labels[s]))
                
                
                if temp > viterbi_matrix[s][t]:
                    viterbi_matrix[s][t] = temp
                    backpointer[s][t] = s_dash
                    current_s = s_dash

                elif temp == viterbi_matrix[s][t]:
                    #We change if whatever label comes first in alphapickle order is better
                    if t == len(distributions)-1:
                        print(sorted([labels[current_s], labels[s]], reverse = True)[0])
                        print(labels[current_s])
                        print(labels[s])
                    if sorted([labels[current_s], labels[s]], reverse = True)[0] == labels[s]:
                        print("Changing: " + str(labels[current_s]))
                        viterbi_matrix[s][t] = temp
                        backpointer[s][t] = s_dash
                        current_s = s_dash

            

    #At this point matrix is complete, get the best value at the end for each label, take it for our best score, and calculate
    best_score = 0
    best_s = -1
    best_path_pointer = -1
    for s in range(len(labels)):
        if viterbi_matrix[s][-1] > best_score:
            best_score = viterbi_matrix[s][-1]
            best_path_pointer = s
            
        elif viterbi_matrix[s][-1] == best_score:
            if sorted([labels[s], labels[best_path_pointer]], reverse = True)[0] == labels[s]:
                best_score = viterbi_matrix[s][-1]
                best_path_pointer = s

        

    #print(backpointer)
    #print(best_path_pointer)
    best_path = [best_path_pointer]

    j = len(distributions) - 1
    while j > 0:
        #print(best_path)
        best_path.insert(0, backpointer[best_path[0]][j])
        j -= 1

    for i in range(len(best_path)):
        best_path[i] = labels[best_path[i]]

    
    print(viterbi_matrix)
   #print(best_path)
    return best_score, best_path

# Sample data test
tokens = ["Sydney", "is", "great"]
distributions = [
    {"LOC": 0.5, "O": 0.5},
    {"LOC": 0.5, "O": 0.5},
    {"LOC": 0.5, "O": 0.5},
]
transitions = {
    ("START", "O"): 0.5,
    ("START", "LOC"): 0.5,
    ("START", "END"): 0.0,
    ("O", "END"): 0.5,
    ("O", "O"): 0.5,
    ("O", "LOC"): 0.5,
    ("LOC", "END"): 0.5,
    ("LOC", "O"): 0.5,
    ("LOC", "LOC"): 0.5,
}
labels = {"LOC", "O"}

answer = viterbi(tokens, distributions, transitions, labels)
if answer[0] != 0.0058482000000000004:
    print("Error in score")
    print(answer[0])
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")
    print(' '.join(answer[1]))
