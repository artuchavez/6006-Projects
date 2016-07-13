import math
import bisect
import StringIO
import collections

###################################################################
# Part (d)
#   Description:
#       Gradebook is a data structure that keeps track of every student
#       and their grade information. The cool thing about Gradebook is that
#       returning the k most average students takes only O(k) time, and 
#       updating a student's grade takes O(log(n) + k) time! Unfortunately,
#       it hasn't been implemented yet.
#
#   Hint:
#       In your data structure, you will need to keep a running average of
#       each student's grade. The way to do that is to keep track, for each
#       student, of the total number of credits the student has taken so far, 
#       and the sum of his grades weighted by the number of credits. 
#       For instance, if a student takes a 12-unit and then a 6-unit class and
#       gets a 5 then a 2, we keep track of (18, 72). Then, the student's 
#       GPA is 72/18=4.
#
#   TODO: 
#       Using your design in part (c), use "__init__" to define and initialize
#       the data structures you will need, and then fill in the methods 
#       "update_grade", "average", and "middle" (descriptions below).
###################################################################


class Gradebook:

    # TODO
    def __init__(self, student_names, k):
        self.k = k
        self.grade_dict = {}
        self.current_gpa_list = []
        for i in range(len(student_names)):
            self.grade_dict[student_names[i]] = (0,0)
            self.current_gpa_list.append(0)
        self.people = self.grade_dict.keys()
        self.num_students = len(self.people)
        self.lower_half = int(math.ceil((self.num_students-k)/2))
        self.middle_peeps = int(self.lower_half)
        self.upper_half = int(self.lower_half + self.middle_peeps+1)
        self.overachievers = Min_Heap(self.people[self.upper_half:], self.current_gpa_list[self.upper_half:])
        self.underachievers = Max_Heap (self.people[0:self.lower_half], self.current_gpa_list[0:self.lower_half])
        self.average_k = []
        for w in range(self.middle_peeps, self.upper_half):
            self.average_k.append((student_names[w], 0))



    def insert_into_k(self,list, new):
        size = len(list)
        for elt in range(size):
            if list[elt] > new[1]:
                list.insert(elt, new)
                return
        list.insert(size, new)
        return


    # TODO
    def update_grade(self, student, credit, grade):
        # Updates student with the new credit and grade information, and 
        # makes sure "middle()" still returns the k most average students 
        # in O(k) time. Does not need to return anything.
        current_grade_info = self.grade_dict[student]

        # tells us which heap student currently is in
        rootmin = self.overachievers.minimum()
        rootmax = self.underachievers.maximum()


        # if student is in the overachievers
        if current_grade_info[1] > rootmin[1]: # in self.overachievers.keys():
            self.overachievers.min_heap_modify(student, -50)
            self.overachievers.extract_min()
            updated_grade = (current_grade_info[0] * current_grade_info[1] + credit * grade) / float(credit + current_grade_info[0])
            self.grade_dict[student] = (credit+current_grade_info[0], updated_grade)
            #if self.average_k[0][0] == student:
            #    self.average_k[0][1] = updated_grade
            if updated_grade >= self.average_k[-1][1] :
                self.overachievers.insert_key(student, updated_grade)
                #self.overachievers.min_heap_modify(student, updated_grade)
            else:
                self.overachievers.insert_key(self.average_k[-1][0], self.average_k[-1][1])
                self.average_k.pop(-1)
                self.insert_into_k(self.average_k, (student, updated_grade))
                #self.average_k.append((student,updated_grade))


        # if student is in the underachievers
        elif current_grade_info[1] > rootmax[1]: #student in self.underachievers.keys():
            self.underachievers.max_heap_modify(student, 1000)
            self.underachievers.extract_max()
            updated_grade = (current_grade_info[0] * current_grade_info[1] + credit * grade) / float(credit + current_grade_info[0])
            self.grade_dict[student] = (credit+current_grade_info[0], updated_grade)
            #if self.average_k[0][0] == student:
            #    self.average_k[0][1] = updated_grade
            if updated_grade <= self.average_k[0][1]:
                self.underachievers.insert_key(student, updated_grade)
                #self.underachievers.max_heap_modify(student, updated_grade)
            else:
                self.underachievers.insert_key(self.average_k[0][0], self.average_k[0][1])
                self.average_k.pop(0)
                self.insert_into_k(self.average_k, (student, updated_grade))
                #self.average_k.append((student,updated_grade))

        #if the student average before update
        else:
            updated_grade = (current_grade_info[0] * current_grade_info[1] + credit * grade) / float(credit + current_grade_info[0])
            self.grade_dict[student] = (credit+current_grade_info[0], updated_grade)
            for elt in range(self.k):
                if self.average_k[elt][0] == student:
                    self.average_k.pop(elt)
                    break
            if updated_grade > rootmin[1]:
                new_add = self.overachievers.extract_min()
                self.overachievers.insert_key(student, updated_grade)
                #self.overachievers.min_heap_modify(student, updated_grade)
                self.insert_into_k(self.average_k, (new_add[0],new_add[1]))
            elif updated_grade < rootmax[1]:
                new_add = self.underachievers.extract_max()
                self.underachievers.insert_key(student, updated_grade)
                #self.underachievers.max_heap_modify(student, updated_grade)
                self.insert_into_k(self.average_k, (new_add[0],new_add[1]))
            else:
                self.insert_into_k(self.average_k, (student, updated_grade))
                # self.average_k.append((student,updated_grade))



        #find where he is......
        #remove him from there by making huge(max heap), tiny(min heap)
        #place him in k list
        #put the smallest/largest into the heap
        # updates his grade
        # check if larger than largest of k OR smaller than smallest of k
            # if larger then we exchange with the root of min heap (or vice versa)
        #if belongs in k: push smallest into the heap (and vice versa)


    # TODO
    def average(self, student):
        # Return a single number representing the GPA for student
        grade_info = self.grade_dict[student]
        print grade_info
        return grade_info[1]

    # TODO
    def middle(self):
        # Return the k most average students and their GPAs as a 
        #   list of tuples, e.g. [(s1, g1),(s2,g2)]
        print self.average_k
        return self.average_k

###################################################################
# Part (a)
#   Description:
#       Max_Heap is a general implementation of a max-heap modified to accept
#       (key, data) pairs. For instance, in the student GPA problem, the 
#       "key" would a student name and the "data" would be the student's GPA,
#       e.g. ("Bob Dylan", 1) 
#
#   Implementation/Initialization Details:
#       The keys (i.e. student names) are stored in a list called "self.keys"
#       The data (i.e. student GPAs) are stored in a list called "self.data"
#       Additionally, a dictionary called "self.key_to_index_mapping" keeps
#       track of the index of the key in the array. For instance, if we had 
#       the following list of (key, data) pairs, which already satisfies the 
#       max-heap property:
#
#           [("Ray Charles", 4), ("Bob Dylan", 1), ("Bob Marley", 3)]
#           
#       then,       self.keys = ["Ray Charles", "Bob Dylan", "Bob Marley"]
#                   self.data = [4, 1, 3]
#           self.key_to_index = {"Ray Charles": 0, 
#                                "Bob Dylan": 1,
#                                "Bob Marley": 2} 
#       where 0, 1, 2 corresponds to the index in "self.keys"
#
#   Provided Methods:
#       All the methods presented in lecture and recitation are provided, with
#       only slight changes to accomodate the (key, data) pair modification.
#       In addition, we provide the method show_tree(self) so that you may 
#       print out what your heap looks like.
#
#   TODO: Fill out the method "max_heap_modify(self, key, data)", which modifies, 
#       the data of "key" to the new "data" and restores the heap invariant. 
#       For instance, using the example above, we may call:
#           
#           heap.max_heap_modify("Bob Marley", 5)
#
#       This should change Bob Marley's grade to 5, and then restore
#       the heap invariant so that the data structure looks like this:
#   
#               self.keys = ["Bob Marley", "Bob Dylan", "Ray Charles"]
#               self.data = [5, 1, 4]
#       self.key_to_index = {"Ray Charles": 2, 
#                           "Bob Dylan": 1,
#                           "Bob Marley: 0"} 
###################################################################
class Max_Heap:

    def __init__(self, keys, data):
        assert len(keys) == len(data)
        
        self.keys = collections.deque(keys)
        self.data = collections.deque(data)
        self.key_to_index = dict(zip(self.keys, range(len(self.keys)))) #!
        self.heapify()

    # TODO
    def max_heap_modify(self, key, data):
        print key
        spot = int(self.key_to_index[key])
        if self.data[spot] > data:
            self.data[spot] = data
            self.max_heapify(spot)
        elif self.data[spot] < data:
            self.increase_key(spot, data)

    def maximum(self):
        return (self.keys[0], self.data[0])

    def extract_max(self):
        if len(self.keys)<1:
            raise Exception("No elements in heap!")
        sm, gm = self.keys.popleft(), self.data.popleft()
        del self.key_to_index[sm]
        if len(self.keys) > 0:
            s, g = self.keys.pop(), self.data.pop()
            self.keys.appendleft(s)
            self.data.appendleft(g)
            self.key_to_index[s] = 0
            self.max_heapify(0)
        return (sm, gm)

    def insert_key(self, k, d):
        self.keys.append(k)
        self.data.append(-float("inf"))
        self.key_to_index[k] = len(self.keys)-1 #!
        self.increase_key(len(self.keys)-1, d)

    def max_heapify(self, i):
        heap_size = len(self.keys)
        l = i*2 + 1
        r = i*2 + 2
        largest = i
        if l < heap_size and self.data[l] > self.data[i]:
            largest = l
        if r < heap_size and self.data[r] > self.data[largest]:
            largest = r
        if largest != i:
            self.swap(largest, i)
            self.max_heapify(largest)

    def increase_key(self, i, key):
        if key < self.data[i]:
            raise Exception("New key is smaller than current key.")
        self.data[i] = key
        parent = (i-1)/2
        while i > 0 and self.data[i] > self.data[parent]:
            self.swap(i, parent)
            i = parent
            parent = (i-1)/2

    def heapify(self):
        for i in range(len(self.keys)/2)[::-1]:
            self.max_heapify(i)

    # Exchanges the students and GPAs at two indices
    def swap(self, i1, i2):
        self.key_to_index[self.keys[i1]] = i2 #!
        self.key_to_index[self.keys[i2]] = i1 #!
        self.data[i1], self.data[i2] = self.data[i2], self.data[i1]
        self.keys[i1], self.keys[i2] = self.keys[i2], self.keys[i1]

    # modified from https://pymotw.com/2/heapq/
    # Displays the heap as a tree
    def show_tree(self, total_width=60, fill=' '):
        """Pretty-print a tree."""
        output = StringIO.StringIO()
        last_row = -1
        for i, n in enumerate(self.keys):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            towrite = str(n) + " (" + str(self.data[i]) + ")"
            output.write(str(towrite).center(col_width, fill))
            last_row = row
        print output.getvalue()
        print '-' * total_width
        print
        return ""

    ########################################################################
    # The following methods are methods used for testing and may be ignored.
    ########################################################################

    def check_heap_invariant(self):
        n = len(self.data)
        for i in range(n/2):
            parent = self.data[i]
            if parent < self.data[2*i+1]:
                return False
            if 2*i + 2 < n:
                if parent < self.data[2*i+2]:
                    return False
        return True

    def check_student_index(self):
        for s,i in self.key_to_index.iteritems():
            if i >= len(self.keys):
                return False
            if self.keys[i] != s:
                return False
        return True


###################################################################
# Part (b)
#   The implementation of Min_Heap is the same as Max_Heap, but modified
#   to be a min-heap. Please refer to the description for Max_Heap.
###################################################################
class Min_Heap:
    '''
    keys: list of key values
    data: list of data that corresponds to the key values
    student_index: a dictionary that maps students names to their index in the
        list representation of the heap
    '''
    def __init__(self, keys, data):
        assert len(keys) == len(data)
        self.keys = collections.deque(keys)
        self.data = collections.deque(data)
        self.key_to_index = dict(zip(self.keys, range(len(self.keys)))) #!
        self.heapify()

    # TODO
    def min_heap_modify(self, key, data):
        spot = int(self.key_to_index[key])
        if self.data[spot] < data:
            self.data[spot] = data
            self.min_heapify(spot)
        elif self.data[spot] > data:
            self.decrease_key(spot, data)

    def minimum(self):
        return (self.keys[0], self.data[0])

    def extract_min(self):
        if len(self.keys)<1:
            raise Exception("No elements in heap!")
        sm, gm = self.keys.popleft(), self.data.popleft()
        del self.key_to_index[sm]
        if len(self.keys) > 0:
            s, g = self.keys.pop(), self.data.pop()
            self.keys.appendleft(s)
            self.data.appendleft(g)
            self.key_to_index[s] = 0
            self.min_heapify(0)
        return (sm, gm)

    def insert_key(self, k, d):
        self.keys.append(k)
        self.data.append(float("inf"))
        self.key_to_index[k] = len(self.keys)-1 #!
        self.decrease_key(len(self.keys)-1, d)

    def min_heapify(self, i):
        heap_size = len(self.keys)
        l = i*2 + 1
        r = i*2 + 2
        smallest = i
        if l < heap_size and self.data[l] < self.data[i]:
            smallest= l
        if r < heap_size and self.data[r] < self.data[smallest]:
            smallest = r
        if smallest != i:
            self.swap(smallest, i)
            self.min_heapify(smallest)

    def decrease_key(self, i, key):
        if key > self.data[i]:
            raise Exception("New key is larger than current key.")
        self.data[i] = key
        parent = (i-1)/2
        while i > 0 and self.data[i] < self.data[parent]:
            self.swap(i, parent)
            i = parent
            parent = (i-1)/2

    def heapify(self):
        for i in range(len(self.keys)/2)[::-1]:
            self.min_heapify(i)

    # Exchanges the students and GPAs at two indices
    def swap(self, i1, i2):
        self.key_to_index[self.keys[i1]] = i2 #!
        self.key_to_index[self.keys[i2]] = i1 #!
        self.data[i1], self.data[i2] = self.data[i2], self.data[i1]
        self.keys[i1], self.keys[i2] = self.keys[i2], self.keys[i1]

    # modified from https://pymotw.com/2/heapq/
    # Displays the heap as a tree
    def show_tree(self, total_width=60, fill=' '):
        """Pretty-print a tree."""
        output = StringIO.StringIO()
        last_row = -1
        for i, n in enumerate(self.keys):
            if i:
                row = int(math.floor(math.log(i+1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2**row
            col_width = int(math.floor((total_width * 1.0) / columns))
            towrite = str(n) + " (" + str(self.data[i]) + ")"
            output.write(str(towrite).center(col_width, fill))
            last_row = row
        print output.getvalue()
        print '-' * total_width
        print
        return ""

    ########################################################################
    # The following methods are methods used for testing and may be ignored.
    ########################################################################

    def check_heap_invariant(self):
        n = len(self.data)
        for i in range(n/2):
            parent = self.data[i]
            if parent > self.data[2*i+1]:
                return False
            if 2*i + 2 < n:
                if parent > self.data[2*i+2]:
                    return False
        return True

    def check_student_index(self):
        for s,i in self.key_to_index.iteritems():
            if i >= len(self.keys):
                return False
            if self.keys[i] != s:
                return False
        return True