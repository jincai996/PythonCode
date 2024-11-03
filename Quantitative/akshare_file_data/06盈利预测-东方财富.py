import akshare as ak

'''
序号	int64	-
代码	object	-
名称	object	-
研报数	int64	-
机构投资评级(近六个月)-买入	float64	-
机构投资评级(近六个月)-增持	float64	-
机构投资评级(近六个月)-中性	float64	-
机构投资评级(近六个月)-减持	int64	-
机构投资评级(近六个月)-卖出	int64	-
xxxx预测每股收益	float64	-
xxxx预测每股收益	float64	-
xxxx预测每股收益	float64	-
xxxx预测每股收益	float64	-
'''
# df = ak.stock_profit_forecast_em()
# df[['代码','名称','研报数','2023预测每股收益','2024预测每股收益','2025预测每股收益','2026预测每股收益']].to_csv(f'06stock_profit_forecast.txt',sep='|',header=False,index=False)

def func():
    df = ak.stock_profit_forecast_em()

    df['2023预测每股收益']=df['2023预测每股收益'].fillna(0).round(2)
    df['2024预测每股收益']=df['2024预测每股收益'].fillna(0).round(2)
    df['2025预测每股收益']=df['2025预测每股收益'].fillna(0).round(2)
    df['2026预测每股收益']=df['2026预测每股收益'].fillna(0).round(2)

    df[['代码','名称','研报数','2023预测每股收益','2024预测每股收益','2025预测每股收益','2026预测每股收益']].to_csv(f'06stock_profit_forecast.txt',sep='|',header=False,index=False)

func()