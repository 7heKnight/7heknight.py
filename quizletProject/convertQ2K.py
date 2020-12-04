import time
import sys
import re

def readFile(dir):
    key = None
    rawList = []
    try:
        file = open('key.txt', 'r', encoding='UTF-8')
        key = file.read()
        key = re.sub('[*]{3,99}', '**', key)
        key = re.sub('[~]{3,99}', '~~', key)
        file.close()
    except:
        pass
    try:
        f = open(dir, 'r', encoding='UTF-8')
        rawList.append(str(f.read()).split('**'))
        rawList[0].pop()
        rawList = rawList[0]
        f.close()
    except IOError:
        print('[-] Error while opening files.')
    return key, rawList

def type2FirstParse(rawList):
    answers = []
    questions = []
    finalList = []
    questionAnswer = []
    for i in range(len(rawList)):
        q = rawList[i].split('~~')[0].replace('\n\n', '\n').replace('  ', ' ') # Changed here
        a = rawList[i].replace('\n', '').replace(' ', '').split('~~')[1].lower()
        forRegex = re.split(r'[\n\[ ]{1}[a-gA-G]{1}[,.)\]]{1}[ ]{0,1}', q, flags=re.IGNORECASE) #here
        questions.append(forRegex[0].replace('\n', ' '))
        questionAnswer.append(forRegex)
        answers.append(a.lower())
    return finalList, questions, questionAnswer, answers

def parseText_Type2(dir):
    answerAfterParse = []
    errorList = []
    pos = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 't': 'True', 'f': 'False'}
    boolCheck = {'a': 'True', 'b': 'False', 't': 'True', 'f': 'False'}

    key, rawList = readFile(dir)
    finalList, questions, questionAnswer, answers = type2FirstParse(rawList)

    for i in range(len(questionAnswer)):
        position = pos.get(answers[i])
        try:
            if not (position == 'True' or position == 'False'):
                if 'True B. False' in questionAnswer[i][position]:
                    answerAfterParse.append('True')
                else:
                    answerAfterParse.append(questionAnswer[i][position].replace('\n', ' '))
            else:
                answerAfterParse.append(position)
        except:
            answerAfterParse.append(boolCheck.get(answers[i]))

    for i in range(len(questions)):
        sub = re.sub('^[ \[]{0,1}[0-9a-zA-Z]{1,2}[.)\]]{1}[ ]{1}', '', questions[i].replace('  ', ' '))
        sub = re.sub('^[ ~]{1,2}', '', sub)
        sub = re.sub('^[0-9]{1,3}[)]{1}[ ]{1}', '', sub)
        sub = re.sub('^[0-9]{1,4}[/. ]{1,3}', '', sub)
        sub = re.sub('^[A-Z]{1,3}[=]{1,2}[0-9]{1,4}[ ]{0,1}', '', sub)
        sub = re.sub('^[(]{1}[0-9]{1,9}[)]{1}[ ]{1}', '', sub)
        try:
            stringQ = str(sub)
            stringA = answerAfterParse[i]
            if not stringQ.replace(' ', '') == '' and not stringA.replace(' ', '') == '':
                keyParsed = str(sub) + '|' + answerAfterParse[i]
                if keyParsed in key:
                    pass
                else:
                    finalList.append(keyParsed + '\n')
            else:
                pass
        except:
            if len(answers[i]) > 2:
                keyParsed = str(sub) + '|' + answers[i]
                if keyParsed in key:
                    pass
                else:
                    finalList.append(keyParsed + '\n')
            else:
                errorList.append(str(sub)+'|')
    return finalList, errorList

def type1FirstParse(key, rawList):
    finalList = []
    for i in range(len(rawList)):
        question = rawList[i].replace('\n', ' ').replace('  ', ' ').split('~~')[0]
        question = re.sub('^[# ]{1,2}', '', question)
        question = re.sub('^[0-9]{1,3}[.) ]{1,3}', '', question)
        question = re.sub('^[a-z]{1,2}[=]{1}[0-9]{1,3}[ ]{1,2}', '', question, flags=re.IGNORECASE)
        answer = rawList[i].replace('\n', ' ').replace('  ', ' ').split('~~')[1]
        keyParsed = str(question) + '|' + str(answer)
        if not (question == '' and answer == ''):
            if keyParsed in key:
                pass
            else:
                finalList.append(keyParsed + '\n')
        else:
            pass
    return finalList

def parseText_Type1(dir):
    key, rawList = readFile(dir)
    finalList = type1FirstParse(key, rawList)
    return finalList

def type3(dir):
    file = open(dir, 'r', encoding='UTF-8')
    arguments = file.read()
    arguments = re.sub('[*]{3,99}', '**', arguments)
    arguments = re.sub('[~]{3,99}', '~~', arguments)
    file.close()
    arguments = arguments.split('**')
    arguments.pop()
    count = 0
    try:
        file = open(dir, 'w', encoding='UTF-8')
        for i in arguments:
            file.write(i.split('~~')[1] + '~~' + i.split('~~')[0] + '**')
            count += 1
        file.close()
    except:
        exit('[-] Error unknown.')
    print('\n[+] Overrided position of ' + str(count) + ' lines into File: ' + dir)

def type4(dir):
    count = 0
    dup = 0
    formE = 0
    keyList = []
    
    file = open(dir, 'r', encoding='UTF-8')
    arguments = file.read()
    file.close()
    arguments = arguments.split('\n')
    arguments.pop()

    for i in arguments:
        try:
            if not i.split('|')[0] == '' and not i.split('|')[1] == '':
                if i.replace(' ', '') in keyList:
                    dup += 1
                else:
                    keyList.append(i + '\n')
            else:
                print('[-] Wrong format: '+i)
                formE += 1
        except:
            print('[-] Wrong format1: ' + i)
            formE += 1
    try:
        file = open(dir+'.log', 'w', encoding='UTF-8')
        for i in keyList:
            file.write(i)
            count += 1
        file.close()
    except:
        exit('[-] Error unknown.')
    print('\n[+] Overrided ' + str(count) + ' key and ' + str(dup) + ' duplicated key and ' + str(formE) + ' key in wrong form.')

if __name__=='__main__':
    start = time.time()
    file = open('key.txt', 'a', encoding='UTF-8')
    if len(sys.argv) == 3:
        if sys.argv[1] == r'2':
            fList, error = parseText_Type2(sys.argv[2])
            count = 0
            countKey = 0
            for i in error:
                count += 1
                print(i)    # print list of error
            for i in fList:
                countKey += 1
                file.write(i)   # write key to files
            print('\n[+] Errors total: ' + str(count))
            print('[+] Keys total wrote to file: ' + str(countKey))
        elif sys.argv[1] == r'1':
            fList = parseText_Type1(sys.argv[2])
            countKey = 0
            for i in fList:
                file.write(i)
                countKey += 1
            print('\n[+] Keys total wrote to file: ' + str(countKey))
        elif sys.argv[1] == r'3':
            type3(sys.argv[2])
        elif sys.argv[1] == r'4':
            type4(sys.argv[2])
        else:
            exit('[-] Option not found!')
    else:
        exit('[-] Wrong format. Usage: python ' + str(sys.argv[0]) + ' (type of raw question) <rawList.txt>')
    print('-------------------------------------------------------------')
    end = time.time() - start
    time.sleep(0.0000000001)
    exit('Program executed in ' + str(end) + ' seconds')

# Notes: This is Code just applied with the parser for the answer is: ~~ and next question is: **
