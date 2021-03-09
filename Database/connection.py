import mariadb
import os

def db_connection():
    conn = None
    
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_database = os.getenv('DB_DATABASE')

    try : conn = mariadb.connect(user= db_user, password= db_password, host= db_host,database= db_database)
    except mariadb.Error:
        print("Can't connect to db")
    return conn