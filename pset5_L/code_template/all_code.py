# Note that infinity can be represented by float('inf') in Python.

################################################################################
# You do not need to implement anything in this section below.

def dist(loc1, loc2):
    xdiff = loc1[0] - loc2[0]
    ydiff = loc1[1] - loc2[1]
    return math.sqrt(xdiff * xdiff + ydiff * ydiff)

import heapq
import itertools
import math
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

    def peek(self):
        self.num_actions += 1
        while self.heap:
            priority, count, item = self.heap[0]
            if item is self.REMOVED:
                heapq.heappop(self.heap)
            else:
                return item, priority

    def head(self):
        priority, count, item = self.heap[0]
        return item, priority

    def empty(self):
        return self.num_elements == 0

# You do not need to implement anything in this section above.
################################################################################

# TODO: Implement both parts (a) and (b) with this function. If target is None,
# then return a list of tuples as described in part (a). If target is not None,
# then return a path as a list of states as described in part (b).
inf = float("inf")
def dijkstra(n, edges, source, target=None):
    distances = {}
    parents = {}
    for vertex in edges.keys():
        distances[vertex] = inf
        parents[vertex] = None
    distances[source] = 0
    S = []
    queue = PriorityQueue()
    queue.add(source, 0)

    while queue.empty() == False:
        u = queue.pop()
        curr_parent = u[0]
        S.append(curr_parent)
        if curr_parent == target:
            break
        for vertex in edges[curr_parent]:
            curr_vertex = vertex[0]
            curr_weight = vertex[1]
            if distances[curr_vertex] > distances[curr_parent] + curr_weight:
                distances[curr_vertex] = distances[curr_parent] + curr_weight
                parents[curr_vertex] = curr_parent
                queue.add(curr_vertex,distances[curr_vertex])

    answer = []

    if target == None:
        for vertex in edges.keys():
            answer.append((vertex, distances[vertex], parents[vertex]))
        return sorted(answer, key=lambda x: x[1])

    if target != None:
        length = distances[target]
        vertices_visited = []
        while target != source:
            vertices_visited.append(target)
            target = parents[target]
        vertices_visited.append(source)
        vertices_visited.reverse()
        answer = [vertices_visited, length]
        return answer
    return None


# TODO: Implement part (c).
def bidirectional(n, edges, source, target):
    mu = [None, float('inf')]

    distances = {}
    parents = {}
    for vertex in edges.keys():
        distances[vertex] = float('inf')
        parents[vertex] = None
    distances[source] = 0
    S = []
    queue = PriorityQueue()
    queue.add(source, 0)

    back_edges = {}
    for vertex in edges.keys():
        for other_end_tuple in edges[vertex]:
            second_node = other_end_tuple[0]
            dist = other_end_tuple[1]
            if second_node in back_edges:
                back_edges[second_node].append((vertex, dist))
            else:
                back_edges[second_node] = [(vertex,dist)]

    for node in edges.keys():
        if node not in back_edges.keys():
            back_edges[node] = [(0, -1)]


    back_distances = {}
    back_parents = {}
    for vertex in back_edges.keys():
        back_distances[vertex] = float('inf')
        back_parents[vertex] = None
    back_distances[target] = 0
    S2 = []
    back_queue = PriorityQueue()
    back_queue.add(target, 0)

    u = (source, 0)
    v = (target, 0)

    for z in range(n):
        if queue.head()[1] < back_queue.head()[1]:
            u = queue.pop()
            # print "first: ", queue.heap
            curr_parent = u[0]
            S.append(curr_parent)
            for vertex in edges[curr_parent]:
                curr_vertex = vertex[0]
                curr_weight = vertex[1]
                if distances[curr_vertex] > distances[curr_parent] + curr_weight:
                    distances[curr_vertex] = distances[curr_parent] + curr_weight
                    parents[curr_vertex] = curr_parent
                    queue.add(curr_vertex,distances[curr_vertex])
                for element in S2:
                    for edge in edges[curr_vertex]:
                        if edge[0] == element:
                            mu_original = mu
                            mu = min(mu, distances[curr_vertex] + edge[1] + back_distances[element])
                            #print "d: ", distances[curr_vertex]
                            #print "e: ", edge[1]
                            #print "b: ", back_distances[element]
                            #print "mu: ", mu
                            if mu != mu_original:
                                mu_forward = curr_vertex
                                mu_backward = element

        else:
            v = back_queue.pop()
            u = v
            # print "second: ", back_queue.heap
            curr_parent = v[0]
            S2.append(curr_parent)
            for vertex in back_edges[curr_parent]:
                curr_vertex = vertex[0]
                curr_weight = vertex[1]
                if back_distances[curr_vertex] > back_distances[curr_parent] + curr_weight:
                    back_distances[curr_vertex] = back_distances[curr_parent] + curr_weight
                    back_parents[curr_vertex] = curr_parent
                    back_queue.add(curr_vertex,distances[curr_vertex])
                for element in S:
                    for edge in back_edges[curr_vertex]:
                        if edge[0] == element:
                            mu_original = mu
                            mu = min(mu, distances[element] + edge[1] + back_distances[curr_vertex])
                            if mu != mu_original:
                                mu_forward = element
                                mu_backward = curr_vertex
        #print "mu: ", mu
        #print "distance queue: ", distances[queue.peek()[0]]
        #print "distance back queue: ", back_distances[back_queue.peek()[0]]

        if distances[u] != float('inf') and back_distances[u] != float('inf'):
            if distances[u] + back_distances[u] < mu[1]:
                mu = [u, distances[u] + back_distances[u]]

            if mu[1] <= (queue.head()[1] + back_queue.head()[1]):
                distance = mu[1]


    vertices_visited = []
    while mu_forward != source:
        vertices_visited.append(mu_forward)
        mu_forward = parents[mu_forward]

    while mu_backward != target:
        vertices_visited.append(mu_backward)
        mu_backward = back_parents[mu_backward]


    if source not in vertices_visited:
        vertices_visited.insert(0, source)

    if target not in vertices_visited:
        vertices_visited.append(target)

    answer = [vertices_visited, mu]
    #print "answer: ", answer
    return answer

# TODO: Implement part (d).
def astar(locs, edges, source, target):
    distances = {}
    parents = {}
    for vertex in edges.keys():
        distances[vertex] = inf
        parents[vertex] = None
    distances[source] = 0
    S = []
    queue = PriorityQueue()
    queue.add(source, 0)

    while queue.empty() == False:
        u = queue.pop()
        curr_parent = u[0]
        S.append(curr_parent)
        if curr_parent == target:
            break
        for vertex in edges[curr_parent]:
            if distances[vertex] > distances[curr_parent] + dist(locs[curr_parent],locs[vertex]):
                distances[vertex] = distances[curr_parent] + dist(locs[curr_parent],locs[vertex])
                parents[vertex] = curr_parent
                queue.add(vertex,distances[vertex]+dist(locs[vertex],locs[target])-dist(locs[source],locs[target]))

    answer = []

    if target != None:
        length = distances[target]
        vertices_visited = []
        while target != source:
            vertices_visited.append(target)
            target = parents[target]
        vertices_visited.append(source)
        vertices_visited.reverse()
        answer = [vertices_visited, length]
        return answer
    return None






