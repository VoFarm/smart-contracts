from api_bitstamp import fetchHistory
from file_handling import saveDict, loadDict, extractHistoricalValues
from strategy_avg import getLastXPrices, getDifferences, setDifferenceUpDown, setLastXPrices, evaluateLatestMovement
from visualizer import drawPlot

#download price history and save
#saveDict(fetchHistory(),'trade-algo-optimization/history.json')
#load price history
priceValues = extractHistoricalValues('close',loadDict('trade-algo-optimization/history.json'))

#smart contract state, stable = True, volatile = False
stableState = True

#token balances
stableToken = 100
volatileToken = 0

#algo optimization params
hodlGain = priceValues[-1]/priceValues[0]
maxGain = (0,)
gainsByVariables = []

#variable test ranges
timeRange = range(1, 8)#2-240
diffRange = range(1, 8)#16-512

def fullSwap(price, recommendation):
    '''
    Fully swaps stable token and volatile token, according to price,
    recommendation and contract state.
    '''
    global stableState
    global stableToken
    global volatileToken
    #execute buy swap
    if stableState and recommendation == 'buy':
        volatileToken = stableToken/price
        stableToken = 0
        stableState = False
    #execute sell swap
    if not stableState and recommendation == 'sell':
        stableToken = volatileToken*price
        volatileToken = 0
        stableState = True


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
    stableToken = 100
    volatileToken = 0
    stableState = True
'''
setLastXPrices(10)
setDifferenceUpDown(239)
for idx in range(getLastXPrices(), len(priceValues)):
    recommendation = evaluateLatestMovement(idx, priceValues)
    fullSwap(priceValues[idx], recommendation)
    print(stableBalance(priceValues[idx]))
gain = stableBalance(priceValues[-1])/100
gainVsHodl = gain/hodlGain
print(gain, gainVsHodl, getLastXPrices(), getDifferences())


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
            #print(stableBalance(priceValues[-idx]),stableToken,volatileToken)
        gain = stableBalance(priceValues[-1])/100
        timeData.append(gain)
        gainVsHodl = gain/hodlGain
        #print(gain, gainVsHodl, getLastXPrices(), getDifferences())
        if(gain>maxGain[0]):
            maxGain = (gain, gainVsHodl, t, d)
            print(maxGain)
    plotData.append(timeData)
drawPlot(plotData)
