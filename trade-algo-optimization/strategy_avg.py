#Emulating the price average trading strategy in Python.
#Some changes have to be made in order for more efficient strategy evaluation.
import math

from numpy import average

#algo parameters

prices = [1,5,6,2,3,1,4,2,3,1,9,4,8,2,6,2,8,7,6,5,4,9,13,16,17,2,3,9,4]
lastXPrices = 10
minDifferenceUp = 5
minDifferenceDown = 5

#functions

def lastXValues(x, idx):
    '''
    Returns last x price values from given index.
    '''
    return prices[idx-x+1:idx+1]


def avg(array):
    '''
    Returns numeric average of number array.
    '''
    return math.fsum(array)/len(array)


def compareLatestPriceToRelevantValues(idx):
    '''
    Compares latest price value to relevant average.
    Returns difference, positvive price>anverage, negative price<average.
    '''
    relevantValues = lastXValues(lastXPrices, idx)
    latestPrice = relevantValues[-1]
    average = avg(relevantValues)
    return latestPrice - average


def evaluateLatestMovement(idx):
    pass



a = lastXValues(5,4)
print(a, avg(a))
print(compareLatestPriceToRelevantValues(17))