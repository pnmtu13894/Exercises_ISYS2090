from Exercise1.Ex1 import *


def checkValidSQLFile(filename):
    checkValidFile = True
    validFile = re.search(r'[\w\d+].(?=.sql)',filename)
    if validFile is None:
        checkValidFile = False

    return checkValidFile

def openFile(filename):
    valid_file = checkValidSQLFile(filename)
    if valid_file:
        inputFile = open(filename, 'r')
        output = inputFile.read()
    else:
        print "Wrong file. You need file with SQL extension."
    return output

file = openFile("Queries.sql")
listOfQueries = re.sub('\n',' ',file)
queries = listOfQueries.split("; ")

cur = connectSchema("academics")
cur.execute(queries[1])

execute_query(cur,queries[1], filename=None, formatName=None)
