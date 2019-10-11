# -*- encoding: utf-8 -*-
#模型定阶

import psycopg2,sys
import pandas,numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.tsa.stattools import arma_order_select_ic

def get_data(parameter):
    try:
        conn=psycopg2.connect(user="etl_usr",
                              password="$etl_usr",
                              host="192.168.1.150",
                              port="5432",
                              database="create_dw_dev")
    except psycopg2.OperationalError as e:
        print('Connect Fail',e)
    else:
        print('Connect Successfully',conn.get_dsn_parameters())
        cursor=conn.cursor()
        cursor.execute("""select data_time,data_value
                        from ods.wdp_history_data_4h
                        where data_time>='2019-06-01 00:00:00'
                        and mn_code='06057581301002'
                        and model_code = '{model_code}'
                        order by data_time;""".format(model_code=parameter))
        result=cursor.fetchall()

        data_time=[i[0] for i in result]
        data_value=[float(i[1]) for i in result]
        df=pandas.DataFrame({'data_time' : data_time, 'data_value' : data_value})

        if conn:
            cursor.close()
            conn.close()
            print("postgresql conection is closed")
        return df


def draw_picture():
    parameter_type = ['060', '101', 'W07']
    wdp_mode={'060':'氨氮','101':'总磷','W07':'高锰酸盐'}
    data_set={parameter:get_data(parameter) for parameter in parameter_type}
    mpl.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
    mpl.rcParams['axes.unicode_minus'] = False
    for key,value in data_set.items():
        print(wdp_mode[key], arma_order_select_ic(value['data_value'],ic='aic',max_ar=30,max_ma=30,trend='nc').aic_min_order)
    return 0


if __name__ == '__main__':
    sys.exit(draw_picture())
    #sys.exit(get_data())

