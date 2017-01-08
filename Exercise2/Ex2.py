from Exercise1.Ex1 import *
from time import clock
import re


def check_valid_SQL_file(filename):
    checkValidFile = True
    validFile = re.search(r'[\w\d+].(?=.sql)',filename)
    if validFile is None:
        checkValidFile = False

    return checkValidFile

def open_file(filename):
    valid_file = check_valid_SQL_file(filename)
    if valid_file:
        try:
            inputFile = open(filename, 'r')
            output = inputFile.read()
            return output
        except IOError as ioe:
            print ioe.message
    else:
        print "Wrong file. You need file with SQL extension."

def get_query_list(SQLfile):
    valid_file = check_valid_SQL_file(SQLfile)
    if valid_file:
        file = open_file(SQLfile)
        listOfQueries = re.sub('\n',' ',file)
        queries = listOfQueries.split("; ")
        return queries
    else:
        print "This file is not SQL file!!!"

def get_rows_from_query(query):
    conn = connect()
    cur = connect_to_schema(conn, "academics")

    try:
        cur.execute("EXPLAIN ANALYSE " + query + ";")
    except:
        print "The query is not valid!!!"

    return cur.fetchall()

def get_planning_time(query):
    for tup in get_rows_from_query(query):
        planning_time = re.search(r'(?<=Planning time: )(\d+.\d*)', tup[0])

        if planning_time:
            return planning_time.group()

def get_execution_time(query):
    for tup in get_rows_from_query(query):
        execution_time = re.search(r'(?<=Execution time: )(\d+.\d*)', tup[0])

        if execution_time:
            return execution_time.group()

def get_client_time(query):
    conn = connect()
    cur = connect_to_schema(conn, "academics")
    start = clock()
    for i in range(500):
        cur.execute(query + ";")
    end = clock()

    return end - start

def create_table(table_name):
    conn = connect()
    cur = connect_to_schema(conn, "academics")

    try:
        cur.execute("DROP TABLE IF EXISTS " + table_name)
        cur.execute("CREATE TABLE " + table_name + "("
                    "id SERIAL,"
                    "time timestamp default NOW(),"
                    "planning_time REAL,"
                    "execution_time REAL,"
                    "run_time REAL,"
                    "query TEXT,"
                    "client_time REAL,"
                    "cold_run REAL,"
                    "hot_run REAL,"
                    "PRIMARY KEY(id)"
                    ")")
        print "Created table " + table_name
        conn.commit()
    except psycopg2.Error as e:
        print e


def insert_data_into_database(table_name):
    conn = connect()
    cur = connect_to_schema(conn, "academics")
    sql_list = get_query_list("Queries.sql")

    create_table(table_name)

    for query in sql_list:
        planning_time = float(get_planning_time(query))
        execution_time = float(get_execution_time(query))
        client_time = float(get_client_time(query))
        cold_run = float(get_execution_time(query))
        hot_run = 0
        for i in range(3):
            hot_run += float(get_execution_time(query))
        hot_run = hot_run/3
        try:

            cur.execute("INSERT INTO " + table_name +
                        "(planning_time, execution_time, run_time, query, client_time, cold_run, hot_run) "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (planning_time, execution_time, execution_time, query, client_time, cold_run, hot_run))
            print "Successfully inserting data."
            conn.commit()
        except psycopg2.Error as e:
            print e

insert_data_into_database("exercise2")
# conn = connect()
# cur = connect_to_schema(conn, 'academics')

# cur.execute("CREATE INDEX fieldnum_index ON interest (fieldnum)")

# sql_list = get_query_list("Queries.sql")
#
# for sql in sql_list:
#     print sql

# print sql_list
# cur.execute("CREATE INDEX ON interest (fieldnum)")
# conn.commit()

# print sql_list
# cur.execute("EXPLAIN ANALYSE " + sql_list[len(sql_list) - 1])


# for tuple in cur.fetchall():
#     print tuple

