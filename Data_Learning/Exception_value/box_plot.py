# -*- coding: utf-8 -*-


import psycopg2,sys
import pandas,seaborn,numpy
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl

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
        cursor.execute("""select data_value
                        from ods.wdp_history_data_4h
                        where data_time>='2019-06-01 00:00:00'
                        and mn_code='06057581301002'
                        and model_code = '{model_code}'
                        order by data_time;""".format(model_code=parameter))
        result=cursor.fetchall()
        data_value = [float(i[0]) for i in result]

        if conn:
            cursor.close()
            conn.close()
            print("postgresql conection is closed")
        return data_value



def draw_picture():
    parameter_type = ['W01', '060', 'W02', '101', 'W07']
    wdp_mode={'W01':'水温','060':'氨氮','W02':'溶解氧','101':'总磷','W07':'高锰酸盐'}
    data_set={parameter:get_data(parameter) for parameter in parameter_type}
    for key,value in data_set.items():
       plt.boxplot(value, showmeans=True)
       mpl.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文
       mpl.rcParams['axes.unicode_minus'] = False
       plt.title(wdp_mode[key]) # 显示图标题
       plt.show()
    return 0

if __name__ == '__main__':
    sys.exit(draw_picture())
    #sys.exit(get_data())






