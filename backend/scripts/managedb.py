import mysql.connector
from mysql.connector import Error
import os


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
        )
        print("Connection to MySQL DB successful")  # TODO make this log
    except Error as e:
        print(f"The error '{e}' occurred")  # TODO make this log

    return connection


# Function to execute SQL queries that modify the database (e.g., INSERT, UPDATE, DELETE)
def execute_query(query, data=None):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:  # TODO add logging
        raise e
    finally:
        cursor.close()
        connection.close()


# Function to execute SQL queries that retrieve data (e.g., SELECT queries)
def execute_read_query(query, data=None):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()
