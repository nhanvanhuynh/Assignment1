from datetime import datetime
import time
import pickle

def rank(currentDict):

    try:
        with open('scoreBoard.pickle', 'rb') as readDictFile:
            dictFile = pickle.load(readDictFile)
            
    except EOFError:
        dictFile = {}
    
    newDict = dict(list(currentDict.items()) + list(dictFile.items()))

    with open('scoreBoard.pickle', 'wb') as writeDictFile:
         pickle.dump(newDict, writeDictFile)

