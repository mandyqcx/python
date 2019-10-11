# -*- encoding: utf-8 -*-
#adf单位根检验

import psycopg2,sys
import pandas,numpy
import matplotlib.pyplot as plt
import matplotlib as mpl
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller as adf

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
       print(wdp_mode[key],adf(value['data_value']))
       mpl.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文
       mpl.rcParams['axes.unicode_minus'] = False
       # plt.title(wdp_mode[key]) # 显示图标题
       # plt.show()
    return 0


if __name__ == '__main__':
    sys.exit(draw_picture())
    #sys.exit(get_data())




# 水温 (-2.451932005635708, 0.12761196289419546, 13, 478, {'1%': -3.4441047380903007, '5%': -2.867605550172837, '10%': -2.570000704119326}, 1807.654524367346)
# a 氨氮 (-4.058965636112388, 0.0011313516337095552, 9, 482, {'1%': -3.4439899743408136, '5%': -2.8675550551408353, '10%': -2.569973792117904}, 438.757518126213)
# 溶解氧 (-1.3580081321138535, 0.6022339069628649, 18, 473, {'1%': -3.444250937448703, '5%': -2.867669873870454, '10%': -2.5700349866579657}, 1326.0338711948646)
# a 总磷 (-6.36484257155851, 2.42413406192547e-08, 1, 490, {'1%': -3.4437660979098843, '5%': -2.8674565460819896, '10%': -2.569921291128696}, -792.6123072329788)
# a 高锰酸盐 (-2.985900519271752, 0.03623225890261539, 12, 479, {'1%': -3.44407586647939, '5%': -2.867592847097137, '10%': -2.5699939338217668}, 1612.844249750357)
