# -*- encoding: utf-8 -*-
#时序图

import psycopg2,sys
import pandas,numpy
import matplotlib.pyplot as plt
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
    parameter_type = ['W01', '060', 'W02', '101', 'W07']
    wdp_mode={'W01':'水温','060':'氨氮','W02':'溶解氧','101':'总磷','W07':'高锰酸盐'}
    data_set={parameter:get_data(parameter) for parameter in parameter_type}
    for key,value in data_set.items():
       data_mean=numpy.mean(value['data_value'])
       data_std=numpy.std(value['data_value'])
       plt.plot(value['data_time'],value['data_value'],marker='o',ms=3,mfc='r')
       plt.axhline(data_mean, color='y',label=data_mean)
       plt.axhline(data_mean-3*data_std, color='r')
       plt.axhline(data_mean+3*data_std, color='r')
       mpl.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文
       mpl.rcParams['axes.unicode_minus'] = False
       plt.xlabel("时间")  # 显示横轴标签
       plt.ylabel("值")   # 显示纵轴标签
       plt.title(wdp_mode[key]) # 显示图标题
       plt.show()
    return 0

if __name__ == '__main__':
    sys.exit(draw_picture())
    #sys.exit(get_data())

