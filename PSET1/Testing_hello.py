"""This is a test to see if I can use PyCharm"""

import heapq

testing_dict = {}
string_test = 'abcdefghijklmnopqrstuvwxyz'
counter = 0
for i in range(26):
    counter = 1
    testing_dict[string_test[i]] = counter


print testing_dict
bunches =  sorted(testing_dict, key = lambda b: testing_dict[b], reverse=True)
print bunches[:25]
print type(bunches)

