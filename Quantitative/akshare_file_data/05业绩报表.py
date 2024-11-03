import akshare as ak
'''
序号	int64	-
股票代码	object	-
股票简称	object	-
每股收益	float64	注意单位: 元
营业收入-营业收入	float64	注意单位: 元
营业收入-同比增长	float64	注意单位: %
营业收入-季度环比增长	float64	注意单位: %
净利润-净利润	float64	注意单位: 元
净利润-同比增长	float64	注意单位: %
净利润-季度环比增长	float64	注意单位: %
每股净资产	float64	注意单位: 元
净资产收益率	float64	注意单位: %
每股经营现金流量	float64	注意单位: 元
销售毛利率	float64	注意单位: %
所处行业	object	-
最新公告日期	object	
'''

def func(announce_date):
    '''
        获取单只股票的每日数据
    '''
    df = ak.stock_yjbb_em(announce_date)

    df['每股收益']=df['每股收益'].fillna(0).astype(int).round(2)

    df[['股票代码','股票简称','每股收益', '营业收入-营业收入','净利润-净利润', '所处行业','最新公告日期']].to_csv(f'05stock_yjbb_{announce_date}.txt',sep='|',header=False,index=False)


announce_list=['20200331','20200630','20200930','20201231',
               '20210331','20210630','20210930','20201231',
               '20220331','20220630','20220930','20201231',
               '20230331','20230630','20230930','20201231',
               '20240331','20240630','20240930']

for date in announce_list:
    try:
        func(date)
    except Exception as e:
        print(e)