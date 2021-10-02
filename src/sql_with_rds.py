from configparser import ConfigParser
import os
import psycopg2

DB_CONFIG_FILE = os.path.dirname(__file__) + '/database.ini'

def config(filename=DB_CONFIG_FILE, section='postgresql'):
    #create a parser
    parser = ConfigParser();
    # read the parser
    parser.read(filename)
    # get the section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('section {0} not found in file {1}', format(section, filename))
    return db


def connect_to_rds():
    conn = None
    try:
        # read connection parameters
        params = config()
        # connect to postgresql database
        print('connecting to postgresql database')
        conn = psycopg2.connect(**params)
        #create a cursor
        cur = conn.cursor()
        #execute a statement
        print('Postgresql database version : ')
        cur.execute('SELECT version()')
        #fetch the data
        db_version = cur.fetchone()
        print(db_version)
        #close the connection
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed ')

def create_tables():
    # provide sql statements
    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE accounts (
            account_id SERIAL PRIMARY KEY,
            account_name VARCHAR(255) NOT NULL
        )
        """
    )
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        #execute the commands
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_vendor_list(user_list):

    sql = "INSERT INTO users(user_name) VALUES (%s)"
    conn = None
    try:
        params = config()

        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        cur.executemany(sql, user_list)

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_users():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT user_id, user_name FROM users ORDER BY user_name")
        print("Numbers of users:", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
def update_user(user_id, user_name):
    sql = """ UPDATE users
              SET user_name = %s 
              WHERE user_id = %s """

    conn = None
    updated_rows = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, (user_name, user_id))

        updated_rows = cur.rowcount

        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows

def delete_user(user_name):

    conn = None
    rows_deleted = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE user_name = %s", (user_name,))

        rows_deleted = cur.rowcount

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return rows_deleted

if __name__ == '__main__':
    #connect_to_rds()
    #create_tables()
    """insert_vendor_list([
             ('John Doe',),
             ('Chiran',),
             ('Anthony Jenkins',),
             ('Docker Alan',),
             ('Richi Rich',),
             ('Phillis Reen',)
         ])"""
    #get_users()
    #delete_user('Waddup')
    response =update_user(18, 'Chiranjeev Singh')
    print(response)
    get_users()


