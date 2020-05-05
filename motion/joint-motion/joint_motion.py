import numpy as np
import math
import time
import matplotlib.pyplot as plt
import tkinter as tk
# ax = plt.axes()
fig = plt.figure(num="Result")
ax = fig.add_subplot(111, aspect='equal', autoscale_on=True)

def initVectors(radii):
    vectors = []
    for r in radii:
        vectors.append([r, 0])
    return vectors

def calcCost(radii, angles):
    return True

def calcTip(tail, radius, theta):
    x = tail[0] + radius * math.cos(theta)
    y = tail[1] + radius * math.sin(theta)
    return [x, y]

'''
calculates the vector sum of multiple vectors
@param vectors - all the vectors to be summed, in the following format:
    [[r0, theta0], [r1, theta1], ...]
'''
def vectorSum(vectors):
    tail = [0, 0]
    for v in vectors:
        tail = calcTip(tail, v[0], v[1])
    return np.array([round(tail[0],3), round(tail[1],3)])

''' draws all vectors passed in, tip to tail '''
def draw(vectors):
    tail = [0, 0]
    for v in vectors:
        tip = calcTip(tail, v[0], v[1])
        dx = tip[0] - tail[0]
        dy = tip[1] - tail[1]
        ax.arrow(tail[0], tail[1], dx, dy, shape='full', head_starts_at_zero=True, width=0.005)
        # ax.arrow(tail[0], tail[1], dx, dy)
        tail = tip

def getMagnitude(vector):
    total = 0
    for i in vector:
        total = total + i**2
    return math.pow(total, 1/len(vector))

''' 
returns the positions of all vectors that minimizes the error
@param dest - the 2D point that the vectors are trying to reach
@param iterations - the number of times to try
@param vectors - the vectors to sum to dest
'''
def goToMagnitude(dest, iterations, vectors, animationMode, maxLength, errorHistory):
    theta = 0
    leastError = getMagnitude(vectorSum(vectors) - dest)
    bestTheta = theta
    step = math.pi/2

    for i in range(iterations):
        for n in range(len(vectors)):
            bestTheta = vectors[n][1]
            theta = bestTheta - step * 2            
            upperLimit = bestTheta + step * 2
            while (theta < upperLimit):
                vectors[n][1] = theta
                end = vectorSum(vectors)
                error = getMagnitude(end - dest)
                if (error < leastError):
                    leastError = error
                    bestTheta = theta
                theta = theta + step
                if (animationMode == True):
                    # animation
                    plt.xlim(-1.1*maxLength, 1.1*maxLength)
                    plt.ylim(-1.1*maxLength, 1.1*maxLength)
                    plt.grid(alpha = 0.25)
                    plt.scatter(dest[0], dest[1])
                    draw(vectors)
                    plt.pause(0.00001)
                    plt.cla()
            vectors[n][1] = bestTheta
            leastError = getMagnitude(vectorSum(vectors) - dest)
        try:
            # scale the step by the ratio of current error to previous error (make step smaller as error decreases)
            stepScaleFactor = (leastError / errorHistory[1][i-1])
        except IndexError:
            # default step scaling factor
            stepScaleFactor = 0.5
        except ZeroDivisionError:
            # if the previous error is already 0, there is no need to go through all the iterations
            return vectors
        if (stepScaleFactor == 1):
            stepScaleFactor = 0.5
        step = step * stepScaleFactor
        errorHistory[0].append(i)
        errorHistory[1].append(leastError)

    return vectors

def calculate(destination, vectorLengths, animationMode, iterations):
    # destination = np.array([10, 10])
    errorHistory = [[], []]
    vectors = initVectors(vectorLengths)
    maxLength = np.sum(vectors, axis=0)[0]
    print(vectors)
    print("animation:", animationMode)

    iterations = 50
    result = goToMagnitude(destination, iterations, vectors, animationMode, maxLength, errorHistory)
    print("result:", result)
    print("least error:", errorHistory[1][-1])

    plt.xlim(-1.1*maxLength, 1.1*maxLength)
    plt.ylim(-1.1*maxLength, 1.1*maxLength)
    plt.grid(alpha = 0.25)
    plt.plot(0, 0, 'ko')
    plt.scatter(destination[0], destination[1])
    draw(result)

    plt.figure(num="Iterations vs Error")
    plt.plot(errorHistory[0], errorHistory[1])

    plt.show()