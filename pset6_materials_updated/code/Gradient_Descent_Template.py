#!/usr/bin/python

import random

##################################################################
###################### Testing Tools #############################
##################################################################

'''
Generates inputs for gradient descent.
Inputs:
    voters: the number of voters, or n from the pdf
    demographic: number of demographic info.
    error: How well our model will fit the data. Below 10 and its pretty good. Above 50 it's pretty bad.
Output:
    Theta:      n by m matrix from pdf
    Y:          length n vector of preferences
    true_x:     x from which we generated Y. If error is low, this will be quite close to optimal.
                When testing, you should check if the final x you get has a low mean_square_diff with this
    initial_x:  perturbed version of true_x. Useful starting point
'''
# Uncomment the block below to generate random parameters. When you submit, comment it out again: You won't be able
# to use numpy on alg.
'''
import numpy as np
def generate_parameters(voters,demographic,error):

    #Randomly generate true params Theta, true_x, and Y
    Theta = 100*np.random.rand(voters,demographic)
    true_x = 10*np.random.rand(1,demographic) - 5
    Y = Theta.dot(true_x.transpose())
    Y = Y.transpose()
    Y = Y + np.random.normal(scale=error,size=voters)

    #Perturb the true x to get something close
    scaling = 0.5*np.ones((1,demographic))+np.random.rand(1,demographic)
    initial_x = np.multiply(true_x,scaling)

    #Somewhat hacky way to convert away from np arrays to lists
    Theta = Theta.tolist()
    Y = [Y[0][i] for i in xrange(voters)]
    true_x = [true_x[0][i] for i in xrange(demographic)]
    initial_x = [initial_x[0][i] for i in xrange(demographic)]

    return Theta,Y,true_x,initial_x
'''

'''
This function is used by the tests and may be useful to use when calculating whether you should stop
This function takes two vectors as input and computes the mean of their squared error
Inputs:
  v1, a length k vector
  v2, a length k vector
Output:
  mse, a float for their mean-squared error
'''
def mean_square_diff(v1,v2):
    diff_vector = [v1[i]-v2[i] for i in xrange(len(v1))]
    mse = 1.0/len(v1)*sum(difference**2 for difference in diff_vector)
    return mse


##################################################################
#################### Part B: Gradient Descent ####################
##################################################################

# GRADIENT DESCENT SPECIFICS
# The stopping condition is given below, namely, when the mean squared diff of the x's
# between iterations is less than some constant. Note, this is not the mean squared diff
# of f(x) but of the vector x itself! For instance
#    x_at_iteration_k = [1,2,4,5]
#    x_at_iteration_k+1 = [1,4,2,6]
#    mean_square_change = mean_square_diff(x_at_iteration_k,x_at_iteration_k+1)

'''
Compute a 'sufficiently close to optimal' x using gradient descent
Inputs:
  Theta - The voting Data as a n by m array
  Y - The favorabilty scores of the voters
  initial_x - An initial guess for the optimal parameters provided to you
  eta - The learning rate which will be given to you.
Output:
  nearly optimal x.
'''
def find_gradient(Theta,Y,X):
    n,m = len(Theta),len(Theta[0])
    s = [0 for i in xrange(m)]
    for i in range(n):
        #print Theta[i]
        #print X
        #print (dot(Theta[i],X))
        new_s = scalar(Theta[i],(dot(Theta[i],X)*-1)+Y[i]) #scalar(scalar(Theta[i], -1),(Y[i] - dot(Theta[i],X)))
        #return new_s
        for j in range(len(new_s)):
            s[j] = s[j] + new_s[j]

    return scalar(s, -2.0/n)


def gradient_descent(Theta, Y, initial_x, eta):
    #We've initialized some variables for you
    n,m = len(Theta),len(Theta[0])
    current_x = initial_x
    mean_square_change = 1
    while mean_square_change > 0.0000000001:
        old_x = current_x
        current_x = add_vectors(old_x, scalar(find_gradient(Theta,Y,old_x), (-1 * eta)))
        mean_square_change = mean_square_diff(current_x, old_x)
    #print current_x
    return current_x

def add_vectors(X,Y):
    n = len(X)
    Ans = []
    for i in range(n):
        Z = X[i] + Y[i]
        Ans.append(Z)
    return Ans

def scalar(X,c):
    size= len(X)
    Z = []
    for i in range(size):
         Z.append(X[i]*c)
    return Z


def dot(X,Y):
    size = len(X)
    total = 0
    for i in range(size):
        total += X[i] * Y[i]
        #print X[i], Y[i]
        #print total
    return total

##################################################################
############### Part C: Minibatch Gradient Descent################
##################################################################

################################## ALGORITHM OVERVIEW ###########################################
# Very similar to above but now we are going to take a subset of 10                             #
# voters on which to perform our gradient update. We could pick a random set of 10 each time    #
# but we're going to do this semi-randomly as follows:                                          #
#   -Generate a random permutation of [0,1...,n] (say, [5,11,2,8 . . .])                        #
#    This permutation allows us to choose a subset of 10 voters to focus on.                    #
#   -Have a sliding window of 10 that chooses the first 10 elements in the permutation          #
#    then the next 10 and so on, cycling once we reach the end of this permutation              #
#   -For each group of ten, we perform a subgradient update on x.                               #
#    You can derive this from the J(x)^mini                                                     #
#   -Lastly, we only update our stopping condition, mean_square_change                          #
#    when we iterate through all n voters. Counter keeps track of this.                         #
#################################################################################################

'''
Minibatch Gradient Descent
Compute a 'sufficiently close to optimal' x using gradient descent with small batches
Inputs:
  Theta - The voting Data as a n by m array
  Y - The favorabilty scores of the voters
  initial_x - An initial guess for the optimal parameters provided to you
  eta - The learning rate which will be given to you.
Output:
  nearly optimal x.
'''

def minibatch_find_gradient(Theta,Y,X,selected):
    n,m = len(Theta),len(Theta[0])
    s = [0 for i in xrange(m)]
    for i in selected:
        new_s = scalar(Theta[i],(dot(Theta[i],X)*-1)+Y[i]) #scalar(scalar(Theta[i], -1),(Y[i] - dot(Theta[i],X)))
        for j in range(len(new_s)):
            s[j] = s[j] + new_s[j]
    return scalar(s, -2.0/10)

def minibatch_gradient_descent(Theta, Y, initial_x, eta):
    # We've gotten you started. Voter_ordering is a random permutation.
    # Window position can be used to keep track of the sliding window's position
    n,m = len(Theta),len(Theta[0])
    current_x = initial_x
    voter_ordering = range(n)
    random.shuffle(voter_ordering)
    mean_square_change = 1
    window_position = 0
    counter = 0
    while mean_square_change > 0.000000001:
        #TODO: Minibatch updates

        old_x = current_x
        selected = voter_ordering[window_position: window_position+10]
        current_x = add_vectors(old_x, scalar(minibatch_find_gradient(Theta,Y,old_x, selected), (-1 * eta)))
        counter+=1
        window_position = (window_position + 10)

        if counter == n/10:
            # TODO: stopping condition updates
            mean_square_change = mean_square_diff(current_x, old_x)
            counter = 0
        #Remove this when you actually fill this out
#        mean_square_change = 0
    return current_x

##################################################################
############## Part D: Line search Gradient Descent###############
##################################################################


'''
Compute the mean-squared error between the prediction for Y given Theta and the current parameters x
and the actual voter desires, Y.
Input:
  Theta - The voting Data as a n by m array
  Y - The favorabilty scores of the voters. Length n.
  x - The current guess for the optimal parameters. Length m.
Output:
  A float for the prediction error.
'''
def prediction_error(Theta,Y,x):
    prediction_error = float('inf')
    #TODO Compute the MSE between the prediction and Y
    prediction = []
    for k in range(len(Theta)):
        prediction.append(dot(Theta[k], x))
    prediction_error = mean_square_diff(prediction, Y)
    return prediction_error

'''
This function should return the next current_x after doubling the learning rate
until we hit the max or the prediction error increases
Inputs:
    current_x   Current guess for x. Length m.
    gradient    Gradient of current_x. Length m.
    min_rate    Fixed given rate.
    max_rate    Fixed max rate.
Output:
    updated_x   Check pseudocode.
'''
def J(X, Theta, Y):
    n = len(Theta)
    ans = 0
    for i in range(n):
        ans += (Y[i] - dot(Theta[i],X))**2
    return float(ans)/n

def line_search(Theta,Y,start_x,gradient,min_rate=0.0000001,max_rate=0.1):
    #TODO Adapt the pseudocode to working python code
    n_current = min_rate
    current_x = add_vectors(start_x, scalar(gradient, -n_current))
    while n_current < max_rate:
        x_temp = add_vectors(current_x, scalar(gradient, -n_current))
        if J(x_temp, Theta, Y) < J(current_x, Theta, Y):
            current_x = x_temp
            n_current  *= 2
        else:
            break
    return current_x


'''
Inputs:
  Theta  The voting Data as a n by m array
  Y      The favorabilty scores of the voters. Length n.
  x      The current guess for the optimal parameters. Length m.
Output:
  gradient Length m vector of the gradient.
'''
def compute_gradient(Theta,Y,current_x):
    #TODO: Compute the gradient. Should be able to copy paste from part b.
    X = current_x
    n,m = len(Theta),len(Theta[0])
    s = [0 for i in xrange(m)]
    for i in range(n):
        #print Theta[i]
        #print X
        #print (dot(Theta[i],X))
        new_s = scalar(Theta[i],(dot(Theta[i],X)*-1)+Y[i]) #scalar(scalar(Theta[i], -1),(Y[i] - dot(Theta[i],X)))
        #return new_s
        for j in range(len(new_s)):
            s[j] = s[j] + new_s[j]

    return scalar(s, -2.0/n)

    #return current_x


def gradient_descent_complete(Theta,Y,initial_x):
    n,m = len(Theta),len(Theta[0])
    delta = 1
    current_x = initial_x
    last_error = prediction_error(Theta,Y,current_x)
    while delta > 0.1:
        gradient = compute_gradient(Theta,Y,current_x)
        current_x = line_search(Theta,Y,current_x,gradient,0.0000005,0.1)
        current_error = prediction_error(Theta,Y,current_x)
        delta = last_error - current_error
        last_error = current_error


    return current_x