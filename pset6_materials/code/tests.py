
import Gradient_Descent_Template as code
import time

def read_params(number):
    with open(str(number)+'.in','r') as infile:
        x_prelim = infile.readline().rstrip().split(':')
        for i in xrange(len(x_prelim)):
            temp = x_prelim[i].split(",")
            x_prelim[i] = [float(elm) for elm in temp]
        x = x_prelim
        y_prelim = infile.readline().rstrip().split(',')
        y = [float(i) for i in y_prelim]
        theta_prelim = infile.readline().rstrip().split(',')
        theta = [float(i) for i in theta_prelim]
        return x,y,theta

def read_output(number):
    with open(str(number)+".out",'r') as infile:
        check_theta = infile.readline().rstrip().split(",")
        return [float(i) for i in check_theta]

def mse(v,u):
    return sum((v[i] - u[i])**2 for i in xrange(len(v)))/len(v)

def main():
    correct = 0
    for i in xrange(1,16):
        x,y,theta = read_params(i)
        if i < 6:
            step_size = 0.00003
            start = time.clock()
            out_theta = code.gradient_descent(x,y,theta,step_size)
            duration = time.clock() - start
            target = read_output(i)
            print "Gradient Descent Test " + str(i) + "\n"
            if mse(target,out_theta) < 0.01:
                print "Passed. In " + str(duration) + " Seconds. \n"
                correct +=1
            else:
                print "Your answer deviates too much from the expected one. \n"
        elif 5<i and i < 11:
            start = time.clock()
            out_theta = code.gradient_descent_complete(x,y,theta)
            duration = time.clock() - start
            target = read_output(i)
            print "Complete Gradient Test " + str(i) + "\n"
            if mse(target,out_theta) < 0.01:
                print "Passed. In " + str(duration) + " Seconds. \n"
                correct +=1
            else:
                print "Your answer deviates too much from the expected one. \n"

        elif i > 10:
            step_size = 0.00001
            start = time.clock()
            out_theta = code.minibatch_gradient_descent(x,y,theta,step_size)
            duration = time.clock() - start
            target = read_output(i)
            print "Minibatch Gradient Test " + str(i) + "\n"
            if mse(target,out_theta) < 0.01:
                print "Passed. In " + str(duration) + " Seconds. \n"
                correct +=1
            else:
                print "Your answer deviates too much from the expected one. \n"
    print str(correct) + " out of 15 correct!"

if __name__ == "__main__":
    main()
