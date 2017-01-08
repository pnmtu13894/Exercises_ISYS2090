from Exercise1.Ex1 import *
from random import randint


def create_random_table(table_name, number_of_rows, number_of_random_columns, maximum_value_of_column):
    conn = connect()
    cur = connect_to_schema(conn, 'academics')

    table_content = "CREATE TABLE " + table_name + "( id SERIAL, "
    arr_of_columns = []
    inserted_columns = []
    for i in range(randint(2, number_of_random_columns)):
        tmp = "column" + str(i) + " integer"
        tmp1 = "column" + str(i)
        inserted_columns.append(tmp1)
        arr_of_columns.append(tmp)


    completed_table = ', '.join(arr_of_columns)

    table_content += completed_table + ", PRIMARY KEY(id));"

    try:
        cur.execute(table_content)
        print "Created table"
        conn.commit()
    except psycopg2.Error as e:
        print 'Unable to create table'
        print e


    for i in range(number_of_rows):
        insert_query = "INSERT INTO " + table_name + "(" + ', '.join(inserted_columns) + ")" + " VALUES("
        arr_of_numbers = []
        for j in range(len(arr_of_columns)):
            random_number = randint(1, maximum_value_of_column)
            arr_of_numbers.append(str(random_number))

        number_values = ', '.join(arr_of_numbers)

        insert_query += number_values + ")"

        try:
            cur.execute(insert_query)
            print "Inserted data into database"
            conn.commit()
        except psycopg2.Error as e:
            print 'Unable to insert data'
            print e
    return table_name


def create_table_as(table_name):
    conn = connect()
    cur = connect_to_schema(conn, 'academics')

    created_table = create_random_table("test4", 300, 10, 2000)

    table_content = "CREATE TABLE " + table_name + " AS TABLE " + created_table

    try:
        cur.execute(table_content)
        print "Created new table"
        conn.commit()
    except psycopg2.Error as e:
        print 'Unable to create new table'
        print e

create_table_as("duplicate")


