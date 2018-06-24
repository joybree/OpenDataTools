# encoding: utf-8

from opendatatools import stock
import pandas as pd
 
df1, msg1 = stock.get_report_data('300124.SZ', type='资产负债表')
df2, msg2 = stock.get_report_data('300124.SZ', type='利润表')
df3, msg3 = stock.get_report_data('300124.SZ', type='现金流量表')
 
df1.to_csv("E:/Python/OpenDataTools/data/report1.csv", encoding='GB2312')
df2.to_csv("E:/Python/OpenDataTools/data/report2.csv", encoding='GB2312')
df3.to_csv("E:/Python/OpenDataTools/data/report3.csv", encoding='GB2312')



import pandas as pd
from progressbar import ProgressBar

def analyze_pledge_info(market='SZ', date='2018-06-21'):

    df_total, df_detail = stock.get_pledge_info(market, date='2018-06-21')

    data = []
    progress_bar = ProgressBar().start(max_value=len(df_detail))
    
    for index, row in df_detail.iterrows():
        progress_bar.update(index+1)
        symbol = str(row['证券代码']) + '.' + market

        if market == 'SZ':
            pledge_share = float(row['待购回无限售条件证券余量'].replace(',', '')) + float(row['待购回有限售条件证券余量'].replace(',',''))
        else:
            pledge_share = float(row['待购回余量（股/份/张）'].replace(',', ''))

        df, msg = stock.get_shareholder_structure(symbol)
        if df is None:
            #print('error occurs on ', symbol)
            continue

        total_share    = float(df[df.indicator == '总股本'].iloc[0, 1].replace(',', ''))
        tradable_share = float(df[df.indicator == '流通股'].iloc[0, 1].replace(',', ''))

        data.append({'symbol': symbol, 'total_share' : total_share, 'tradable_share' : tradable_share, 'pledge_share' : pledge_share, 'pledge_ratio' : pledge_share / total_share })

    df = pd.DataFrame(data)
    
    return df

df_sh = analyze_pledge_info('SH', '2018-06-21')
df_sz = analyze_pledge_info('SZ', '2018-06-21')

df = pd.concat([df_sh, df_sz])

df.sort_values('pledge_ratio', ascending=False, inplace=True)
df.head(20)	