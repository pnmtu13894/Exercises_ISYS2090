from Exercise1.Ex1 import *


def checkValidSQLFile(filename):
    checkValidFile = True
    validFile = re.search(r'[\w\d+].(?=.sql)',filename)
    if validFile is None:
        checkValidFile = False

    return checkValidFile

def openFile(filename):
    inputFile = open(filename, 'r')
    output = inputFile.read()
    return output

file = openFile("Queries.txt")
listOfQueries = re.sub('\n',' ',file)
queries = listOfQueries.split("; ")
print listOfQueries
for query in queries:
    print query