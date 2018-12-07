#-*- encoding:UTF-8 -*-

import psycopg2

def main():
    conn=psycopg2.connect(host='127.0.0.1',database='postgres',port='5432',user='postgres',password='postgres')
    cursor=conn.cursor()
    create_table_query='create table py_table(id int,name varchar(32))'
    cursor.execute(create_table_query)
    conn.commit()
    print('table is created')
    if conn:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
