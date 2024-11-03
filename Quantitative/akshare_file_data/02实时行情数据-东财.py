import akshare as ak
from datetime import datetime

'''
序号	int64	-
代码	object	-
名称	object	-
最新价	float64	-
涨跌幅	float64	注意单位: %
涨跌额	float64	-
成交量	float64	注意单位: 手
成交额	float64	注意单位: 元
振幅	float64	注意单位: %
最高	float64	-
最低	float64	-
今开	float64	-
昨收	float64	-
量比	float64	-
换手率	float64	注意单位: %
市盈率-动态	float64	-
市净率	float64	-
总市值	float64	注意单位: 元
流通市值	float64	注意单位: 元
涨速	float64	-
5分钟涨跌	float64	注意单位: %
60日涨跌幅	float64	注意单位: %
年初至今涨跌幅	float64	注意单位: %
'''


current_date = datetime.now().strftime('%Y-%m-%d')

def func():
    df = ak.stock_zh_a_spot_em()

    df['日期']= current_date

    df['流通市值']=df['流通市值'].fillna(0).astype(int)
    df['总市值']=df['总市值'].fillna(0).astype(int)

    df[['日期','代码','名称','最新价','涨跌幅','涨跌额','最高','最低','今开','昨收','量比','换手率','市盈率-动态','市净率','总市值','流通市值']].to_csv('stock_zh_a_spot.txt',sep='|',header=False,index=False)

func()