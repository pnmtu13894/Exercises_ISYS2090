import psycopg2
import psycopg2.extras
import traceback
import sys
import os
import string
import re
import urllib2


def writeFile(outputName, string1):
    outputName = outputName.lower()
    outfile = open(outputName, "w")
    outfile.write(string1)
    outfile.close()

def connect():
    try:
        conn = psycopg2.connect("dbname=postgres user=postgres password=minhtu138 host=localhost port=55820")
        print "\nSuccessfully connected"
    except psycopg2.Error as e:
        print "\nUnable to connect the database system\n"
        print e
        print traceback.format_exc()
    cur = conn.cursor()
    cur.execute("SET search_path TO academics")
    return conn

def connectSchema(schema):
    connection = connect()
    try:
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SET search_path TO " + schema)
        return cur
    except psycopg2.Error as e:
        print e

def execute_query(cur, query, filename=None, formatName=None):
    container = ''
    try:
        cur.execute(query)
    except:
        print "\nCannot execute the database\n"

    rows = cur.fetchall()

    for row in rows:
        for c in range(len(row)):
            container += str(row[c]) + '  '
        container += '\n'
    print

    if filename == "":
        print "\nShow the table of data:\n"
        print container
    else:
        if formatName == "":
            filename += '.txt'
        else:
            filename += formatName
            writeFile(filename, container)

    check_file = checkExistingFile(filename)
    if check_file:
        print "File already existed!"

def checkExistingFile(filename):
    existed_file = False
    PATH = "./" + filename
    if os.path.isfile(PATH):
        existed_file = True
    return existed_file

def rename(file_name):
    check_file = checkExistingFile(file_name)
    if check_file:
        print "\nThe file is available\n"
        print "\nEnter the new file name(with format): "
        new_name = sys.stdin.readline()
        new_name = new_name.lower().strip()

        if new_name != "":
            os.rename(file_name, new_name)
    else:
        print "The file does not exist. You can use this name.\n\n"

def print_options():
    print "1.Execute and print out the data.\n" \
          "2.Check the file name if it's available.\n" \
          "3.Exit"

def input(connection):
    cur = connectSchema("academics")

    while connection:
        print_options()
        print "Choose the option(1, 2 or 3):"
        choice = sys.stdin.readline()
        if choice[:].strip() == "1":
            print "Enter the query: "
            SQL = sys.stdin.readline()
            if(SQL[:-1] == "quit"):
                break
            else:
                print "Enter the filename:"
                fileName = sys.stdin.readline()
                fileName = fileName.strip()
                print "Enter the format: "
                format = sys.stdin.readline()
                format = format.strip()
            execute_query(cur, SQL, fileName, format)
            connection.commit()
        elif choice[:].strip() == "2":
            print "\nEnter the file name:"
            name = sys.stdin.readline()
            name = name.lower().strip()
            rename(name)
        elif choice[:].strip() == "3":
            break
        else:
            print("The option is not available. Please choose another one.\n")
    if connection:
        connection.close()

















