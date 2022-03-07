import requests as req
import ast #ast is used here instead of json because bitstamp returns its data as dict

#some very useful standard variables
historyUrl = 'https://www.bitstamp.net/api/v2/ohlc/'
currentValueHeader = {"step":3600,"limit":1}#"step":21600,180,3600,86400
standartTradePair = 'btcusd'#ethusd
standartTimeStep = 3600#21600 180 3600 86400
ethUnixStart = 1502899200 #1644679546 2022-02-12 #1614797285 2021-03-03 UTC    #1502899200 #2017-08-16 16:00 UTC


def fetchValues(tradePair, headerParameters):
    '''
    `tradePair`etheur, btceur, btcusd...

    `headerParameters`{"step":number,"limit":number}

    Returns pair values for given timespan, timestep, tradepair.
    '''
    resp = req.get(historyUrl + tradePair, headerParameters).text
    return ast.literal_eval(resp)


def mergeOHLC(dataListObject, newDataListObject):
    '''
    `dataListObject`Previous data list object.

    `newDataListObject`New data list object to be merged with dataListObject
    
    Merges new data of an OHLC list into an existing OHCL list.
    '''
    dataListObject['data']['ohlc'].extend(newDataListObject['data']['ohlc'])# = dataListObject['data']['ohlc'] + newDataListObject['data']['ohlc']
    return dataListObject


def fetchHistory(tradepair = standartTradePair, start = ethUnixStart, timestep = standartTimeStep):
    '''
    Fetches history of given tradepair from given unix start up to now.
    '''
    header = {"step":timestep,"limit":1000,"start":start}
    history = {"data":{"ohlc":[]}}
    resp = fetchValues(tradepair,header)

    while (len(resp['data']['ohlc']) > 1):
        #merge response into history
        history = mergeOHLC(history,resp)
        #adjust new header start value
        header['start'] = header['start'] + 1000*timestep
        #get next response with new header
        resp = fetchValues(tradepair,header)
        #testing len
        print(len(history['data']['ohlc']),'candlesticks fetched')

    return history

