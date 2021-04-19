import numpy as np
import pandas as pd

file = 'D:/Work/Project/12SKX/00DataAnalysis/2020/Return/return-2020-03.csv'
SKUfile = 'D:/Work/Project/12SKX/SKX Data/DataMaster/SKUDataMaster.csv'

df = pd.read_csv(file)
df.drop(df[df['QTYIN']<=0].index, inplace=True)

sku = pd.read_csv(SKUfile)

save_path = 'D:/Work/Project/12SKX/00DataAnalysis/2020/Return_bySKU'

df.loc[df['CATEGORY'] == 'ACC', ['CATEGORY']] = 'APP'

df = pd.merge(df, sku, on='SKU', how='left')

df.loc[(df['fullCaseUnits'].isna()) & (df['CATEGORY'] == 'FTW'), ['fullCaseUnits']] = 6
df.loc[(df['fullCaseUnits'].isna()) & (df['CATEGORY'] != 'FTW'), ['fullCaseUnits']] = 28

SKUbyDate = pd.pivot_table(df, index=['CATEGORY','GENDER', 'SKU', 'fullCaseUnits'],
                    columns='DATEIN', values='QTYIN', aggfunc='sum', fill_value=0).reset_index()

# print(SKUbyDate.head(5))

# print(SKUbyDate.columns)
date = SKUbyDate.columns[4:]
N = len(date)

# 2-days duration
print("2Day calculation start!")
print('*'*30)
sku_2day_qty = SKUbyDate[['CATEGORY','GENDER', 'SKU', 'fullCaseUnits']].copy()
sku_2day_qty2case = SKUbyDate[['CATEGORY','GENDER', 'SKU', 'fullCaseUnits']].copy()
for i in range(N-1):
    col = date[i] + '~' + date[i+1]
    print(col)
    sku_2day_qty[col] = SKUbyDate[date[i]] + SKUbyDate[date[i+1]]
    sku_2day_qty2case[col] = np.floor((SKUbyDate[date[i]] + SKUbyDate[date[i+1]])/SKUbyDate['fullCaseUnits']) * SKUbyDate['fullCaseUnits']

# print(sku_2day_qty.head(5))

# 3-days duration
print("3Day calculation start!")
print('*'*30)
sku_3day_qty = SKUbyDate[['CATEGORY','GENDER', 'SKU', 'fullCaseUnits']].copy()
sku_3day_qty2case = SKUbyDate[['CATEGORY','GENDER', 'SKU', 'fullCaseUnits']].copy()
for i in range(N-2):
    col = date[i] + '~' + date[i+2]
    print(col)
    sku_3day_qty[col] = SKUbyDate[date[i]] + SKUbyDate[date[i+1]] + SKUbyDate[date[i+2]]
    sku_3day_qty2case[col] = np.floor((SKUbyDate[date[i]] + SKUbyDate[date[i+1]] + SKUbyDate[date[i+2]])/SKUbyDate['fullCaseUnits']) \
                             * SKUbyDate['fullCaseUnits']

# print(sku_3day_qty.head(5))


### 将结果写入文件
write = pd.ExcelWriter('{}/return_03.xlsx'.format(save_path))

SKUbyDate.to_excel(write, sheet_name='SKUbyDate', index=False)
sku_2day_qty.to_excel(write, sheet_name='sku_2day_qty', index=False)
sku_2day_qty2case.to_excel(write, sheet_name='sku_2day_qty2case', index=False)
sku_3day_qty.to_excel(write, sheet_name='sku_3day_qty', index=False)
sku_3day_qty2case.to_excel(write, sheet_name='sku_3day_qty2case', index=False)

write.close()
write.save()


