import numpy as np
import pandas as pd


def storageABC():
    fold = 'D:/Work/Project/12SKX/00DataAnalysis/Inv_ABC'

    inv_file = '{}/inv_month_end.csv'.format(fold)
    sku_file = '{}/skuABC.xlsx'.format(fold)

    inv = pd.read_csv(inv_file)
    sku = pd.read_excel(sku_file)

    ## 清除库存小于0的数据
    inv.drop(inv[inv['QTY'] <= 0].index, inplace=True)

    inv.columns = ['INV_DATE', 'BUSINESS_CHANNEL', 'STYLE', 'COLOR', 'SIZE',
                   'SKU', 'CATE', 'GENDER', 'INV_QTY']


    inv.loc[(inv['CATE'] != 'Footwear'), 'CATE'] = 'APP'
    inv.loc[(inv['CATE'] == 'Footwear'), 'CATE'] = 'FTW'

    inv['Year'] = inv['INV_DATE'].apply(lambda x: x[:4])
    inv['Month'] = inv['INV_DATE'].apply(lambda x: x[5:7])

    inv['Period'] = ''

    inv.loc[(inv['Month'] == '01') | (inv['Month'] == '02') | (inv['Month'] == '03'), 'Period'] = 'Q1'
    inv.loc[(inv['Month'] == '04') | (inv['Month'] == '05') | (inv['Month'] == '06'), 'Period'] = 'Q2'
    inv.loc[(inv['Month'] == '07') | (inv['Month'] == '08') | (inv['Month'] == '09'), 'Period'] = 'Q3'
    inv.loc[(inv['Month'] == '10') | (inv['Month'] == '11') | (inv['Month'] == '12'), 'Period'] = 'Q4'


    sku['Year'] = sku['Year'].astype(str)

    re = pd.merge(inv, sku, on=['SKU', 'Year', 'Period', 'CATE'], how='left')

    sku_detail_file = 'D:/Work/Project/12SKX/SKX Data/DataMaster/SKUDataMaster.xlsx'
    sku_detail = pd.read_excel(sku_detail_file)

    re = pd.merge(re, sku_detail[['SKU', 'Units per case']], on='SKU', how='left')

    re.loc[(re['Units per case'].isna()) & (re['CATE'] == 'FTW'), ['Units per case']] = 6
    re.loc[(re['Units per case'].isna()) & (re['CATE'] == 'FTW') &
           (re['GENDER_EN'] == 'UNISEX-KIDS'), ['Units per case']] = 12

    re.loc[(re['Units per case'].isna()) & (re['CATE'] != 'FTW'), ['Units per case']] = 28

    re['Case'] = re['INV_QTY'] / re['Units per case']

    index = ['Period', 'INV_DATE', 'lineABC']
    pt = pd.pivot_table(re, index=index, values=['SKU', 'INV_QTY', 'Case'],
                        aggfunc={'SKU': len, 'INV_QTY':np.sum, 'Case':np.sum}).reset_index()

    re.to_csv('{}/InvABC_source.csv'.format(fold), index=False)
    pt.to_csv('{}/InvABC_results.csv'.format(fold), index=False)