import mysql.connector
from mysql.connector import Error
import os
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.environ["MYSQL_HOST"],
            user=os.environ["MYSQL_USER"],
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ["MYSQL_DATABASE"],
        )
        logging.info("Connection to MySQL DB successful")
    except Error as e:
        logging.error(f"The error '{e}' occurred during connection")
        raise e
    
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
        logging.info(f"Query executed successfully: {query}")
    except Error as e:
        logging.error(f"Error executing query: {query}. Error: {str(e)}")
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
        logging.info(f"Read query executed successfully: {query}")
        return result
    except Error as e:
        logging.error(f"Error executing read query: {query}. Error: {str(e)}")
        raise e
    finally:
        cursor.close()
        connection.close()
