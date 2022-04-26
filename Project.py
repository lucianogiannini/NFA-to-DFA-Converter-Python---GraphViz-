import graphviz
from graphviz import Digraph

class NFA:
  def __init__(self, num_states, state_names, epsilon, start_state, final_states, transitions):
    self.num_states = num_states
    self.state_names = state_names
    self.epsilon = epsilon
    self.epsilon.append('e')
    self.epsilon_len = len(epsilon)
    self.start_state = start_state
    self.final_states = final_states
    self.transitions = transitions
    self.transitions_len = len(transitions)
    self.graph = Digraph()
    #2d array of state names and epsilon
    self.states_dict = dict()
    self.reverse_state_dict = dict()
    for i in range(self.num_states):
      self.states_dict[self.state_names[i]] = i
      self.reverse_state_dict[i] = self.state_names[i]
    self.epsilon_dict = dict()
    self.reverse_epsilon_dict = dict()
    for i in range(self.epsilon_len):
      self.epsilon_dict[self.epsilon[i]] = i
      self.reverse_epsilon_dict[i] = self.epsilon[i]
    self.transition_matrix = [[[0] for x in range(self.epsilon_len)] for y in range(self.num_states)]
    #print('\n')
    #print(self.reverse_epsilon_dict)
    #print('\n')

    #print(self.transition_matrix)
    for i in transitions:
        self.transition_matrix[self.states_dict[i[0]]][self.epsilon_dict[i[1]]].append(i[2])
    #print(self.transition_matrix)
    for i in range(len(self.transition_matrix)):
        for j in range(len(self.transition_matrix[i])):
            if len(self.transition_matrix[i][j]) > 1:
                self.transition_matrix[i][j].pop(0)
    
    #print('\n')
    #print transition_matrix
    print("NFA Transition Matrix:")
    for i in range(len(self.transition_matrix)):
        for j in range(len(self.transition_matrix[i])):
            print(self.transition_matrix[i][j], end=' ')
        print('\n')
    #making graph for NFA
    for x in self.state_names:
        if (x not in self.final_states):
            self.graph.attr('node', shape='circle')
            self.graph.node(x)
        else:
            self.graph.attr('node', shape='doublecircle')
            self.graph.node(x)
    self.graph.attr('node', shape='none')
    self.graph.node('')
    self.graph.edge('', self.start_state)

    #self.graph.render('nfa', view=True)
    # now need edges
    for i in range(len(self.transition_matrix)):
        for j in range(len(self.transition_matrix[i])):
            if len(self.transition_matrix[i][j]) > 0 and self.transition_matrix[i][j][0] != 0:
                for k in range(len(self.transition_matrix[i][j])):
                    #print(self.reverse_state_dict[i], self.transition_matrix[i][j][k], self.reverse_epsilon_dict[j])
                    self.graph.edge(self.reverse_state_dict[i], self.transition_matrix[i][j][k], label=('ε', self.reverse_epsilon_dict[j])[self.reverse_epsilon_dict[j] != 'e'])
    self.graph.render('nfa', view=True)
    #print out quintuple
    print('NFA Quintuple:')
    print("Q : " + str(self.state_names)+"\nΣ : "
    + str(self.epsilon)+"\nq0 : "
    + str(self.start_state)+"\nF : "+str(self.final_states) + \
			"\nδ : \n" + str(self.transition_matrix))
    def get_transition(state):
        #print(state)
        #print(trans_char)
        if not isinstance(state, list):
            #print(self.states_dict.get(state))
            #print(self.epsilon_dict.get(trans_char))
            return state
        else:
            states = list()
            for j in state:
                #print(state)
                states.extend(j)
            return states
    
    dfa_matrix = dict()
    nfa_transitions = []
    for i in range(len(self.transition_matrix)):
        #print(self.transition_matrix[i][len(self.transition_matrix[i])-1])
        if self.transition_matrix[i][len(self.transition_matrix[i])-1] != [0]:
            key = [self.reverse_state_dict[i]]
            for k in range(len(self.transition_matrix[i][len(self.transition_matrix[i])-1])):
                new_state = self.transition_matrix[i][len(self.transition_matrix[i])-1][k]
                key.append(new_state)
            set(key)
            key.sort()
            key = "".join(key)
            dfa_matrix[key] = [0]
        else:
            key = [self.reverse_state_dict[i]]
            #print(key)
            dfa_matrix[key[0]] = [0]
        
        print(dfa_matrix)
    while(check_dict_for_new_states(dfa_matrix)):
        for j in dfa_matrix.copy():
            if dfa_matrix[j] == [0]:
                #print("j",j)
                state = split(j)
                print("state", state)
                for p in range(len(self.transition_matrix[i])-1):
                    new_state = []
                    for k in state:
                        i = self.states_dict[k]
                        if self.transition_matrix[i][p][0] != 0:
                            new_state.extend(get_transition(self.transition_matrix[i][p]))
                    new_state = remove_dups(new_state)
                    set(new_state)
                    print("New State: ",new_state)
                    new_state = [h for h in new_state if h != 0]
                    new_state.sort()
                    
                    if not len(new_state) == 0:
                        new_state = "".join(new_state)
                        #print("new_state: ",new_state)
                        if new_state not in dfa_matrix:
                            if new_state not in j:
                                dfa_matrix[new_state] = [0]
                        if new_state not in j:
                            dfa_matrix[j].append(new_state)
                        else:
                            dfa_matrix[j].append(j)
                    else:
                        dfa_matrix[j].extend([0]) 
    print(dfa_matrix)
    clear_empty_dict(dfa_matrix)
    print("dfa_matrix: ",dfa_matrix)
    remove_first_state(dfa_matrix)
    print("dfa_matrix: ",dfa_matrix)
    check_for_dups(dfa_matrix)
    print("dfa_matrix: ",dfa_matrix)
    check_if_node_has_any_incoming_arrows(dfa_matrix,find_dfa_start_state(self, dfa_matrix, self.start_state))
    print("dfa_matrix: ",dfa_matrix)
    print('\n')
    dfa_matrixx = [[0 for x in range(self.epsilon_len-1)] for y in range(len(dfa_matrix))]
    #print("dfa_matrixx: ",dfa_matrixx)
    
    c = 0 
    for i in dfa_matrix:
        for j in range(self.epsilon_len-1):
            temp = dfa_matrix[i]
            dfa_matrixx[c][j] = temp[j]
        c += 1
    print("DFA Transition Matrix: ")
    for i in range(len(dfa_matrixx)):
        for j in range(len(dfa_matrixx[i])):
            print(dfa_matrixx[i][j], end=' ')
        print('\n')
    

    dfa_start_state = find_dfa_start_state(self, dfa_matrix, self.start_state)
    dfa = Digraph()
    for i in dfa_matrix:
        if(isFinalState(i, self.final_states) == False):
            dfa.attr('node', shape='circle')
            dfa.node(i)
        else:
            dfa.attr('node', shape='doublecircle')
            dfa.node(i)
    dfa.attr('node', shape='none')
    dfa.node('')
    dfa.edge('', dfa_start_state)
    dfa.attr('node', shape='circle')
    dfa.node('ϕ')
    #dfa.render('dfa', view=True)
    dfa_reverse_state_dict = dict()
    m = 0
    for i in dfa_matrix:
        dfa_reverse_state_dict[m] = i
        m += 1
    #print("dfa_reverse_state_dict: ",dfa_reverse_state_dict)
    for i in range(len(dfa_matrixx)):
        for j in range(len(dfa_matrixx[i])):
            if dfa_matrixx[i][j] != 0:
                #print(dfa_reverse_state_dict[i], dfa_matrixx[i][j], self.reverse_epsilon_dict[j])
                dfa.edge(dfa_reverse_state_dict[i], dfa_matrixx[i][j], label=('ε', self.reverse_epsilon_dict[j])[self.reverse_epsilon_dict[j] != 'e'])
            else:
                dfa.edge(dfa_reverse_state_dict[i], 'ϕ', self.reverse_epsilon_dict[j])
        
    for j in range(len(dfa_matrixx[0])):    
        dfa.edge('ϕ', 'ϕ', self.reverse_epsilon_dict[j])
    dfa.render('dfa', view=True)
def find_dfa_start_state(self, dfa_matrix, start_state):
    for i in dfa_matrix:
        if self.start_state in i:
            return i
    return None

def isFinalState(state, final_states):
    for i in final_states:
        if i in state or i == state:
            return True
    return False

def split(word):
    return [char for char in word]
    
def check_dict_for_new_states(dfa_matrix):
    for i in dfa_matrix:
        if dfa_matrix[i] == [0]:
            return True
def clear_empty_dict(dfa_matrix):
    for i in dfa_matrix.copy():
        bools = False
        for j in dfa_matrix[i]:
            if j != 0:
                bools = True
        if not bools:
            dfa_matrix.pop(i)
    return dfa_matrix
def remove_first_state(dfa_matrix):
    for i in dfa_matrix.copy():
        dfa_matrix[i].pop(0)
def check_for_dups(dfa_matrix):
    counti = 0
    
    for i in dfa_matrix.copy():
        #print("i",i)
        countj = 0
        for j in dfa_matrix.copy():
            if countj != counti+1:
                countj = countj + 1
                continue
            elif i in j:
                #print(i, dfa_matrix[i], "FIRST")
                #print(j, dfa_matrix[j], "SECOND")
                if dfa_matrix[i] == dfa_matrix[j]:
                    removed = i
                    leftover = remove_same(removed, j)
                    print("leftover", leftover)
                    print(removed, "removed")
                    dfa_matrix.pop(i)
                    for k in dfa_matrix.copy():
                      newdict = {}
                      print("k",k)
                      newdict[k] = []
                      print(newdict)
                      for l in dfa_matrix[k]:
                        print("l", l)
                        if l == removed:
                          newdict[k].append(j)
                        elif l == leftover:
                          print("here")
                          newdict[k].append(j)
                        else:
                          newdict[k].append(l)
                      print(newdict)
                      dfa_matrix.update(newdict)
                        
        counti = counti + 1
    return dfa_matrix
def check_if_node_has_any_incoming_arrows(dfa_matrix , start_state):
    for i in dfa_matrix.copy():
        used = False
        if start_state != i:
            values = dfa_matrix.values()
            #print(values)
            for j in values:
                  for k in j:
                    if i == k:
                      used = True
                      break
            if not used:
                dfa_matrix.pop(i)
def remove_dups(arr):
  res = []
  for i in arr:
    if i not in res:
        res.append(i)
  return res

def remove_same(first, second):
  temp = ""
  for i in second:
    if first != i:
      temp +=i
  return temp
def main():
    ############################
    ##Used for Input from User##
    ############################
    print("Please enter the information for the NFA:")
    num_states = int(input("Number of states: "))
    state_names = []
    for i in range(num_states):
        state_names.append(input("State name: "))
    epsilon =  []
    while True:
        epsilon_input = input("Epsilon: ")
        if epsilon_input == "":
            break
        epsilon.append(epsilon_input)
    start_state = input("Start state: ")
    final_states = []
    while True:
        final_states_input = input("Final states: ")
        if final_states_input == "":
            break
        final_states.append(final_states_input)
    transitions = []
    while True:
        transitions_input = input("Transitions: format: (state, input, next_state) (use e for epsilon transition): ")
        if transitions_input == "":
            break
        temp_trans = transitions_input.split(",");
        transitions.append(temp_trans)
    
    #print all data
    # print(num_states)
    # print(state_names)
    # print(final_states)
    # print(start_state)
    # print(epsilon)
    # print(transitions)

    # nfa = NFA(num_states, state_names, epsilon, start_state, final_states, transitions)
    #EXAMPLES#
    #all strings composed of 0 or more occurrences of 101 example string  = 101101101101101101
    # nfa = NFA(4,
    # ['A', 'B', 'C', 'D'],
    # ['x', 'y'],
    # 'A',
    # ['D'],
    # [['A', 'y', 'B'], ['B', 'x', 'C'], ['C', 'y', 'D'], ['D', 'e', 'A']])

  #   nfa = NFA(4, # number of states
	# ['A', 'B', 'C', 'D'], # array of states
	# ['a', 'b', 'c'], # array of alphabets
	# 'A', # start state
	# ['D'], # array of final states
	# [['A', 'a', 'A'], ['A', 'e', 'B'], ['B', 'b', 'B'],
	# ['A', 'e', 'C'], ['C', 'c', 'C'], ['B', 'b', 'D'],
	# ['C', 'c', 'D']])

  # nfa = NFA(5, # number of states
	# ['A', 'B', 'C', 'D', 'F'], # array of states
	# ['a', 'b', 'c', 'd'], # array of alphabets
	# 'A', # start state
	# ['D'], # array of final states
	# [['A', 'a', 'A'], ['A', 'e', 'B'], ['B', 'b', 'B'],
	# ['A', 'e', 'C'], ['C', 'c', 'C'], ['B', 'b', 'D'],
	# ['C', 'c', 'D'], ['D', 'd', 'F'], ['F', 'd', 'F']])
main()


