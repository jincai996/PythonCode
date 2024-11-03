import akshare as ak
import time
from datetime import datetime
from dateutil.parser import parse

'''
股票代码    000001
股票简称    平安银行
总股本      19405918198.0
流通股      19405617528.0
总市值      227631420462.540009
流通市值    227627893603.440002
行业        银行
上市时间    19910403
'''
def func1(code):
    df = ak.stock_individual_info_em(symbol=code)

    return f'{df.iloc[0].value}|{df.iloc[1].value}|{int(df.iloc[2].value)}|{int(df.iloc[3].value)}|{round(df.iloc[4].value,2)}|{round(df.iloc[5].value,2)}|{df.iloc[6].value}|{parse(str(df.iloc[7].value)).date()}'

'''
获取全部股票代码
'''
def func2():
    df = ak.stock_zh_a_spot_em()

    code=df[['代码']].values.tolist()

    return [i[0] for i in code]

codelist=func2()

current_date = datetime.now().strftime('%Y-%m-%d')


with open('01stock_individual_info.txt',mode='a+',encoding='utf8') as f: #个股信息查询
    for code in codelist:
        try:
            result=func1(code)
        except Exception as e:
            print(e)
        else:
            f.write(f'{current_date}|{result}\n')

