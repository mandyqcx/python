# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import tushare as ts

data = ts.get_hist_data('sz50',start='2016-11-01',end='2016-12-30')
data = data.sort_index()

x = range(len(data))
# 收盘价的折线图
plt.plot(x,data['close'])
plt.show()


