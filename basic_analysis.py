# -*- coding: utf-8 -*-

import xlrd
import pandas as pd
import datetime


def merge_daily_stock():
    # 修改地方一:所要合并sheet的excel所在位置,绝对位置 or 相对位置
    excel_name = 'D:/Work/Project/09蜜思肤/data_1124/daily_stock.xlsx'
    wb = xlrd.open_workbook(excel_name)
    sheets = wb.sheet_names()  # 获取workbook中所有的表格
    # 循环遍历所有sheet
    data = pd.DataFrame()
    for i in range(len(sheets)):
        df = pd.read_excel(excel_name, sheet_name=i, index=False, encoding='utf8')
        df['date'] = '2020/10/{}'.format(i+1)
        data = data.append(df)

    # 修改地方二:合并后的数据要放在哪个excel里
    writer = pd.ExcelWriter('D:/Work/Project/09蜜思肤/data_1124/Oct_stock.xlsx')

    # 指定合并后的数据放在哪个sheet里
    # 修改地方三:合并后的数据放在名为ALLDATA的sheet表里,这个名字自定义的,指定的excel里没有这个sheet的话,会自动创建的
    # 更新序号
    data.index = range(1, len(data) + 1)
    data.index.name = '序号'
    data.to_excel(excel_writer=writer, sheet_name='ALL')
    writer.save()
    writer.close()
    print('Data merge complete!')


def outbound_by_sku(file_path, file_name):
    df = pd.read_excel('{}{}'.format(file_path, file_name))
    if 'date' in list(df.columns):
        sku_qty = pd.pivot_table(df, index=['SKU_ID'], columns=['date'], values=['qty'],
                                 aggfunc='sum')
        sku_qty.columns = sku_qty.columns.get_level_values(1).strftime('%Y-%m-%d')
        sku_qty = sku_qty.reset_index().fillna(0)
    else:
        sku_qty = pd.pivot_table(df, index=['SKU_ID'], values=['qty'], aggfunc='sum')

    # get the qty of date cols
    print(list(sku_qty.columns))
    col_n = len(list(sku_qty.columns))
    date_cols = list(sku_qty.columns)

    sku_ABC = sku_qty['SKU_ID']
    for i in range(1,col_n):
        print(str(date_cols[i]))
        date_df = sku_qty[['SKU_ID', str(date_cols[i])]]
        date_ABC = classify_ABC(date_df)
        sku_ABC = pd.merge(sku_ABC, date_ABC, on=['SKU_ID'], how='left')


    # 添加ABC的计数
    sku_ABC_count = sku_ABC.drop('SKU_ID', axis=1).apply(pd.value_counts)
    # 添加累计值
    sku_ABC_count.loc['All'] = sku_ABC_count.apply(lambda x: x.sum())

    time = datetime.datetime.now()
    str_time = time.strftime('%Y_%m_%d_%H_%M')

    writer = pd.ExcelWriter('{}outbound_ABC_{}.xlsx'.format(file_path, str_time))
    sku_qty.to_excel(writer, sheet_name='01-outbound_qty')
    sku_ABC.to_excel(writer, sheet_name='02-outbound_ABC')
    sku_ABC_count.to_excel(writer, sheet_name='03-ABC_count')
    writer.save()
    writer.close()


def classify_ABC(data, class_num = 4):
    # ABC划分依据
    c = ['A', 'B', 'C', 'Z']
    ratio = [0.7, 0.9, 1]
    if class_num >4:
        c = ['1SA', '20A', '30B', '40C', '50Z']
        ratio = [0.2, 0.5, 0.8, 1]

    org_col = list(data.columns)
    date_col = org_col[1]
    data.columns = ['SKU_ID', 'qty']

    data['qty_rate'] = data['qty'] / data['qty'].sum()
    data['qty_rank'] = data['qty_rate'].rank(ascending=False, method='first')
    data[org_col[1]] = c[-1]

    for index, row in data.iterrows():
        cumu_rate = data[(data['qty_rank'] <= row['qty_rank'])]['qty_rate'].sum()
        if row['qty'] == 0:
            data.loc[index, [date_col]] = c[-1]
        elif row['qty_rank'] == 1:
            data.loc[index, [date_col]] = c[0]
        elif cumu_rate <= ratio[0]:
            data.loc[index, [date_col]] = c[0]
        elif cumu_rate <= ratio[1]:
            data.loc[index, [date_col]] = c[1]
        elif cumu_rate <= ratio[2]:
            data.loc[index, [date_col]] = c[2]
        elif class_num >4 and cumu_rate <= ratio[3]:
            data.loc[index, [date_col]] = c[3]

    return data[['SKU_ID', date_col]]


if __name__ == '__main__':
    # merge_daily_stock()
    file_path = 'D:/Work/Project/09蜜思肤/data_1124/'
    outbound_file = 'outbound.xlsx'
    outbound_by_sku(file_path, outbound_file)