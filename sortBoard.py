from datetime import datetime
import time
import pickle
import operator

def sortBoard():

    try:
        with open('scoreBoard.pickle', 'rb') as readDictFile:
            dictFile = pickle.load(readDictFile)
    #if the file is empty declare dictFile = {}
    except EOFError:
        dictFile = {}
        
    sortedBoard = {}
    sortedBoard = sorted(dictFile.items(), key=operator.itemgetter(1))
	
    #return sortedBoard
    with open('sortScoreBoard.pickle', 'wb') as writeDictFile:
            pickle.dump(sortedBoard, writeDictFile)

