from api_bitstamp import fetchHistory
from file_handling import saveDict, loadDict, extractHistoricalValues
from strategy_avg import lastXPrices, minDifferenceDown, minDifferenceUp, evaluateLatestMovement

#download price history and save
#saveDict(fetchHistory(),'trade-algo-optimization/history.json')
#load price history
priceValues = extractHistoricalValues('close',loadDict('trade-algo-optimization/history.json'))

#smart contract state, stable = True, volatile = False
stableState = True

#token balances
stableToken = 100
volatileToken = 0


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


for idx in range(lastXPrices, len(priceValues)):
    latestPrice = priceValues[idx]
    recommendation = evaluateLatestMovement(idx, priceValues)
    fullSwap(latestPrice, recommendation)
    print(latestPrice, recommendation, stableBalance(latestPrice))

        
    