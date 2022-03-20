from api_bitstamp import fetchHistory
from file_handling import saveDict, loadDict, extractHistoricalValues, saveAnalysis
from strategy_avg import getLastXPrices, getDifferences, setDifferenceUpDown, setLastXPrices, evaluateLatestMovement #strategy_avg 
from visualizer import drawHeatMapPlot, drawAreaMap, drawPortfolioProgress

#download price history and save
#saveDict(fetchHistory(),'trade-algo-optimization/history.json')
#load price history
priceValues = extractHistoricalValues('close',loadDict('trade-algo-optimization/historyHourly.json'))

#smart contract state, stable = True, volatile = False
stableState = True

#token balances
defaultValue = 100
stableToken = defaultValue
volatileToken = 0

#algo optimization params
hodlGain = priceValues[-1]/priceValues[0]
maxGain = (0,)
gainsByVariables = []

#variable test ranges
timeRangeStart = 2
timeRangeEnd = 168
diffRangeStart = 8
diffRangeEnd = 386
timeRange = range(timeRangeStart, timeRangeEnd+1)
diffRange = range(diffRangeStart, diffRangeEnd+1)

def fullSwap(price, recommendation)->bool:
    '''
    Fully swaps stable token and volatile token, according to price,
    recommendation and contract state.
    Returns wether or not a swap has been executed.
    '''
    global stableState
    global stableToken
    global volatileToken
    #execute buy swap
    if stableState and recommendation == 'buy':
        volatileToken = stableToken/price
        stableToken = 0
        stableState = False
        return True
    #execute sell swap
    if not stableState and recommendation == 'sell':
        stableToken = volatileToken*price
        volatileToken = 0
        stableState = True
        return True
    #did not execute swap
    return False


def stableBalance(price):
    '''
    Returns contract balance measured in stable token, no matter the contract state.
    '''
    if(stableState):
        return stableToken
    else:
        return volatileToken*price


def resetAlgorithm():
    global stableToken
    global volatileToken
    global stableState
    stableToken = defaultValue
    volatileToken = 0
    stableState = True

def singleBacktest(timeValue, differenceValue, priceValues):
    portfolioProgress = []
    swaps = []
    resetAlgorithm()
    setLastXPrices(timeValue)
    setDifferenceUpDown(differenceValue)
    for idx in range(getLastXPrices(), len(priceValues)):
        recommendation = evaluateLatestMovement(idx, priceValues)
        swap = fullSwap(priceValues[idx], recommendation)
        if swap:
            swaps.append(idx)
        portfolioProgress.append(stableBalance(priceValues[idx]))
    gain = stableBalance(priceValues[-1])/defaultValue
    return portfolioProgress, swaps, gain

'''
plotData = []
for t in timeRange:
    print(t)
    setLastXPrices(t)
    timeData = []
    for d in diffRange:
        setDifferenceUpDown(d)
        resetAlgorithm()
        for idx in range(getLastXPrices(), len(priceValues)):
            recommendation = evaluateLatestMovement(idx, priceValues)
            fullSwap(priceValues[idx], recommendation)
        gain = stableBalance(priceValues[-1])/defaultValue
        timeData.append(gain)
        gainVsHodl = gain/hodlGain
        if(gain>maxGain[0]):
            maxGain = (gain, gainVsHodl, t, d)
            print(maxGain)
    plotData.append(timeData)
'''


#saveAnalysis(plotData, timeRangeStart, timeRangeEnd, diffRangeStart, diffRangeEnd, hodlGain, 'bogustest.json')
analysisFromSave = loadDict('backtest3Minutely.json')
drawHeatMapPlot(analysisFromSave['analysisResult'])
drawAreaMap(analysisFromSave['analysisResult'],analysisFromSave['hodlGain'])
(progress, swaps, gn) = singleBacktest(17,198,priceValues)
print(len(swaps),progress[-1]/progress[0],priceValues[-1]/priceValues[0])
drawPortfolioProgress(priceValues, progress)
