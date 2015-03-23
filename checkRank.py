from datetime import datetime
import pickle

#check what rank the user are
def rank(timeFinish):
    try:
        with open('sortScoreBoard.pickle', 'rb') as readScoreFile:
            scoreBoard = pickle.load(readScoreFile)
    #if the file is empty declare dictFile = {}
    except EOFError:
        scoreBoard = {}
        
    rank = 0
    for key, value in scoreBoard:
        rank +=1
        time = str(timeFinish)
        if datetime.strptime(time,'%H:%M:%S.%f').time() < datetime.strptime(value, '%H:%M:%S.%f').time():
            return rank
    else:
        return rank+1
