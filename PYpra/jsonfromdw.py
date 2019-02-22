#-*- encoding:UTF-8 -*-


import psycopg2

def main():
    connection=psycopg2.connect(user='etl_usr',password='$etl_usr',host='192.168.1.150',port='5432',database='create_dw_dev')
    cursor=connection.cursor()
    #print(connection.get_dsn_parameters(),'\n') 检查是否连接成功，已经连接的参数
    '''cursor.execute("select  (data_value->>'data_time')::timestamp as data_time,\
                   (data_value->>'mn_code')::varchar(32) as mn_code, \
                   data_value->'metric'->'Rtd' as rtd \
                   from chr_raw_history_json \
                   where (data_value->>'data_time')::timestamp>='2018-10-03 01:00:00' \
                   and (data_value->>'data_time')::timestamp<'2018-10-03 01:00:10'")'''
    cursor.execute('select data_time,mn_code,rtd from tmp.temp_row_json;')

    records=cursor.fetchall()
    for data_time,mn_code,data in records:
        total_len=len(data)

        value=list(data.values())
        actul_len=len([i for i in value if i !='null'])

        data_rate=actul_len/total_len

        insert_query='insert into tmp.temp_data_rate_result(data_time,mn_code,total_len,actul_len,data_rate) values(%s,%s,%s,%s,%s)'
        values=(data_time,mn_code,total_len,actul_len,data_rate)
        cursor.execute(insert_query,values)

    connection.commit()



if __name__=='__main__':
    main()
