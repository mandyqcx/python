#-*- encoding:UTF-8 -*-

import psycopg2


def main():
        connection=psycopg2.connect(user="postgres",password="postgres",host="127.0.0.1",port="5432",database="postgres")
        cursor=connection.cursor()
        print (connection.get_dsn_parameters(),'\n')
        cursor.execute("select id,name from t")
        #record=cursor.fetchall()
        #record=cursor.fetchmany()
        for i in range(10):
            record=cursor.fetchall()
            print(record)
        if (connection):
            cursor.close()
            connection.close()
            print("postgresql conection is closed")


if __name__ == '__main__':
    main()
