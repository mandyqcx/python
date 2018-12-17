#*-* encoding:UTF-8 *-*

import psycopg2

def main(id):
    conn=psycopg2.connect(host='127.0.0.1',database='postgres',port='5432',user='postgres',password='postgres')
    cursor=conn.cursor()
    select_query="select * from t where id=%s;"
    cursor.execute(select_query,(id,))
    result=cursor.fetchall()
    print(result)

    delete_query='delete from t where id=%s'
    cursor.execute(delete_query,(id,))
    conn.commit()
    count=cursor.rowcount
    print(count)

    cursor.execute(select_query,(id,))
    result=cursor.fetchall()
    print(result)


if __name__ == '__main__':
    main(11)
