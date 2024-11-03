import akshare as ak
from datetime import datetime,timedelta
import pandas as pd

'''
关键词	object	-
新闻标题	object	-
新闻内容	object	-
发布时间	object	-
文章来源	object	-
新闻链接	object	-
'''


def func1(symbol):
    '''
        获取单只股票新闻
    '''
    # 获取A股数据
    df = ak.stock_news_em(symbol=symbol)

    # 去掉时分秒
    df['发布时间'] = pd.to_datetime(df['发布时间']).dt.date
    
    df[['关键词','新闻标题', '新闻内容', '发布时间', '文章来源']].to_csv(f'04stock_news_{symbol}.txt',sep='|',header=False,index=False)


def func2():
    df = ak.stock_zh_a_spot_em()

    code=df[['代码']].values.tolist()

    return [i[0] for i in code]

codelist=func2()

for code in codelist:
    try:
        result=func1(code)
    except Exception as e:
        print(e)
