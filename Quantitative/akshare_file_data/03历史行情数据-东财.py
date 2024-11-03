import akshare as ak
from datetime import datetime,timedelta

'''
日期	object	交易日
股票代码	object	不带市场标识的股票代码
开盘	float64	开盘价
收盘	float64	收盘价
最高	float64	最高价
最低	float64	最低价
成交量	int64	注意单位: 手
成交额	float64	注意单位: 元
振幅	float64	注意单位: %
涨跌幅	float64	注意单位: %
涨跌额	float64	注意单位: 元
换手率	float64	注意单位: %
'''
# 获取当前日期
current_date = datetime.now()

last_year = current_date - timedelta(days=365*3)

# 格式化为YYYYMMDD格式
start_date=last_year.strftime('%Y%m%d')

end_date=current_date.strftime('%Y%m%d')


def func1(symbol,v_start_date,v_end_date):
    '''
        获取单只股票的每日数据
    '''
    # 获取A股数据
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=v_start_date, end_date=v_end_date, adjust="hfq")

    # 添加股票代码列
    df['股票代码']=f'{symbol}'

    df['成交量']=df['成交量'].fillna(0).astype(int)
    df['成交额']=df['成交额'].fillna(0).astype(int)

    df[['股票代码','日期', '开盘', '收盘', '最高', '最低','成交量','成交额','振幅','涨跌幅','涨跌额','换手率']].to_csv(f'03stock_zh_a_hist_{symbol}.txt',sep='|',header=False,index=False)


def func2():
    df = ak.stock_zh_a_spot_em()

    code=df[['代码']].values.tolist()

    return [i[0] for i in code]

codelist=func2()

for code in codelist:
    try:
        func1(code,start_date,end_date)
    except Exception as e:
        print(e)