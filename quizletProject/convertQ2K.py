import time
import sys
import re

def readFile(dir):
    try:
        rawList = []
        f = open(dir, 'r', encoding='UTF-8')
        rawList.append(str(f.read()).split('**'))
        rawList[0].pop()
        rawList = rawList[0]
        f.close()
        return rawList
    except:
        print('[-] Error while opening files.')

def type2FirstParse(rawList):
    answers = []
    questions = []
    finalList = []
    questionAnswer = []
    for i in range(len(rawList)):
        q = rawList[i].split('~~')[0]
        a = rawList[i].replace('\n', '').replace('', '').split('~~')[1].lower()
        forRegex = re.split(r'[\n]{1,2}[a-gA-G]{1}[,.)]{0,1}[ ]{1}', q, flags=re.IGNORECASE)
        questions.append(forRegex[0].replace('\n', ' '))
        questionAnswer.append(forRegex)
        answers.append(a.lower())
    return finalList, questions, questionAnswer, answers

def parseText_Type2(dir):
    answerAfterParse = []
    errorList = []
    pos = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 't': 'True', 'f': 'False'}
    boolCheck = {'a': 'True', 'b': 'False', 't': 'True', 'f': 'False'}

    rawList = readFile(dir)
    finalList, questions, questionAnswer, answers = type2FirstParse(rawList)

    for i in range(len(questionAnswer)):
        position = pos.get(answers[i])
        try:
            if not position == 'True' or position == 'False':
                if 'True B. False' in questionAnswer[i][position]:
                    answerAfterParse.append('True')
                else:
                    answerAfterParse.append(questionAnswer[i][position].replace('\n', ' '))
            else:
                answerAfterParse.append(position)
        except:
            answerAfterParse.append(boolCheck.get(answers[i]))

    for i in range(len(questions)):
        sub = re.sub('^[0-9a-zA-Z]{1,2}[.)]{1}[ ]{1}', ' ', questions[i].replace('  ', ' '))
        try:
            key = str(sub) + '|' + answerAfterParse[i]
            if key in finalList:
                pass
            else:
                finalList.append(key + '\n')
        except:
            if len(answers[i]) > 2:
                finalList.append(str(sub)+'|'+str(answers[i]))
            else:
                errorList.append(str(sub)+'|')
    return finalList, errorList

def type1FirstParse(rawList):
    finalList = []
    for i in range(len(rawList)):
        question = rawList[i].replace('\n', ' ').replace('  ', ' ').split('~~')[0]
        question = re.sub('^[# ]{1,2}', '', question)
        question = re.sub('^[0-9]{1,3}[.) ]{1,3}', '', question)
        question = re.sub('^[a-z]{1,2}[=]{1}[0-9]{1,3}[ ]{1,2}', '', question, flags=re.IGNORECASE)
        answer = rawList[i].replace('\n', ' ').replace('  ', ' ').split('~~')[1]
        key = str(question) + '|' + str(answer)
        if question == '' and answer == '':
            pass
        else:
            if key in finalList:
                pass
            else:
                finalList.append(key + '\n')
    return finalList

def parseText_Type1(dir):
    rawList = readFile(dir)
    finalList = type1FirstParse(rawList)
    return finalList

if __name__=='__main__':
    start = time.time()
    file = open('key.txt', 'a', encoding='UTF-8')
    if len(sys.argv) == 3:
        if sys.argv[1] == r'2':
            fList, error = parseText_Type2(sys.argv[2])
            count = 0
            for i in error:
                count += 1
                print(i)
            for i in fList:
                file.write(i)
            print('\n[+] Error total: ' + str(count))
        elif sys.argv[1] == r'1':
            fList = parseText_Type1(sys.argv[2])
            for i in fList:
                file.write(i)
    else:
        exit('[-] Wrong format. Usage: python ' + str(sys.argv[0]) + ' (type of raw question) <rawList.txt>')
    print('-------------------------------------------------------------')
    end = time.time() - start
    time.sleep(0.0000000001)
    exit('Program executed in ' + str(end) + ' seconds')

# Notes: This is Code just applied with the parser for the answer is: ~~ and next question is: **