from cProfile import label
import math
from turtle import color
import matplotlib.pyplot as plt
import numpy as np

#a = np.random.random((30, 16))


def drawHeatMapPlot(arrayOfArrays,title=''):
    (vmin, vmax) = _vminVmax(arrayOfArrays)
    plt.imshow(arrayOfArrays,cmap='inferno', interpolation='none', vmin=vmin, vmax=vmax)
    plt.colorbar()
    plt.xlabel('difference')
    plt.ylabel('time')
    plt.title(title)
    plt.show()


def drawAreaMap(arrayOfArrays, hodlGain, title=''):
    colorParameters = {#color parameters adjustet for cmap=Set1
        'uw': 8,   #unprofitable, worse than hodling
        'ub':1,    #unprofitable, better than hodling
        'pw':2,    #profitable, worse than hodling
        'pb':0     #profitable, better than hodling
    }
    arrayOfArrays = _adjustForAreaMap(arrayOfArrays, hodlGain, colorParameters)
    plt.imshow(arrayOfArrays,cmap='Set1', interpolation='none', vmin=0, vmax=9)
    #plt.colorbar()
    plt.xlabel('difference')
    plt.ylabel('time')
    plt.title(title)
    plt.show()


def _adjustForAreaMap(arrayOfArrays, hodlGain, colorParameters):
    for array in arrayOfArrays:
        for i in range(len(array)):
            if hodlGain > 1:
                if array[i]>hodlGain:
                    array[i] = colorParameters['pb']
                else:
                    if array[i]>1:
                        array[i] = colorParameters['pw']
                    else:
                        array[i] = colorParameters['uw']
            else:
                if array[i]>hodlGain:
                    if array[i]>1:
                        array[i] = colorParameters['pb']
                    else:
                        array[i] = colorParameters['ub']
                else:
                    array[i] = colorParameters['uw']
    return arrayOfArrays


def _vminVmax(arrayOfArrays):
    vmin = math.inf
    vmax = 0
    for a in arrayOfArrays:
        localMin = min(a)
        localMax = max(a)
        if localMin < vmin:
            vmin = localMin
        if localMax > vmax:
            vmax = localMax
    return (vmin, vmax)


def drawPortfolioProgress(priceValues, portfolioValues, swaps=None):
    #plt.plot(priceValues)
    #plt.plot(portfolioValues)
    #if swaps:
    #    [plt.axvline(x=s) for s in swaps]
    #plt.show()
    figure, axis_1 = plt.subplots()
    axis_1.plot(priceValues, color='green')
    axis_2 = axis_1.twinx()
    axis_2.plot(portfolioValues, color='orange')
    if swaps:
        [plt.axvline(x=s) for s in swaps]
    plt.show()

