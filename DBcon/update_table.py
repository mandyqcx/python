# -*- encoding:UTF-8 -*-

import psycopg2


def main(id,name):
    conn=psycopg2.connect(host='127.0.0.1',database='postgres',port='5432',user='postgres',password='postgres')
    cursor=conn.cursor()
    select_query="select * from t where id=%s;"
    cursor.execute(select_query,(id,))
    result=cursor.fetchall()
    print(result)

    update_query="update t set name=%s where id=%s;"
    cursor.execute(update_query,(name,id))
    conn.commit()
    row=cursor.rowcount
    print(row)

    cursor.execute(select_query,(id,))
    result=cursor.fetchall()
    print(result)

    if conn:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main(11,'kimmy')
