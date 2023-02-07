import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect("./polygons.db")
        print(f'successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(e)
    if conn:
        return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def initialize_data(conn, polygon):
    sql = ''' INSERT INTO polygon(name,coordinates)
                  VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, polygon)
    return cur.lastrowid

def main():
    database = "polygons.db"
 
    sql_create_polygon_table = """ CREATE TABLE IF NOT EXISTS polygon (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        coordinates text NOT NULL
                                    ); """
 
    conn = create_connection()
    if conn is not None:
        create_table(conn, sql_create_polygon_table)
        polygon = ('polygon1', '[[0,0], [0,1], [1,1], [1,0], [0,0]]')
        initialize_data(conn, polygon)
        conn.commit()
    else:
        print("Error! Cannot create the database connection.")
 
if __name__ == '__main__':
    main()


