from flask import Flask, render_template, url_for, request, redirect, flash, session
from datetime import datetime
import pickle
import checkWord,sortBoard,generateRandom,addRankBoard,checkRank
import os
import sys

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def display_home():
    return render_template("home.html",the_title="Welcome to word game!",
                           play_url=url_for("playGame"))

#check which submit button did the user click(start game or display Rank board)      
@app.route('/wordGame', methods=["POST"])
def playGame():
    if request.form['submit'] == 'Start Game':
        start()
        return redirect(url_for("inputValue"))
    
    elif request.form['submit'] == 'Rank Board':
        return redirect(url_for("rankBoardDisplay"))

#///////////////////////////////////////////////////////////////////////////////     
#display inputvalue html        
@app.route('/input')
def inputValue():
    return render_template("wordGame.html",the_title="Word Game",
                           random_data = session.get('sourceWord'),
                           take_input_url=url_for("checkInput") )
    
#///////////////////////////////////////////////////////////////////////////////
#check input value and check submit button (next input or retry)
@app.route('/checkInput', methods=["POST"])
def checkInput():
    #take values from html input
    if request.form['submit'] == 'Result':
        
        userInput=[]
        userInput.extend([request.form['input_value'],request.form['input_value2'],
        request.form['input_value3'], request.form['input_value4'],request.form['input_value5'],
        request.form['input_value6'],request.form['input_value7']])

        session['listInput'] = userInput
        return redirect(url_for("scoreBoardDisplay"))
            
    # allow user to retry     
    elif request.form['submit'] == 'Retry':
        start()
        return redirect(url_for("inputValue"))
    elif request.form['submit'] == 'Home Screen':
        return redirect(url_for("display_home"))

#///////////////////////////////////////////////////////////////////////////////
#Diplay User Score Board and check their rank       
@app.route('/result')
def scoreBoardDisplay():
    time = datetime.now() - session.get('timeNow')  #check the time of the user submit
    rank = checkRank.rank(time)                     #use the time and get the rank
    session['timeFinish'] = str(time)
    invalidWord = checkList(session.get('listInput'))   #check for invalid word
    inputList = session.get('listInput')
    session['pass'] = False

    if len(inputList) == 7 and len(invalidWord) == 0:
        session['pass'] = True
        return render_template("scoreBoard.html",the_title="Your Result",time_data = time,
                               rank_data = rank,result_data = invalidWord,
                               list_data = inputList,result_url=url_for("scoreBoard") )
    else:
        session['pass'] = False
        failed = "You failed to join the rank board"
        rank = 0
        return render_template("scoreBoard.html",the_title="Your Result",rank_failed=failed,time_data = time,
                               rank_data = rank,result_data = invalidWord,list_data = inputList,
                               result_url=url_for("scoreBoard") )

#///////////////////////////////////////////////////////////////////////////////
# Check for submit button click   
@app.route('/top10', methods=["POST"])
def scoreBoard():
    if session.get('pass') == False and request.form['submit'] == 'Add To Rank':
        flash("You need all 7 valid words to join the rank board")
        return redirect(url_for("scoreBoardDisplay"))
    elif request.form['submit'] == 'Add To Rank' and request.form['user_name'] == '':
        flash("Please enter your name for the Rank Board")
        return redirect(url_for("scoreBoardDisplay"))
    
    elif request.form['submit'] == 'Add To Rank' and request.form['user_name'] != '':
        #add the user to rank board
        username = {request.form['user_name'] : session.get('timeFinish')}
        addRankBoard.rank(username)
        return redirect(url_for("rankBoardDisplay"))
    
    elif request.form['submit'] == 'Play Again':
        start()
        return redirect(url_for("inputValue"))
    
    elif request.form['submit'] == 'Home Screen':
        return redirect(url_for("display_home"))

#///////////////////////////////////////////////////////////////////////////////
#display Rank Board             
@app.route('/rankBoardDisplay')
def rankBoardDisplay():
    rankBoard = getScoreBoard()
    return render_template("rankBoard.html",the_title="Rank Board",
                           rankBoard_data = rankBoard,rank_Board_url=url_for("rankBoard") )

#///////////////////////////////////////////////////////////////////////////////
#Check for Rank Board button click            
@app.route('/rankBoard', methods=["POST"])
def rankBoard():
    session.clear()
    # allow user to play    
    if request.form['submit'] == 'Play':
        start()
        return redirect(url_for("inputValue"))
    
    elif request.form['submit'] == 'Home Screen':
        return redirect(url_for("display_home"))

#///////////////////////////////////////////////////////////////////////////////
#return list of bad word if it not in the dictionary and source word        
def getScoreBoard():
    sortBoard.sortBoard()
    try:
        with open('sortScoreBoard.pickle', 'rb') as readDictFile:
            dictFile = pickle.load(readDictFile)
            
    except EOFError:
        dictFile = {}
         
    return dictFile

#///////////////////////////////////////////////////////////////////////////////
#return list of bad word if it not in the dictionary       
def checkList(userList):
    duplicationList = checkDuplication(userList) # check the list of Ducplication
    badList = []
    count = 0
    for i in userList:
        check = True
        count += 1
        #check the input word is a valid word
        if i == session.get('sourceWord'):
            badList.append(i + " (line " + str(count) + " same as source word)")   
        elif checkWord.exist(i,session.get('sourceWord')) == False and len(i) > 2 and len(i) <= len(session.get('sourceWord')):
            badList.append(i + " (line " + str(count) + " Not in dictionary)")
            check = False
        elif i == '':
            badList.append("(line " + str(count) + " No Word Enter)")
        elif len(i) <= 2:
            badList.append(i + " (line " + str(count) + " require more letters)")
        elif len(i) > len(session.get('sourceWord')):
            badList.append(i + " (line " + str(count) + " Too many Letters)")
        elif duplicationList[count-1] == "True" and check:
            badList.append( i + " (line " + str(count) + " Duplication)")
        
    return badList

#///////////////////////////////////////////////////////////////////////////////
#create session for start time and create a word
def checkDuplication(userList):
    userSet = set(userList)
    myList = []
    for line in userList:
        if line in userSet:
            userSet = [x for x in userSet if x != line]
            myList.append('False')
        else:
            myList.append('True')
    
    return myList
    
#///////////////////////////////////////////////////////////////////////////////
#create session for start time and create a word
def start():
    session['sourceWord'] = generateRandom.randomWord()
    session['timeNow'] = datetime.now()
    
app.config['SECRET_KEY'] = 'thisismysecretkeywhichyouwillneverguesshahahahahahahaha'                            

if __name__ == '__main__':
    app.run(debug=True)
