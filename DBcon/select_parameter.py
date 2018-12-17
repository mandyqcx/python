# -*- encoding:UTF-8 -*-

import psycopg2


def main(ido,idt):
    try:
        conn=psycopg2.connect(host='127.0.0.1',port='5432',database='postgres',user='postgres',password='postgres')
        cursor_o=conn.cursor()
        select_quety='select * from t where id=%s or id=%s'
        cursor_o.execute(select_quety,(ido,idt))
        result=cursor_o.fetchall()
        print(result)
        for rows in result:
            print('id=',rows[0])
            print('name=',rows[1])
            print('data=',rows[2])
            print('time=',rows[3])

        cursor_t=conn.cursor()
        select_quety_2='select * from t where id=%s or id=%s'
        cursor_t.execute(select_quety_2,(ido,idt))
        result_2=cursor_t.fetchone()
        print(result_2[1])

        result_3=cursor_t.fetchone()
        print(result_3[0])

        result_4=cursor_t.fetchone()
        print(result_4)

        if conn:
            cursor_o.close()
            cursor_t.close()
            conn.close()
    except(Exception,psycopg2.Error) as error:
        print(error)


if __name__ == '__main__':
    main(2,3)



