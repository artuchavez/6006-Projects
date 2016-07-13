# Note that infinity can be represented by float('inf') in Python.

################################################################################
# You do not need to implement anything in this section below.
import math
#import copy


def dist(loc1, loc2):
    xdiff = loc1[0] - loc2[0]
    ydiff = loc1[1] - loc2[1]
    return math.sqrt(xdiff * xdiff + ydiff * ydiff)

import heapq
import itertools
# Borrowed heavily from https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.entry_finder = {}
        self.REMOVED = '<removed>'
        self.counter = itertools.count()
        self.num_elements = 0
        self.num_actions = 0

    def add(self, item, priority):
        if item in self.entry_finder:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entry_finder[item] = entry
        heapq.heappush(self.heap, entry)
        self.num_actions += 1
        self.num_elements += 1

    def remove(self, item):
        entry = self.entry_finder.pop(item)
        entry[-1] = self.REMOVED
        self.num_elements -= 1

    def pop(self):
        self.num_actions += 1
        while self.heap:
            priority, count, item = heapq.heappop(self.heap)
            if item is not self.REMOVED:
                self.num_elements -= 1
                del self.entry_finder[item]
                return item, priority
        raise KeyError('Pop from an empty priority queue')

    def head(self):
        priority, count, item = self.heap[0]
        while item is self.REMOVED:
            heapq.heappop(self.heap)
            priority, count, item = self.heap[0]
        return item, priority

    def empty(self):
        return self.num_elements == 0

# You do not need to implement anything in this section above.
################################################################################

# TODO: Implement both parts (a) and (b) with this function. If target is None,
# then return a list of tuples as described in part (a). If target is not None,
# then return a path as a list of states as described in part (b).
def dijkstra(n, edges, source, target=None):
    #print n,edges,source
    Q = PriorityQueue()
    d = {}
    p = {}
    for v in range(n):
        d[v] = float('inf')
        p[v] = None
        Q.add(v, float('inf'))
    d[source] = 0
    Q.add(source, 0)
    p[source] = None

    for z in range(n): #not empty
        tuple_u = Q.pop()
        u = tuple_u[0]
        if u == target and target != None:
            distance = d[u]
            ans = [u]
            while p[u] != None:
                ans.append(p[u])
                u = p[u]
            ans.reverse()
            #print 'Actions', Q.num_actions
            return (ans,distance)

        for next in edges[u]:
            if d[next[0]] > d[u] + next[1]:
                d[next[0]] = d[u] + next[1]
                p[next[0]] = u
                Q.add(next[0], d[u] + next[1])
    answer = []
    for i in range(n):
        answer.append((i,d[i],p[i]))
    sorted_answer = sorted(answer, key = correct, reverse=False)
    #print 'Actions', Q.num_actions
    return sorted_answer

def correct(elt):
    return elt[1]


# TODO: Implement part (c).
def bidirectional(n, edges, source, target):

    mu = [None, float('inf')]

    reverse_edges = {}
    for j in range(n):
        reverse_edges[j] = []
    for e in edges.items():
        start = e[0]
        for k in e[1]:
            destination_node = k[0]
            current = reverse_edges[destination_node]
            current.append((start, k[1]))

    #now we have 2 graphs and run 2 searches separately

    Q_forward = PriorityQueue()
    d_forward = {}
    p_forward = {}

    Q_backward = PriorityQueue()
    d_backward = {}
    p_backward = {}

    for v in range(n):
        d_forward[v] = float('inf')
        d_backward[v] = float('inf')
        p_forward[v] = None
        p_backward[v] = None
        #Q_forward.add(v, float('inf'))
        #Q_backward.add(v, float('inf'))

    #Q_backward = copy.deepcopy(Q_forward)
    d_forward[source] = 0
    Q_forward.add(source, 0)
    p_forward[source] = None

    d_backward[target] = 0
    Q_backward.add(target, 0)
    p_backward[target] = None

    for z in range(n): #not empty
        if Q_forward.head()[1] <= Q_backward.head()[1]:
            tuple_u = Q_forward.pop()
            u = tuple_u[0]
            for next in edges[u]:
                if d_forward[next[0]] > d_forward[u] + next[1]:
                    d_forward[next[0]] = d_forward[u] + next[1]
                    p_forward[next[0]] = u
                    Q_forward.add(next[0], d_forward[u] + next[1])
        else:
            tuple_u = Q_backward.pop()
            u = tuple_u[0]
            for next in reverse_edges[u]:
                if d_backward[next[0]] > d_backward[u] + next[1]:
                    d_backward[next[0]] = d_backward[u] + next[1]
                    p_backward[next[0]] = u
                    Q_backward.add(next[0], d_backward[u] + next[1])


        if d_forward[u] != float('inf') and d_backward[u] != float('inf'):
            if d_forward[u] + d_backward[u] < mu[1]:
                mu = [u, d_forward[u] + d_backward[u]]

            if mu[1] <= (Q_forward.head()[1] + Q_backward.head()[1]):
                distance = mu[1]
#                print "mu"
#                print mu
#                print 'forward', Q_forward.head()[1]
#                print 'backward', Q_backward.head()[1]
                u = mu[0]
                forward_ans = [u]
                while p_forward[u] != None:
                    forward_ans.append(p_forward[u])
                    u = p_forward[u]
                forward_ans.reverse()
                backwards_ans = []
                u = mu[0]
                while p_backward[u] != None:
                    backwards_ans.append(p_backward[u])
                    u = p_backward[u]
                #print 'forward_anssssss', forward_ans
                #print 'backwars_ansssss', backwards_ans
                forward_ans.extend(backwards_ans)
                #print (forward_ans,distance)
                #print 'num actions', Q_backward.num_actions, Q_forward.num_actions, Q_backward.num_actions+ Q_forward.num_actions
                return (forward_ans,distance)






# TODO: Implement part (d).
def astar(locs, edges, source, target):
    #print 'locs', locs
    Q = PriorityQueue()
    d = {}
    p = {}
    nodes = {}
    for v in range(len(locs)):
        nodes[v] = locs[v]
    #print nodes

    for v in nodes.keys():
        d[v] = float('inf')
        p[v] = None
        #Q.add(v, float('inf'))
    d[source] = 0
    Q.add(source, 0)
    p[source] = None

    for z in range(len(locs)): #not empty
        tuple_u = Q.pop()
        u = tuple_u[0]
        if u == target:
            distance = d[u]
            travel = 0
            ans = [u]
            while p[u] != None:
                travel += dist(nodes[u], nodes[p[u]])
                ans.append(p[u])
                u = p[u]
            ans.reverse()
            #print ans
            #print 'Actions', Q.num_actions
            return (ans, travel)

        for next in edges[u]:
            #print 'next', next
            if d[next] > d[u] + dist(nodes[u],nodes[next]) + dist(nodes[next],nodes[target]) - dist(nodes[u],nodes[target]):
                d[next] = d[u] + dist(nodes[u],nodes[next]) + dist(nodes[next],nodes[target]) - dist(nodes[u],nodes[target])
                p[next] = u
                #print d[u], dist(nodes[u],nodes[next]), dist(nodes[next],nodes[target]), dist(nodes[u],nodes[target])
                Q.add(next, d[u] + dist(nodes[u],nodes[next]) + dist(nodes[next],nodes[target]) - dist(nodes[u],nodes[target]))

        """
        for next in edges[u]:
            if d[next[0]]  > (d[u] + dist(locs[next[0]], locs[target]) - dist(locs[u], locs[target])):
                d[next[0]] = d[u] + dist(locs[next[0]], locs[target]) - dist(locs[u], locs[target])
                p[next[0]] = u
                Q.add(next[0], d[u] + dist(locs[next[0]], locs[target]) - dist(locs[u], locs[target]))
        """



