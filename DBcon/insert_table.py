#-*- encoding:UTF-8 -*-

import psycopg2

def main(id,name,value,time):
    conn=psycopg2.connect(host='127.0.0.1',database='postgres',port='5432',user='postgres',password='postgres')
    cursor=conn.cursor()
    insert_query='insert into t(id,name,value,data_time) values(%s,%s,%s,%s)'
    values=(id,name,value,time)
    cursor.execute(insert_query,values)
    conn.commit()
    rowcount=cursor.rowcount
    print(rowcount)

if __name__ == '__main__':
    main(11,'Mandy',100,'now()')


