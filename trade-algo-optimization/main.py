from api_bitstamp import fetchHistory
from file_handling import saveDict, loadDict, extractHistoricalValues
from strategy_avg import lastXPrices, setDifferenceUpDown, setLastXPrices, evaluateLatestMovement

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
timeRange = range(10, 1440)
diffRange = range(20, 800)

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


def resetBalances():
    global stableToken
    global volatileToken
    stableToken = 100
    volatileToken = 0

'''
for idx in range(lastXPrices, len(priceValues)):
    latestPrice = priceValues[idx]
    recommendation = evaluateLatestMovement(idx, priceValues)
    fullSwap(latestPrice, recommendation)
    #print(latestPrice, recommendation, stableBalance(latestPrice))'
'''


for t in timeRange:
    setLastXPrices(t)
    for d in diffRange:
        setDifferenceUpDown(d)
        resetBalances()
        for idx in range(lastXPrices, len(priceValues)):
            recommendation = evaluateLatestMovement(idx, priceValues)
            fullSwap(priceValues[idx], recommendation)
        gain = stableBalance(priceValues[-1])/100
        gainVsHodl = gain/hodlGain
        if(gain>maxGain[0]):
            maxGain = (gain, gainVsHodl, t, d)
            print(maxGain)
