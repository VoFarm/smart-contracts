from api_bitstamp import fetchHistory
from file_handling import saveDict, loadDict, extractHistoricalValues

#download price history and save
#saveDict(fetchHistory(),'history.json')
#load price history
historicalValues = extractHistoricalValues('close',loadDict('history.json'))
print(historicalValues, len(historicalValues))