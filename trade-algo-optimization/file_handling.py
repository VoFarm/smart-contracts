#file handler
from ctypes.wintypes import HLOCAL
import json #json can be used to load json data as dict and save dict as json, no ast needed here
import ast #for converting strings to numbers


def loadFile(path):
    f = open(path,'r')
    contents = f.read()
    f.close()
    print('loading',path)
    return contents


def saveFile(data,path):
    f = open(path, "w")
    f.write(data)
    f.close()
    print('saved',path)


def loadDict(jsonPath):
    '''
    Loads dict from a .json file.
    '''
    filestring = loadFile(jsonPath)
    return json.loads(filestring)#ast.literal_eval(filestring)


def saveDict(dictData,jsonPath):
    '''
    Saves dict as .json file at given path.
    '''
    jsonString = json.dumps(dictData)
    saveFile(jsonString,jsonPath)



def extractHistoricalValues(valueType,historicalDict):
    '''
    Extracts certain values from entire history, returns list of numbers.
    valueType: "high","timestamp","volume","low","close","open"
    historicalDict: ohlc dictionary including all historical candlesticks
    '''
    values = [ast.literal_eval(x[valueType]) for x in historicalDict['data']['ohlc']]
    return values


def saveAnalysis(analysisResult, timeRangeStart, timeRangeEnd, diffRangeStart, diffRangeEnd, hodlGain, jsonPath):
    '''Saves backtest analysis.'''
    saveDict(
        {
            'analysisResult':analysisResult,
            'timeRangeStart':timeRangeStart,
            'timeRangeEnd':timeRangeEnd,
            'diffRangeStart':diffRangeStart,
            'diffRangeEnd':diffRangeEnd,
            'hodlGain':hodlGain,
        },
        jsonPath
    )
