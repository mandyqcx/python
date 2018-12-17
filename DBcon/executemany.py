# -*- encoding: UTF-8 -*_

import psycopg2

def main(lista,listb,listc):
    conn=psycopg2.connect(host='127.0.0.1',port='5432',database='postgres',user='postgres',password='postgres')
    cursor=conn.cursor()
    insert_query='insert into t(id,name,value,data_time) values(%s,%s,%s,%s)'
    cursor.executemany(insert_query,lista)
    conn.commit()
    rowcount=cursor.rowcount
    print(rowcount)


    update_query='update t set value=%s where id=%s'
    cursor.executemany(update_query,listb)
    conn.commit()
    rowcount=cursor.rowcount
    print(rowcount)

    delete_query='delete from t where id=%s'
    cursor.executemany(delete_query,listc)
    conn.commit()
    rowcount=cursor.rowcount
    print(rowcount)


if __name__ == '__main__':
    lista=[(11,'mandy',100,'now()'),(12,'kimmy',110,'now()')]
    listb=[(110,11),(100,12)]
    listc=[(11,),(12,)]
    main(lista,listb,listc)



