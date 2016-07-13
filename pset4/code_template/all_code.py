################################################################################
#
# States are represented by 3-tuples of integers in the range 0, ..., k.
#
# Transitions are 2-tuples of states (start_state, end_state), where start_state
# is the start of the transition and end_state is the end of the transition.
#
# Reachable states should be represented by a 3-tuple (state, length, previous)
# where state is the reachable state, length is the length of the path to get
# there, and previous is the previous state. For the 0 length path to the start,
# that would be (start, 0, start).
#
################################################################################

# start is a state, a 3-tuple (x, y, z) where 0 <= x, y, z <= k
# transitions is a list of 2-tuples of 3-tuples (x, y, z)
#   where 0 <= x, y, z <= k.
# Note that the start state is reachable through a path of length 0.

def reachable_states(s, transitions):
    #create a dictionary with all the valid transitions from each node
    trans_dict = {}
    nodes = {}
    trans_dict[s] = []
    for elt in transitions:
        trans_dict[elt[0]] = []
        trans_dict[elt[1]] = []
        nodes[elt[0]] = 'node'

    #print nodes_list
    for elt in transitions:
        moves_list = trans_dict[elt[0]]
        moves_list.append(elt[1])
        trans_dict[elt[0]] = moves_list

    #find the shortest path
    colors = {}
    distances = {}
    parents = {}
    for v in trans_dict.keys():
        colors[v] = 'white'
        distances[v] = float('inf')
        parents[v] = None
    colors[s] = 'grey'
    distances[s] = 0
    parents[s] = s
    Q = []
    Q.append(s)
    while Q: #while the queue is not empty.....
        u = Q.pop(0)
        if u not in trans_dict:
            continue
        for v in trans_dict[u]:
            if colors[v] == 'white':
                colors[v] = 'grey'
                distances[v] = distances[u] + 1
                parents[v] = u
                Q.append(v)
        colors[u] = 'black'
    # construct the output we need
    answer = []
    unique = {}
    for v in trans_dict.keys():
        if distances[v] == float('inf'):
            continue
        elements = (v, distances[v], parents[v])
        if v not in unique:
            answer.append(elements)
            unique[v] = elements

    #answer.append((s,distances[s],parents[s]))

    # sort the output

    def getKey(item):
        return item[1]
    answer.sort(key=getKey)
    return answer




# Returns either a path as a list of reachable states if the target is
# reachable or False if the target isn't reachable.
def simple_machine(k, start, target):
    #print 'start', start, 'target', target, k
    frontier = [start]
    distances = dict()
    parents = dict()
    distances[start] = 0
    while len(frontier) != 0:
        u = frontier.pop(0)
        for v in valid_transitions(u, k):
            if v not in distances: #has not been visited
                parents[v] = u
                distances[v] = distances[u] + 1
                frontier.append(v)
                if v == target:
                    return FindPath(start, v, parents)
    return False



"""
    # calculate all the transitions
    # run previous alg
    # backwards define the path
    state = start
    all_choices = []
    while valid_transitions(state,k) != []:
        new = valid_transitions(state,k)
        for elt in new:
            if elt not in unique_trans:
                unique_trans[elt] = 'discovered'
                state = elt[1]
        all_choices.extend(new)
    print all_choices
"""



"""
    visited = {}
    visited[start] = 'visited'
    parent = {}
    parent[start] = None
    queue = []
    queue.append(start)
    while queue:
        u = queue.pop()
        choices = valid_transitions(u,k)
        if not choices:
            return False
        for next_state in choices:
            if next_state not in visited:
                visited[next_state] = 'visited'
                parent[next_state] = u
                queue.append(next_state)
                if next_state == target:
                    break

    #WHAT IF NOT AT TARGET
    #find the path
"""
def FindPath(start, target, parent):
        path = [target]
        while path[-1] != start:
            predecessor = parent[path[-1]]
            path.append(predecessor)
        path.reverse()
        return path



def valid_transitions(state,k):
    ok_transitions = []
    a = state[0]
    b = state[1]
    c = state[2]
    if within_k(a+1,k) and within_k(b+1,k) and within_k(c+1,k):
        ok_transitions.append(((a+1,b+1,c+1)))
    if within_k(a-1,k) and within_k(b-1,k) and within_k(c-1,k):
        ok_transitions.append(( (a-1,b-1,c-1)))
    if within_k(a+1,k) and within_k(b,k) and within_k(c,k):
        ok_transitions.append(((a+1,b,c)))
    if within_k(a-1,k) and within_k(b,k) and within_k(c,k):
        ok_transitions.append(((a-1,b,c)))
    return ok_transitions

def within_k(num,k):
    if num <= k and num >= 0:
        return True

def simple_machine2(k, start, target, trans_funct):
    #print 'start', start, 'target', target, k
    unique_trans = {}
    universe = []
    for i in range(0,k+1):
        #print 'doneeeeee' + str(i)
        for j in range(0,k+1):
            for h in range(0,k+1):
                new = trans_funct((i,j,h), k)
                #universe.extend(new)
                for elt in new:
                    if elt not in unique_trans:
                        unique_trans[elt] = 'discovered'
                        universe.append(elt)
    all_trans = reachable_states2(start, universe)
    for thing in all_trans[0]:
        if thing[0] == target or thing[2] == target:
            money = FindPath(start, target, all_trans[1])
            return money
    return False

def valid_transitions2(state,k):
    ok_transitions = []
    a = state[0]
    b = state[1]
    c = state[2]
    if a == 0:
        ok_transitions.append((state, (a+1,b,1)))
    if b == 0:
        ok_transitions.append((state, (a,1,2)))
    if a == 1 and b==0:
        ok_transitions.append((state, (3,0,c)))
    if a == 0 and b==1:
        ok_transitions.append((state, (0,3,c)))
    if a ==1 and c == 2:
        ok_transitions.append((state, (3,b,2)))
    if b ==1 and c == 1:
        ok_transitions.append((state, (a,3,1)))
    if a == 3:
        ok_transitions.append((state, (0,b,c)))
    if b == 3:
        ok_transitions.append((state, (a,0,c)))
    return ok_transitions


# Returns either False if the mutual exclusion property is satisfied or
# a minimum-length counterexample as a list of reachable states.
def mutual_exclusion_1():
    # TODO: Implement part c.
    initial_state = (0,0,1)
    try1 = simple_machine2(3,initial_state,(3,3,0),valid_transitions2)
    try2 = simple_machine2(3,initial_state,(3,3,1),valid_transitions2)
    try3 = simple_machine2(3,initial_state,(3,3,2),valid_transitions2)
    try4 = simple_machine2(3,initial_state,(3,3,3),valid_transitions2)

    possibles = [try1, try2, try3, try4]
    current_ans = False
    for elt in possibles:
        if elt != False and len(elt) < len(current_ans):
            current_ans = elt
    return current_ans

def valid_transitions3(state,k):
    ok_transitions = []
    a = state[0]
    b = state[1]
    c = state[2]
    if a == 0 and c == 0:
        ok_transitions.append((state, (1,b,0)))
    if b == 0 and c ==0:
        ok_transitions.append((state, (a,1,0)))
    if a == 1:
        ok_transitions.append((state, (2,b,1)))
    if b==1:
        ok_transitions.append((state, (a,2,2)))
    if a ==2 and c == 1:
        ok_transitions.append((state, (3,b,1)))
    if b ==2 and c == 2:
        ok_transitions.append((state, (a,3,2)))
    if a == 3:
        ok_transitions.append((state, (0,b,0)))
    if b == 3:
        ok_transitions.append((state, (a,0,0)))
    if a == 2 and c != 1:
        ok_transitions.append((state, (0,b,c)))
    if b == 2 and c != 2:
        ok_transitions.append((state, (a,0,c)))

    return ok_transitions


# Returns either False if the mutual exclusion property is satisfied or
# a minimum-length counterexample as a list of reachable states.
def mutual_exclusion_2():
    # TODO: Implement part d.
    initial_state = (0,0,0)
    try1 = simple_machine2(3,initial_state,(3,3,0),valid_transitions3)
    try2 = simple_machine2(3,initial_state,(3,3,1),valid_transitions3)
    try3 = simple_machine2(3,initial_state,(3,3,2),valid_transitions3)
    try4 = simple_machine2(3,initial_state,(3,3,3),valid_transitions3)

    possibles = [try1, try2, try3, try4]
    current_ans = False
    for elt in possibles:
        if elt != False:
            if current_ans == False:
                current_ans = elt
            elif len(elt) < len(current_ans):
                current_ans = elt
    return current_ans



def reachable_states2(s, transitions):
    # TODO: Implement part a.
    #create a dictionary with all the valid transitions from each node
    trans_dict = {}
    nodes = {}
    trans_dict[s] = []
    for elt in transitions:
        trans_dict[elt[0]] = []
        trans_dict[elt[1]] = []
        nodes[elt[0]] = 'node'

    #print nodes_list
    for elt in transitions:
        moves_list = trans_dict[elt[0]]
        moves_list.append(elt[1])
        trans_dict[elt[0]] = moves_list

    #find the shortest path
    colors = {}
    distances = {}
    parents = {}
    for v in trans_dict.keys():
        colors[v] = 'white'
        distances[v] = float('inf')
        parents[v] = None
    colors[s] = 'grey'
    distances[s] = 0
    parents[s] = s
    Q = []
    Q.append(s)
    while Q: #while the queue is not empty.....
        u = Q.pop(0)
        if u not in trans_dict:
            continue
        for v in trans_dict[u]:
            if colors[v] == 'white':
                colors[v] = 'grey'
                distances[v] = distances[u] + 1
                parents[v] = u
                Q.append(v)
        colors[u] = 'black'
    # construct the output we need
    answer = []
    unique = {}
    for v in trans_dict.keys():
        if distances[v] == float('inf'):
            continue
        elements = (v, distances[v], parents[v])
        if v not in unique:
            answer.append(elements)
            unique[v] = elements

    #answer.append((s,distances[s],parents[s]))

    # sort the output

    def getKey(item):
        return item[1]
    answer.sort(key=getKey)
    return answer, parents

