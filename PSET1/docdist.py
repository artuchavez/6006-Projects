#!/usr/bin/python

import string
import sys
import math
import heapq
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = string.maketrans(string.punctuation+string.uppercase[0:26],
                                     " "*len(string.punctuation)+string.lowercase[0:26])

def extract_words(filename):
    """
    Return a list of words from a file
    """
    try:
        f = open(filename, 'r')
        doc = f.read()
        lines = doc.translate(translation_table)
        return lines.split()
    except IOError:
        print "Error opening or reading input file: ",filename
        sys.exit()

##############################################
## Part a. Count the frequency of each word ##
##############################################
def count_frequencies(extracted_words):
    """
    :param extracted_words: the a list of the words in a document
    :return: a dictionary with the word as the key and the number of occurences as the value
    """
    word_record = {}
    for elt in extracted_words:
        if elt in word_record:
            word_record[elt] += 1
        else:
            word_record[elt] = 1
    return word_record

def find_theta(dict1, dict2):
    """
    :param dict1: output of count_frequencies for document 1
    :param dict2: output of count_frequencies for document 2
    :return: the angle between the two vectors
    """
    final_dot_prod = 0
    mag_1 = 0
    mag_2 = 0
    keys_of_1 = dict1.keys()
    keys_of_2 = dict2.keys()
    common_keys = []
    for i in keys_of_1:
        mag_1 += (dict1[i])**2
        if i in keys_of_2:
            common_keys.append(i)
    for elt in common_keys:
        dot_calc = dict1[elt] * dict2[elt]
        final_dot_prod += dot_calc
    for k in keys_of_2:
        mag_2 += (dict2[k])**2
    mag_1 = math.sqrt(mag_1)
    mag_2 = math.sqrt(mag_2)
    print mag_1
    print mag_2
    theta = math.acos(final_dot_prod / (mag_1 * mag_2))
    return theta



def doc_dist(word_list1, word_list2):
    """
    Returns a float representing the document distance 
    in radians between two files when given the list of
    words from both files
    """
    first_dict = count_frequencies(word_list1)
    second_dict = count_frequencies(word_list2)
    distance = find_theta(first_dict,second_dict)
    return distance

##############################################
## Part b. Count the frequency of each pair ##
##############################################
def count_word_pairs(word_list):
    """
    :param word_list: list of words in doc
    :return: dictionary with pairs of words as key and # occurences as value
    """
    word_record = {}
    num_words = len(word_list)
    for i in range(num_words-1):
        pair = word_list[i] + ' ' + word_list[i+1]
        if pair in word_record:
            word_record[pair] += 1
        else:
            word_record[pair] = 1
    return word_record

def doc_dist_pairs(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on unique 
    consecutive pairs of words when given the list of
    words from both files
    """
    first_dict = count_word_pairs(word_list1)
    second_dict = count_word_pairs(word_list2)
    distance = find_theta(first_dict,second_dict)
    return distance

#############################################################
## Part c. Count the frequency of the 50 most common words ##
#############################################################


def find_top_fifty(word_freq_dict):
    """
    :param word_list: a list of tuples with occurences
    :return: dictionary with the word as key and # occurences as values
    """
    sorted_key_list = sorted(word_freq_dict, key = lambda b: word_freq_dict[b], reverse=True)
    top_50 = {}
    for elt in sorted_key_list[:50]:
        top_50[elt] = word_freq_dict[elt]
    return top_50

"""

    list_1 = word_freq_dict.items()
    print list_1
    print type(list_1)
    magic_heap = heapq._heapify_max(list_1)
    important_elements = {}
    counter = 0
    while counter <= 50:
        top_selection = heapq.heappop(magic_heap)
        important_elements[top_selection[0]] = top_selection[1]
    return important_elements
"""

def doc_dist_50(word_list1, word_list2):
    """
    Returns a float representing the document distance
    in radians between two files based on the 
    50 most common unique words when given the list of
    words from both files
    """
    whole_dict1 = count_frequencies(word_list1)
    whole_dict2 = count_frequencies(word_list2)
    top_fifty1 = find_top_fifty(whole_dict1)
    top_fifty2 = find_top_fifty(whole_dict2)
    distance = find_theta(top_fifty1,top_fifty2)
    return distance

# play3 = extract_words("/Users/achavezg/PycharmProjects/6.006/PSET1/plays/pirates_of_penzance.txt")
# play1 = extract_words("/Users/achavezg/PycharmProjects/6.006/PSET1/plays/henry_iv_1.txt")
# play2 = extract_words("/Users/achavezg/PycharmProjects/6.006/PSET1/plays/henry_iv_2.txt")
# play4 = extract_words('/Users/achavezg/PycharmProjects/6.006/PSET1/plays/tempest.txt')
# first_comp = doc_dist_50(play1,play2), doc_dist_pairs(play1,play2), doc_dist(play1,play2)
# second_comp = doc_dist_50(play1,play3), doc_dist_pairs(play1,play3), doc_dist(play1,play3)
# third_comp = doc_dist_50(play1,play4), doc_dist_pairs(play1,play4), doc_dist(play1,play4)
# print first_comp
# print second_comp
# print third_comp

print doc_dist_50(extract_words('henry_iv_1.txt'), extract_words(('henry_iv_2.txt')))


