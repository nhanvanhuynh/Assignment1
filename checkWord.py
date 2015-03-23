def freq_count(letters):

    f_count = {}
    for char in letters:
        f_count.setdefault(char, 0)
        f_count[char] += 1
    return f_count

def exist(word,sourceWord):

    sc = freq_count(sourceWord.lower())
    wc = freq_count(word.lower())
    for letter, count in wc.items():
        if sc.get(letter, 0) < count:
            return False
        
     #check for the word in dictionary
    if len(word) > 2 and len(word) < 7:
        with open('smallWord.txt' , 'r') as smallFile:
            for smallLine in smallFile:
                if word.lower() in smallLine.lower().split():	
                    return True
            else:
                 return False   #not in dictionary
    elif len(word) > 7:
        with open('largeWord.txt' , 'r') as largeFile:
            for largeLine in largeFile:
                if word.lower() in largeLine.lower().split():
                    return True
            else:
                return False    #not in dictionary


