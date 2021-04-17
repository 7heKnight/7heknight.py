import sqlite3

if __name__ == '__main__':
    connection = sqlite3.connect("dbFPT.sqlite")
    cursor = connection.cursor()

    connection.execute("""DROP TABLE IF EXISTS InFos""")

    connection.execute("""CREATE TABLE InFos (
                ProCode INTEGER, 
                Deleted TXT
                );""")

    file = open("datafile.txt",'r').readlines()
    data = [file[i] for i in range(1,len(file))]
    for row in data:
        row = row.rstrip().split()
        cursor.execute("""INSERT INTO InFos(ProCode, Deleted)
                    VALUES (?, ?)""", [row[0], str(row[3])])
        connection.commit()
    sqlStatement = "SELECT * FROM InFos ORDER BY ProCode DESC"
    query = cursor.execute(sqlStatement)