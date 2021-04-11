import sqlite3
import re

def existDB(fileName):
    try:
        open(fileName)
        return True
    except:
        return False

if __name__=='__main__':
    # Checking if file not found, it will exit the program
    fileName = 'Course.txt'
    if not existDB(fileName):
        exit('[-] File not found!')
    openFile = open(fileName)

    # Checking if database exist, it will execute in the memory
    database = 'dbSCList.sqlite'
    if not existDB(database):
        connection = sqlite3.connect(database)
    else:
        connection = sqlite3.connect(':memory:')
    cur = connection.cursor()

    # Creating the studentCourse table
    cur.execute('CREATE TABLE StudentCourse (SCode TEXT, CCode TEXT, avg REAL, SDes TEXT)')

    # Parsing text file and insert into database
    listStudent = openFile.readlines()
    for i in range(1, len(listStudent)):
        studentCode, course, avg = re.findall(r'(\S+?)[ \t\n]', listStudent[i])
        if float(avg) >= 5:
            status = 'PASSED'
        else:
            status = 'NOT PASSED'
        cur.execute('INSERT INTO StudentCourse VALUES ( ?, ?, ?, ?)', (studentCode, course, float(avg), status))

    # Print top 5
    cur.execute('SELECT * FROM StudentCourse ORDER BY avg DESC, SCode LIMIT 5')
    result = cur.fetchall()
    print('SCode', ' CCode', ' AVG', ' Status')
    for row in result:
        print(row[0], row[1], row[2], row[3])
    connection.close()
    print('----------------------------\n[+] Executed successfully!')
