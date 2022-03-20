#This strategy has not yet been implemented in Solidity.
#It is an variation of strategy_avg.
#This is just for testing purposes
from math import fsum

#algo parameters

lastXPrices = 0
minDifferenceUp = 0
minDifferenceDown = 0

#functions

def lastXValues(x, idx, priceValues):
    '''
    Returns last x price values from given index.
    '''
    return priceValues[idx-x+1:idx+1]


def avg(array):
    '''
    Returns numeric average of number array.
    '''
    return fsum(array)/len(array)


def compareLatestPriceToRelevantValues(idx, priceValues):
    '''
    Compares latest price value to relevant average.
    Returns difference, positvive price>anverage, negative price<average.
    '''
    relevantValues = lastXValues(lastXPrices, idx, priceValues)
    latestPrice = relevantValues[-1]
    average = avg(relevantValues)
    return latestPrice/average


def evaluateLatestMovement(idx, priceValues)->str:
    changed = compareLatestPriceToRelevantValues(idx, priceValues) -1
    if changed > minDifferenceUp:
        #price has gone up, indicate sell
        return 'sell'#sell
    else:
        if changed < minDifferenceDown:
            #price has gone down, indicate buy
            return 'buy'#buy
        else:
            #cannot indicate anything, hold
            return 'hold'


#getter and setter functions
def getLastXPrices():
    return lastXPrices

def getDifferences():
    return (minDifferenceUp, minDifferenceDown)

def setLastXPrices(x):
    global lastXPrices
    lastXPrices = x


def setDifferenceUpDown(absDiff,divisor=1000):
    global minDifferenceDown
    global minDifferenceUp
    minDifferenceUp = absDiff/divisor
    minDifferenceDown = -absDiff/divisor