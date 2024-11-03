import akshare as ak

'''
序号	int64	-
板块	object	-
涨跌幅	object	注意单位: %
总成交量	float64	注意单位: 万手
总成交额	float64	注意单位: 亿元
净流入	float64	注意单位: 亿元
均价	float64	-
'''
def func():
    df = ak.stock_board_industry_summary_ths()

    df['总成交量']=df['总成交量'].fillna(0).astype(int)

    df['总成交额']=df['总成交额'].fillna(0).astype(int)

    df[['板块','涨跌幅','总成交量', '总成交额', '净流入', '均价']].to_csv(f'07stock_board_industry_summary_ths.txt',sep='|',header=False,index=False)

func()


