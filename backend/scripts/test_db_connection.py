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
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
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
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()


# Function to execute SQL queries that retrieve data (e.g., SELECT queries)
def execute_read_query(query):
    connection = create_connection()
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()


# Function to test the connection and query sample data
def test_connection_and_query():
    connection = create_connection()
    if connection:
        print("Testing connection...")
        try:
            # Query to select all meetings
            select_meetings_query = "SELECT * FROM meetings;"
            meetings = execute_read_query(select_meetings_query)
            if meetings:
                for meeting in meetings:
                    print(meeting)
            else:
                print("No meetings found.")
        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            connection.close()


if __name__ == "__main__":
    test_connection_and_query()
