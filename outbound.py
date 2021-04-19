# -*- coding: utf-8 -*-
# coding: utf-8

import os
import numpy as np
import pandas as pd
import datetime


def data_clean(folder_path, save_path):
    # 修改当前工作目录
    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound/raw_data'

    os.chdir(folder_path)
    # 将该文件夹下的所有文件名存入一个列表
    file_list = os.listdir()

    # print('Month', 'file_name', 'all_record', 'valid_record', 'orderNum', 'SKU' ,'Qty')

    for i in range(len(file_list)):
        # file_name = 'ob_2020-01.csv'
        a = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding='gbk', low_memory=False)

        # 修改channel列 ‘Ship-to Consumer’
        a.loc[a['CHANNEL'] == 'Ship-to Consumer (i.e. Tmall, JD, etc.)', ['CHANNEL']] = 'Ship-to Consumer'

        row1 = a.shape[0]

        # 删除qty<=0的行
        a.drop(a[a['QTY'] <= 0].index, inplace=True)
        row2 = a.shape[0]
        orderNum = a['DOCNO'].nunique()
        sku = a['SKU'].nunique()
        qty = a['QTY'].sum()
        print(i + 1, file_list[i], row1, row2, orderNum, sku, qty)

        a.to_csv('{}/{}'.format(save_path, file_list[i]), encoding='gbk', index=False)


def outbound_by_date(folder_path, save_path, index=None):
    if index is None:
        index = ['DATEOUT']

    save_file_name = 'order_by_' + '_'.join(index) + '.csv'

    os.chdir(folder_path)
    file_list = os.listdir()  # 将该文件夹下的所有文件名存入一个列表

    for i in range(len(file_list)):
        df = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding='gbk', low_memory=False)
        orderNum = df.groupby(index)['DOCNO'].nunique()
        skuNum = df.groupby(index)['SKU'].nunique()
        orderNum.columns = [index + ['orderNum']]
        skuNum.columns = [index + ['skuNum']]

        total_qty = df.groupby(index).agg(orderLine=pd.NamedAgg(column='DOCNO', aggfunc='count'),
                                          sumQty=pd.NamedAgg(column='QTY', aggfunc='sum')).reset_index()

        dis_count = pd.merge(orderNum, skuNum, on=index, how='outer')
        re = pd.merge(dis_count, total_qty, on=index, how='outer')

        print(i + 1, re.shape[0], re['sumQty'].sum())
        if i > 0:
            re.to_csv('{}/{}'.format(save_path, save_file_name), index=False, header=False, mode='a+')
        else:
            re.to_csv('{}/{}'.format(save_path, save_file_name), index=False)


def order_by_date(folder_path, save_path, index=None):
    if index is None:
        index = ['DATEOUT', 'DOCNO']

    save_file_name = 'order_by_' + '_'.join(index) + '.csv'

    os.chdir(folder_path)
    file_list = os.listdir()  # 将该文件夹下的所有文件名存入一个列表

    for i in range(len(file_list)):
        df = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding='gbk', low_memory=False)
        df['CATE'] = 'FTW'
        df.loc[(df['CATEGORY'] != 'FTW'), ['CATE']] = 'APP'

        # print(file_list[i], '非重复订单数： ', df['DOCNO'].nunique())


        # ### merge order DATA_TYPE, CHANNEL
        type = df[['DATEOUT', 'DOCNO', 'DATA_TYPE', 'CHANNEL']].drop_duplicates().reset_index()


        skuNum = df.groupby(index)['SKU'].nunique()
        qty = df.groupby(index).agg(Qty=pd.NamedAgg(column='QTY', aggfunc='sum'))

        re0 = pd.merge(type, skuNum, on=index, how='outer')
        re = pd.merge(re0, qty, on=index, how='outer')
        # print(re.columns)
        # print(re.head(5))

        re['order_structure'] = np.NAN
        re.loc[(re['SKU'] == 1) & (re['Qty'] == 1), ['order_structure']] ='单品单件'
        re.loc[(re['SKU'] == 1) & (re['Qty'] > 1), ['order_structure']] = '单品多件'
        re.loc[(re['SKU'] > 1) & (re['Qty'] > 1) & (re['SKU']  == re['Qty']), ['order_structure']] = '多品单件'
        re.loc[(re['SKU'] > 1) & (re['Qty'] > 1) & (re['SKU']  != re['Qty']), ['order_structure']] = '多品多件'

        re['order_structure2'] = '单件'
        re.loc[(re['order_structure'] != '单品单件'), ['order_structure2']] = '多件'


        order_cate = pd.pivot_table(df, index=index, columns=['CATE'], values=['QTY'],
                                  aggfunc=sum,fill_value=0)

        # print(order_cate.columns)
        # print(order_cate.head(5))

        col = []
        for j in order_cate.columns:
            j = list(j)
            col.append('_'.join(j))

        order_cate.columns = col
        # print(order_cate.columns)
        order_cate['order_category'] = ''
        order_cate.loc[(order_cate['QTY_APP'] > 0) & (order_cate['QTY_FTW'] >0), ['order_category']] = 'A+F'
        order_cate.loc[(order_cate['QTY_APP'] > 0) & (order_cate['QTY_FTW'] == 0), ['order_category']] = 'A'
        order_cate.loc[(order_cate['QTY_APP'] == 0) & (order_cate['QTY_FTW'] > 0), ['order_category']] = 'F'

        result = pd.merge(re, order_cate, on=index, how='outer')

        print(i + 1, file_list[i], '订单数：', df['DOCNO'].nunique() ,
              '行数：',result.shape[0], '件数：',df['QTY'].sum())
        if i > 0:
            result.to_csv('{}/{}'.format(save_path, save_file_name), index=False,
                          encoding='gbk', header=False, mode='a+')
        else:
            result.to_csv('{}/{}'.format(save_path, save_file_name), encoding='gbk', index=False)


def order_by_month(folder_path, save_path, index=None):
    if index is None:
        index = ['DATEOUT', 'DATA_TYPE', 'CHANNEL']

    save_file_name = 'order_by_' + '_'.join(index) + '.csv'

    os.chdir(folder_path)
    file_list = os.listdir()  # 将该文件夹下的所有文件名存入一个列表

    for i in range(len(file_list)):
        df = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding='gbk', low_memory=False)
        # df['CATE'] = 'FTW'
        # df.loc[(df['CATEGORY'] != 'FTW'), ['CATE']] = 'APP'

        # print(file_list[i], '非重复订单数： ', df['DOCNO'].nunique())


        # ### merge order DATA_TYPE, CHANNEL
        type = df[['DATEOUT', 'DATA_TYPE', 'CHANNEL']].drop_duplicates().reset_index()


        orderNum = df.groupby(index)['DOCNO'].nunique()
        skuNum = df.groupby(index)['SKU'].nunique()
        qty = df.groupby(index).agg(Line=pd.NamedAgg(column='DOCNO', aggfunc='count'),
                                    Qty=pd.NamedAgg(column='QTY', aggfunc='sum'))

        re0 = pd.merge(orderNum, skuNum, on=index, how='outer')
        re = pd.merge(re0, qty, on=index, how='outer').reset_index()


        print(i + 1, re.shape)
        if i > 0:
            re.to_csv('{}/{}'.format(save_path, save_file_name), index=False,
                          encoding='gbk', header=False, mode='a+')
        else:
            re.to_csv('{}/{}'.format(save_path, save_file_name), encoding='gbk', index=False)



def orderABC(folder_path, file_list, save_path, period, rate=None):
    if rate is None:
        rate = [0.8, 0.95, 1]
    class_type = ['A', 'B', 'C']

    df_list = []
    for i in range(len(file_list)):
        t = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding='gbk')
        df_list.append(t)

    df = pd.concat(df_list)
    df['CATE'] = 'FTW'
    df.loc[(df['CATEGORY'] != 'FTW'), ['CATE']] = 'APP'
    df['Period'] = period

    print('all data size: ', df.shape)

    sku = df.groupby('SKU').agg(line=pd.NamedAgg(column='DATEOUT', aggfunc='count'),
                                qty=pd.NamedAgg(column='QTY', aggfunc='sum')).reset_index()
    sku_cate = df[['SKU', 'Period', 'CATE']].drop_duplicates()

    sku = pd.merge(sku_cate, sku, on='SKU', how='left')

    sku_FTW = sku.loc[sku['CATE'] == 'FTW'].copy()
    sku_APP = sku.loc[sku['CATE'] == 'APP'].copy()


    save_file_name = 'skuABC_{}.xlsx'.format(period)
    write = pd.ExcelWriter('{}/{}'.format(save_path, save_file_name))

    skuABC = class_ABC(write, sku, rate, class_type)
    skuABC_FTW = class_ABC(write, sku_FTW, rate, class_type)
    skuABC_APP = class_ABC(write, sku_APP, rate, class_type)

    write.save()
    write.close()


    '''订单ABC组合'''
    ## 订单ABC组合
    skuABC_cate = skuABC_FTW[['SKU', 'lineABC', 'qtyABC']].append(skuABC_APP[['SKU', 'lineABC', 'qtyABC']])

    df = pd.merge(df, skuABC_cate, on='SKU', how='left')
    df_temp = df[['Period','DATEOUT', 'DOCNO', 'DATA_TYPE', 'CHANNEL']].drop_duplicates()

    ## 统计一个订单中SKU 行数ABC的个数
    df_order_lineABC = pd.pivot_table(df, index=['DOCNO'], columns='lineABC',
                                   values='SKU', aggfunc='count', fill_value=0).reset_index()
    print(df_order_lineABC.columns)
    cols = list(df_order_lineABC.columns[1:])
    print(cols)
    x = np.where(df_order_lineABC[cols],cols, '')
    df_order_lineABC['orderLineABC'] = pd.Series(''.join(i) for i in x)


    ## 统计一个订单中SKU 件数ABC的个数
    df_order_qtyABC = pd.pivot_table(df, index=['DOCNO'], columns='qtyABC',
                                      values='SKU', aggfunc='count', fill_value=0).reset_index()
    print(df_order_qtyABC.columns)
    cols = list(df_order_qtyABC.columns[1:])
    print(cols)
    y = np.where(df_order_qtyABC[cols], cols, '')
    df_order_qtyABC['orderQtyABC'] = pd.Series(''.join(i) for i in y)

    # print(df_order_lineABC.head(20))
    # print(df_order_qtyABC.head(20))

    df_order = pd.merge(df_order_lineABC[['DOCNO','orderLineABC']], df_order_qtyABC[['DOCNO','orderQtyABC']],
                        on='DOCNO', how='left')

    df_result = pd.merge(df_temp, df_order, on='DOCNO', how='left')
    # print(df_result.head(20))

    save_file_name = 'orderABC_{}.csv'.format(period)
    df_result.to_csv('{}/{}'.format(save_path, save_file_name), encoding='gbk', index=False)



def sku_ABC_byDate(folder_path, file_list, save_path, period, rate=None, line=True):
    if rate is None:
        rate = [0.8, 0.95, 1]
    if line:
        measure = 'count'
    else:
        measure = 'sum'

    class_type = ['A', 'B', 'C']

    df_list = []
    for i in range(len(file_list)):
        t = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding='gbk')
        df_list.append(t)

    df = pd.concat(df_list)
    df['CATE'] = 'FTW'
    df.loc[(df['CATEGORY'] != 'FTW'), ['CATE']] = 'APP'
    df['Period'] = period

    print('all data size: ', df.shape)

    # sku = df.groupby('SKU').agg(line=pd.NamedAgg(column='DATEOUT', aggfunc='count'),
    #                             qty=pd.NamedAgg(column='QTY', aggfunc='sum')).reset_index()


    # all_date = df['DATEOUT'].unique()

    # df_temp = df[['DATEOUT', 'SKU', 'CATE', 'QTY']]
    # df_temp.columns = ['DATEOUT', 'SKU', 'CATE', 'QTY']
    #
    # df_temp['DATE'] = pd.to_datetime(df_temp['DATEOUT'], format="%Y/%m/%d")


    sku = pd.pivot_table(df, index='SKU', columns='DATEOUT', values='QTY',
                         aggfunc=measure, fill_value=0)

    sku_cate = df[['SKU', 'Period', 'CATE']].drop_duplicates()

    sku = pd.merge(sku_cate, sku, on='SKU', how='left')

    sku_FTW = sku.loc[sku['CATE'] == 'FTW'].copy()
    sku_APP = sku.loc[sku['CATE'] == 'APP'].copy()

    print(sku_FTW.head())
    print(sku_APP.head())

    idx = ['SKU', 'Period', 'CATE']
    n = len(idx)

    sku_FTW_columns = list(sku_FTW.columns)

    date_cols = sku_FTW_columns[n:]

    # FTW ABC
    for i in range(len(date_cols)):
        date = date_cols[i]
        t = sku_FTW[ idx + [date] ]
        ABC_temp = class_ABC(t, idx, rate, class_type, date)
        if i>0:
            all_FTW_ABC = pd.merge(all_FTW_ABC, ABC_temp, on=idx, how='left')
        else:
            all_FTW_ABC = ABC_temp

    # APP ABC
    for i in range(len(date_cols)):
        date = date_cols[i]
        t = sku_APP[idx + [date]]
        ABC_temp = class_ABC(t, idx, rate, class_type, date)
        if i > 0:
            all_APP_ABC = pd.merge(all_APP_ABC, ABC_temp, on=idx, how='left')
        else:
            all_APP_ABC = ABC_temp

    FTW_ABC_cols = list(all_FTW_ABC.columns)
    FTW_count = all_FTW_ABC[ FTW_ABC_cols[n:]].apply(pd.value_counts)

    APP_ABC_cols = list(all_APP_ABC.columns)
    APP_count = all_APP_ABC[APP_ABC_cols[n:]].apply(pd.value_counts)

    print(FTW_count)
    print(APP_count)

    save_file_name = 'skuABC_{}.xlsx'.format(period)
    write = pd.ExcelWriter('{}/{}'.format(save_path, save_file_name))

    # print(all_FTW_ABC.columns)
    all_FTW_ABC.index = range(1, len(all_FTW_ABC) + 1)
    all_APP_ABC.index = range(1, len(all_APP_ABC) + 1)


    all_FTW_ABC.to_excel(write, sheet_name='FTW_ABC')
    all_APP_ABC.to_excel(write, sheet_name='APP_ABC')
    FTW_count.to_excel(write, sheet_name='FTW_count')
    APP_count.to_excel(write, sheet_name='APP_count')

    write.save()
    write.close()


def class_ABC(sku, index, rate=None, class_type=None, col=None):
    if rate is None:
        rate = [0.8, 0.95, 1]
    if class_type is None:
        class_type = ['A', 'B', 'C']
    if col is None:
        col = 'line'

    sku.sort_values(by=col, ascending=False, inplace=True, ignore_index=True)
    sku['{}_rate'.format(col)] = sku[col] / sku[col].sum()
    sku['{}_rate_cumu'.format(col)] = sku['{}_rate'.format(col)].cumsum()
    sku.loc[(sku['{}_rate_cumu'.format(col)] >1), ['{}_rate_cumu'.format(col)]] = 1

    # sku.sort_values(by='qty', ascending=False, inplace=True, ignore_index=True)
    # sku['qty_rate'] = sku['qty'] / sku['qty'].sum()
    # sku['qty_rate_cumu'] = sku['qty_rate'].cumsum()
    # sku.loc[(sku['qty_rate_cumu'] > 1), ['qty_rate_cumu']] = 1
    # sku['qtyABC'] = np.NAN

    sku['{}_ABC'.format(col)] = np.NAN

    for i in range(len(rate)):
        sku.loc[(sku['{}_rate_cumu'.format(col)] <= rate[i]) & (sku['{}_ABC'.format(col)].isna()),
                ['{}_ABC'.format(col)]] = class_type[i]

    sku.loc[(sku[col] == 0), ['{}_ABC'.format(col)]] = 'D'
        # sku.loc[(sku['qty_rate_cumu'] <= rate[i]) & (sku['qtyABC'].isna()), ['qtyABC']] = class_type[i]

    # print('all sku size: ', sku.shape)
    # print(sku.head(5))

    # cate = list(sku['CATE'].unique())

    # sku.to_excel(write, sheet_name='skuABC_{}'.format('_'.join(cate)), index=False)

    return sku[ index + ['{}_ABC'.format(col)]]


def sku_qty2case(file_name, sku_detail, save_path, period, index=None):
    if index is None:
        index = ['DATA_TYPE', 'DATEOUT', 'SKU']


    df = pd.read_csv(file_name, encoding='gbk')
    df['CATE'] = 'FTW'
    df.loc[(df['CATEGORY'] != 'FTW'), ['CATE']] = 'APP'
    cate = df[['SKU', 'CATE']].drop_duplicates()
    print('cate: ', cate.shape)

    sku_all = pd.read_excel(sku_detail)

    print('all data size: ', df.shape)

    sku_qty = df.groupby(index).agg(line=pd.NamedAgg(column='DATEOUT', aggfunc='count'),
                                qty=pd.NamedAgg(column='QTY', aggfunc='sum')).reset_index()
    temp = pd.merge(sku_qty, cate, on='SKU', how='left')

    sku = pd.merge(temp, sku_all[['SKU', 'fullCaseUnits']], on='SKU', how='left')

    # fill none where units_per_case is None
    sku.loc[(sku['fullCaseUnits'].isna()) & (sku['CATE'] == 'FTW'), ['fullCaseUnits']] = 6
    sku.loc[(sku['fullCaseUnits'].isna()) & (sku['CATE'] == 'APP') , ['fullCaseUnits']] = 28


    sku['caseNum'] = round(sku['qty'] / sku['fullCaseUnits'], 2)
    sku['fullCaseNum'] = np.floor(sku['qty'] / sku['fullCaseUnits'])
    sku['pcs'] = sku['qty'] - sku['fullCaseNum']*sku['fullCaseUnits']

    print(sku.head(20))
    print('SKU size: ', sku.shape)

    save_file_name = '{}/skuCase_{}.csv'.format(save_path, period)
    sku.to_csv(save_file_name, encoding='gbk', index=False)


if __name__ == '__main__':
    time1 = datetime.datetime.now()

    ### 清洗outbound数据
    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound/raw_data'
    # save_path = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound/new_data'
    # data_clean(folder_path, save_path)

    ### order detail by date
    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound/new_data'
    # save_path = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound'
    # outbound_by_date(folder_path, save_path, index=['DATEOUT'])


    # Q1 = ['ob_2020-01.csv', 'ob_2020-02.csv', 'ob_2020-03.csv']
    # Q2 = ['ob_2020-04.csv', 'ob_2020-05.csv', 'ob_2020-06.csv']
    # Q3 = ['ob_2020-07.csv', 'ob_2020-08.csv', 'ob_2020-09.csv']
    # Q4 = ['ob_2020-10.csv', 'ob_2020-11.csv', 'ob_2020-12.csv']
    #
    # sku_ABC(folder_path, Q1, save_path, 'Q1')

    # file_name = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound/new_data/ob_2020-01.csv'
    # sku_detail = 'D:/Work/Project/12SKX/Data/DataMaster/SKUDataMaster.xlsx'
    #
    # sku_qty2case(file_name=file_name, sku_detail=sku_detail, save_path=save_path, period='01')


    ### -----2019---------------
    ### ------------------------

    ### 2019 data clean
    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/2019/2019 outbound'
    # save_path = 'D:/Work/Project/12SKX/00DataAnalysis/2019/outbound_new'
    # data_clean(folder_path, save_path)

    ### order detail by date 2019
    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/2019/outbound_new'
    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/Outbound/new_data'
    # save_path = 'D:/Work/Project/12SKX/00DataAnalysis/2019'
    # # # outbound_by_date(folder_path, save_path, index=['DATEOUT'])
    # #
    # order_by_date(folder_path, save_path, index=['DATEOUT', 'DOCNO'])



    # folder_path = 'D:/Work/Project/12SKX/00DataAnalysis/2019/outbound_new'
    # save_path = 'D:/Work/Project/12SKX/00DataAnalysis/2019/skuABC'

    # Q1 = ['ob_2019-01.csv', 'ob_2019-02.csv', 'ob_2019-03.csv']
    # Q2 = ['ob_2019-04.csv', 'ob_2019-05.csv', 'ob_2019-06.csv']
    # Q3 = ['ob_2019-07.csv', 'ob_2019-08.csv', 'ob_2019-09.csv']
    # Q4 = ['ob_2019-10.csv', 'ob_2019-11.csv', 'ob_2019-12.csv']
    #
    # orderABC(folder_path, Q4, save_path, 'Q4')
    #
    # M1 = ['ob_2019-01.csv']
    # sku_ABC_byDate(folder_path, M1, save_path, 'M1')


    ### 2021-02-03 check the JITX 2020.02

    # DATA CLEANING
    # folder_path = 'F:/SKX/SourceData/2020.02-12 ECOM OB updated'
    # save_path = 'F:/SKX/SourceData/2020 ECOM updated'

    # data_clean(folder_path, save_path)

    ### check JITX+JIT 大数
    folder_path = 'F:/SKX/SourceData/2020 ECOM ob updated'
    save_path = 'F:/SKX/SourceData/2020 ECOM outbound update JITX results'

    # index = ['DATEOUT', 'DATA_TYPE', 'CHANNEL']
    # order_by_month(folder_path, save_path, index=index)

    order_by_date(folder_path, save_path)


    time2 = datetime.datetime.now()
    print('running time: {} S'.format((time2 - time1).seconds))
