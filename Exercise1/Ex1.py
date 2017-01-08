import psycopg2
import psycopg2.extras
import traceback
import sys
import os
import csv
import re


def read_file(file_name):
    file = open(file_name, 'r')
    container = file.read()

    return container

def write_csv_file(outputName, query):
    """
    Write the file with the content of container
    :param outputName: the name of the output file
    :param container: the string
    :return: None
    """
    file = open(outputName, 'w')
    writer = csv.writer(file)

    conn = connect()
    cur = connect_to_schema(conn, "academics")
    cur.execute(query)

    desc = cur.description

    rows = cur.fetchall()

    name = ''

    for c in range(len(desc)):
        name += desc[c][0] + ' '
    writer.writerow([name])

    for row in rows:
        data = ''
        for i in range(len(row)):
            data += str(row[i]).strip() + ' '
        writer.writerow([data])

    file.close()

def write_html_file(filename, query):
    """
    1.Connect to the database
        1.1 Execute the query and get the description
        1.2 fetch the data into an array
    2. Create a container to contain the html tags
    3. Loop through the description to get the column name
    4. Loop again the array of rows to get the data
    5. Return the contain and write onto the output file
    :param filename: the name of the output file
    :param query: The query of the user input to the database
    :return: None
    """

    conn = connect()
    cur = connect_to_schema(conn, "academics")
    file = open(filename, 'w')

    cur.execute(query)
    desc = cur.description
    rows = cur.fetchall()

    container = ''
    container += '<html>\n'
    container += '<div style="display: None;">%s</div>' % query
    container += '\n<table>\n<tr>\n'

    for c in range(len(desc)):
        container += '<th>%s</th>\n' % str(desc[c][0])
    container += '</tr>\n'

    for i in range(len(rows)):
        container += '<tr>\n'
        for j in range(len(desc)):
            container += '<td>%s</td>\n' % (str(rows[i][j]).strip())
        container += '</tr>\n'
    container += '</table>\n</html>'

    file.write(container)
    file.close()

def write_file(output_name, query):
    """
    1.Convert the output name into lower case
    2. open the file
    3. write the data onto the file
    4. close the file
    :param output_name: name of the output file
    :param container: string of data
    :return: None
    """
    container = get_data_from_query(query)

    output_name = output_name.lower()
    outfile = open(output_name,'w')
    outfile.write(container)
    outfile.close()

def connect():
    """
    1. Using the psycopg2 package to connect to the database
    :return: the connection to the database
    """
    try:
        conn = psycopg2.connect("dbname=postgres user=postgres password=minhtu138 host=localhost port=55820")
    except psycopg2.Error as e:
        print "\nUnable to connect the database system\n"
        print e
        print traceback.format_exc()
    cur = conn.cursor()
    return conn

def connect_to_schema(connection, schema):
    """
    1. Connect to the database
    2. Execute the query to Set search_path to the specific schema
    :param schema: the name of schema that user want to connect
    :param connection: The connection to the database
    :return:  the cursor
    """

    try:
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SET search_path TO " + schema)
        return cur
    except psycopg2.Error as e:
        print e

def execute_query(query, filename=None, formatName=None):
    """
    1. Execute the query
    2. Get the widths between columns and the column names
    3. fetch all the data into an array
    4. Loop through the array to collect data into the container of string
    5. Check filename
        5.1 If the filename is empty or None
            5.1.1 print out the container as default text
        5.2 Else continuing check the format is empty or None
            5.2.1 If the format is empty
                5.2.1.1 plus the filename with the default plain text (.txt)
            5.2.2 Else filename will plus with the format name
    6. Check the three possible format names which are .html, .csv, .txt
    7. Write data based on the format name into the output file.

    :param cur: the cursor
    :param query: the input query
    :param filename: the name of output file
    :param formatName: the format of output file
    :return: None
    """
    container = get_data_from_query(query)

    if filename == "" or filename is None:
        print "\nShow the table of data:\n"
        print container
    else:
        if formatName == "" or filename is None:
            filename += '.txt'
        else:
            filename += formatName
            if formatName == '.csv':
                write_csv_file(filename,query)
            elif formatName == '.html':
                write_html_file(filename, query)
            else:
                write_file(filename, query)

def get_data_from_query(query):
    container = ''
    conn = connect()
    cur = connect_to_schema(conn, "academics")

    try:
        cur.execute(query)
    except:
        print "\nCannot execute the database\n"
    desc = cur.description

    # column_widths = get_column_widths(desc)

    column_names = get_column_names(desc)
    container += column_names + "\n"

    rows = cur.fetchall()

    for row in rows:
        for c in range(len(row)):
            container += str(row[c]).strip() + ' '
        container += '\n'
    print

    return container

def check_existing_file(filename):
    """
    Check if the file exists or not
    :param filename: name of the output file
    :return: boolean parameter True or False
    """
    existed_file = False
    if filename is not None:
        PATH = "./" + filename
        if os.path.isfile(PATH):
            existed_file = True
    return existed_file

def rename(old_file_name, old_format):
    """
    Rename the old file name with the new one
    :param file_name: name of the output file
    :return: None
    """
    old_file = old_file_name + old_format
    check_file = check_existing_file(old_file)
    if check_file:
        print "\nThe file is available\n"

        print "\nEnter the new file name: "
        new_name = sys.stdin.readline()
        new_name = new_name.lower().strip()

        print "\nEnter the new format: "
        new_format = sys.stdin.readline()
        new_format = new_format.lower().strip()

        new_file = new_name + new_format

        if new_file != "":
            if format == new_format:
                os.rename(old_file, new_file)
            else:
                container = read_file(old_file)
                if old_format == '.html':
                    query = re.search(r'(?<=<div style="display: None;">)[* \w\d+]+', container).group()
                else:
                    os.rename(old_file,new_file)
    else:
        print "The file does not exist. You can use this name.\n\n"

def get_column_widths(desc):
    """
    Get the width between columns
    :param desc: the description of the executed query
    :return: the list of value
    """
    widths = []
    for i in range(len(desc)):
        if(len(desc[i][0]) > desc[i][2]):
            widths.append(len(desc[i][0]))
        else:
            widths.append(desc[i][2])
    return widths

def get_column_names(desc):
    """
    Get the name of columns and put into the container of strings
    :param desc: the description of executed query
    :return: the string value
    """
    widths = get_column_widths(desc)
    container = ''
    for i in range(len(desc)):
        container += desc[i][0] + ' '*(widths[i])
    return container

def print_options():
    """
    Print out the possible options
    :return: None
    """
    print "1.Execute and print out the data.\n" \
          "2.Check the file name if it's available.\n" \
          "3.Exit"

def input(connection):
    """

    :param connection: the connection to the database
    :return: None
    """
    conn = connect()
    cur = connect_to_schema(conn, "academics")

    while connection:
        print_options()
        print "Choose the option(1, 2 or 3):"
        choice = sys.stdin.readline()
        if choice[:].strip() == "1":
            print "Enter the query: "
            SQL = sys.stdin.readline()
            if(SQL[:-1] == "quit"):
                continue
            else:
                print "Enter the filename:"
                fileName = sys.stdin.readline()
                fileName = fileName.strip()
                print "Enter the format: "
                format = sys.stdin.readline()
                format = format.strip()
            raw_file_name = fileName + format
            print raw_file_name
            valid_file = check_existing_file(raw_file_name)
            if valid_file:
                print "\n\nExisted File. Please change another name!!!\n"
                continue
            else:
                execute_query(SQL, fileName, format)
                connection.commit()
        elif choice[:].strip() == "2":
            print "\nEnter the file name:"
            name = sys.stdin.readline()
            name = name.lower().strip()
            print "\nEnter the format name: "
            format = sys.stdin.readline()
            format = format.lower().strip()

            rename(name, format)
        elif choice[:].strip() == "3":
            break
        else:
            print("The option is not available. Please choose another one.\n")
    if connection:
        connection.close()

def run():
    connectDatabase = connect()
    input(connectDatabase)



# file = open('output1.csv', 'r')
#
# data = csv.reader(file)
# container = ''
# for row in data:
#      container += ' '.join(row) + '\n'
#
# list =  container.split('\n')
























