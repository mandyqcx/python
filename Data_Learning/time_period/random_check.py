# -*- encoding: utf-8 -*-
#自相关图

import psycopg2,sys
import pandas,numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller as adf
from statsmodels.sandbox.stats.diagnostic import acorr_ljungbox


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
        print(wdp_mode[key],acorr_ljungbox(value['data_value'], lags=6))
        mpl.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文
        mpl.rcParams['axes.unicode_minus'] = False
       # plt.title(wdp_mode[key]) # 显示图标题
       # plt.show()
    return 0


if __name__ == '__main__':
    sys.exit(draw_picture())
    #sys.exit(get_data())



# 水温 (array([ 385.77961266,  724.33438505, 1034.35064716, 1333.21464245,1627.76095602, 1881.26912357]),
#     array([6.86551888e-086, 5.16162870e-158, 6.35775829e-224, 2.09237676e-287,0.00000000e+000, 0.00000000e+000]))
# 氨氮 (array([ 315.72998812,  511.10160698,  656.91735661,  784.39497095,915.50344764, 1033.32598981]),
#     array([1.23316599e-070, 1.03680289e-111, 4.60854164e-142, 1.84249778e-168,1.17404137e-195, 5.53577175e-220]))
# 溶解氧 (array([268.00450576, 374.29955396, 441.49727004, 544.09794878,724.13442503, 925.78149296]),
#      array([3.08904614e-060, 5.27089747e-082, 2.26709835e-095, 1.93585206e-116,2.96860973e-154, 1.00208952e-196]))
# 总磷 (array([318.9437151 , 544.50646471, 698.97356721, 805.5627283 ,878.82555026, 923.85753395]),
#     array([2.46027770e-071, 5.77994237e-119, 3.50436088e-151, 4.79095847e-173,1.01767941e-187, 2.61147480e-196]))
# 高锰酸盐 (array([239.1505246 , 335.8139051 , 383.23797214, 432.94801302,520.67331774, 638.81793314]),
#       array([6.02463054e-054, 1.19932540e-073, 9.45659676e-083, 2.10834099e-092,2.75037746e-110, 9.83630315e-135]))
