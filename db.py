import mysql.connector


def get_db_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abi@2805",
        database="task_manager"
    )

    return connection