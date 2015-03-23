from random import randint

def randomWord():
    with open('largeWord.txt', 'r') as largeFile:
        generateNumber = randint(0,53454)
        count=0
        for line in largeFile:
            if generateNumber == count:
                return line.strip()              
            count +=1
