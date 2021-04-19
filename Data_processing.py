# -*- coding: utf-8 -*-
# coding: utf-8

import os
import numpy as np
import pandas as pd
import datetime

class Config:
    def __init__(self):
        self.QTY_CLASS_INTERVAL = [0, 1, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
        self.QTY_CLASS = []

        # PARM2 P&C分级,区间端点
        # self.TOTE_CLASS_INTERVAL = [0, 0.5, 1, 2, 5, 7, 10]
        self.PLT_CLASS_INTERVAL = [0, 0.5, 1, 2, 5]
        self.CTN_QTY_INTERVAL = [0, 3, 8, 10]
        self.CTN_QTY_CLASS = []
        self.PC_CLASS = []

        # PARM2 days Class 区间
        self.DAYS_CLASS_INTERVAL = [0, 1, 5, 10, 20, 31]
        self.DAYS_CLASS = []

    def get_qty_class(self):
        '''
        PARM2 EN&EQ&IQ&IK Class
        '''

        len_QTY = len(self.QTY_CLASS_INTERVAL)

        for i in range(len_QTY):
            tmp = []
            if i == len_QTY - 1:
                tmp.append("Q" + str(i + 1) + "(" + str(self.QTY_CLASS_INTERVAL[i]) + ",+)")
                tmp.append(self.QTY_CLASS_INTERVAL[i])
                tmp.append(np.inf)
                self.QTY_CLASS.append(tmp)
            elif i < 9:
                tmp.append(
                    "Q0" + str(i + 1) + "(" + str(self.QTY_CLASS_INTERVAL[i]) + "," + str(
                        self.QTY_CLASS_INTERVAL[i + 1]) + "]")
                tmp.append(self.QTY_CLASS_INTERVAL[i])
                tmp.append(self.QTY_CLASS_INTERVAL[i + 1])
                self.QTY_CLASS.append(tmp)
            else:
                tmp.append(
                    "Q" + str(i + 1) + "(" + str(self.QTY_CLASS_INTERVAL[i]) + "," + str(
                        self.QTY_CLASS_INTERVAL[i + 1]) + "]")
                tmp.append(self.QTY_CLASS_INTERVAL[i])
                tmp.append(self.QTY_CLASS_INTERVAL[i + 1])
                self.QTY_CLASS.append(tmp)
        # pprint.pprint(self.QTY_CLASS)

    def get_PC_class(self):
        '''
        PARM2 P&C Class
        '''
        len_PALLET = len(self.PLT_CLASS_INTERVAL)

        rank_num = len_PALLET
        for i in range(rank_num):
            tmp = []
            if i == rank_num - 1:
                tmp.append("P" + str(i + 1) + "(" + str(self.PLT_CLASS_INTERVAL[i]) + ",+)")
                tmp.append(self.PLT_CLASS_INTERVAL[i])
                tmp.append(np.inf)
                # print(tmp)
                self.PC_CLASS.append(tmp)
            else:
                if i < 9:
                    tmp.append(
                        "P0" + str(i  + 1) + "(" + str(self.PLT_CLASS_INTERVAL[i]) + "," + str(
                            self.PLT_CLASS_INTERVAL[i + 1]) + "]")
                    tmp.append(self.PLT_CLASS_INTERVAL[i])
                    tmp.append(self.PLT_CLASS_INTERVAL[i + 1])
                    # print(tmp)
                    self.PC_CLASS.append(tmp)
                else:
                    tmp.append(
                        "P" + str(i + 1) + "(" + str(self.PLT_CLASS_INTERVAL[i]) + "," + str(
                            self.PLT_CLASS_INTERVAL[i + 1]) + "]")
                    tmp.append(self.PLT_CLASS_INTERVAL[i])
                    tmp.append(self.PLT_CLASS_INTERVAL[i + 1])
                    # print(tmp)
                    self.PC_CLASS.append(tmp)
        # pprint.pprint(self.PC_CLASS)

    def get_ctn_qty_class(self):
        """
        整箱数量分级
        :return:
        """
        len_QTY = len(self.CTN_QTY_INTERVAL)

        for i in range(len_QTY):
            tmp = []
            if i == len_QTY - 1:
                tmp.append("C" + str(i + 1) + "(" + str(self.CTN_QTY_INTERVAL[i]) + ",+)")
                tmp.append(self.CTN_QTY_INTERVAL[i])
                tmp.append("+")
                self.CTN_QTY_CLASS.append(tmp)
            elif i < 9:
                tmp.append(
                    "C0" + str(i + 1) + "(" + str(self.CTN_QTY_INTERVAL[i]) + "," + str(
                        self.CTN_QTY_INTERVAL[i + 1]) + "]")
                tmp.append(self.CTN_QTY_INTERVAL[i])
                tmp.append(self.CTN_QTY_INTERVAL[i + 1])
                self.CTN_QTY_CLASS.append(tmp)
            else:
                tmp.append(
                    "C" + str(i + 1) + "(" + str(self.CTN_QTY_INTERVAL[i]) + "," + str(
                        self.CTN_QTY_INTERVAL[i + 1]) + "]")
                tmp.append(self.CTN_QTY_INTERVAL[i])
                tmp.append(self.CTN_QTY_INTERVAL[i + 1])
                self.CTN_QTY_CLASS.append(tmp)
        # pprint.pprint(self.CTN_QTY_CLASS)

    def get_days_class(self):
        '''
        PARM2 DAYS Class
        '''

        len_DAYS = len(self.DAYS_CLASS_INTERVAL)

        for i in range(len_DAYS - 1):
            tmp = []
            if i < 9:
                tmp.append(
                    "D0" + str(i + 1) + "(" + str(self.DAYS_CLASS_INTERVAL[i]) + "," + str(
                        self.DAYS_CLASS_INTERVAL[i + 1]) + "]")
                tmp.append(self.DAYS_CLASS_INTERVAL[i])
                tmp.append(self.DAYS_CLASS_INTERVAL[i + 1])
                self.DAYS_CLASS.append(tmp)
            else:
                tmp.append(
                    "D" + str(i + 1) + "(" + str(self.DAYS_CLASS_INTERVAL[i]) + "," + str(
                        self.DAYS_CLASS_INTERVAL[i + 1]) + "]")
                tmp.append(self.DAYS_CLASS_INTERVAL[i])
                tmp.append(self.DAYS_CLASS_INTERVAL[i + 1])
                self.DAYS_CLASS.append(tmp)

    def run(self):
        self.get_PC_class()
        self.get_ctn_qty_class()
        self.get_qty_class()
        self.get_days_class()


# os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#使用递归去解决
def merge(folder_path,save_file_path, qtyCol, save_file_name):
    '''
    :param folder_path: merge file folder path
    :param save_file_path: save file folder path
    :param save_file_name: save file name
    :return:
    '''

    # 修改当前工作目录
    os.chdir(folder_path)
    # 将该文件夹下的所有文件名存入一个列表
    file_list = os.listdir()
    encoding = 'gbk'

    # 读取第一个CSV文件并包含表头
    df = pd.read_csv('{}/{}'.format(folder_path,file_list[0]), encoding=encoding)  # 编码默认UTF-8，若乱码自行更改
    # print(df)
    rows0 = df.shape[0]
    # 删除库存小于等于0的行
    df.drop(df[df[qtyCol]<=0].index, inplace=True)
    rows = df.shape[0]
    print(1, file_list[0], rows0, rows, df[qtyCol].sum())


    # 将读取的第一个CSV文件写入合并后的文件保存
    df.to_csv('{}/{}'.format(save_file_path, save_file_name), encoding=encoding, index=False)

    # 循环遍历列表中各个CSV文件名，并追加到合并后的文件
    for i in range(1, len(file_list)):
        # print(i, file_list[i])
        df = pd.read_csv('{}/{}'.format(folder_path, file_list[i]), encoding=encoding)
        rows0 = df.shape[0]

        df.drop(df[df[qtyCol] <= 0].index, inplace=True)
        n = df.shape[0]


        print(i+1, file_list[i], rows0, n, df[qtyCol].sum())
        rows += n
        df.to_csv('{}/{}'.format(save_file_path, save_file_name), encoding=encoding,
                  index=False, header=False, mode='a+')
    print('all data rows: ', rows)



def merge_data(path, newFileName):
    big_file = []
    for file in os.listdir(path):
        big_file.append(pd.read_csv(os.path.join(path, file), encoding='ANSI'))
    writer = pd.ExcelWriter('{}{}.xlsx'.format(path,newFileName))
    pd.concat(big_file).to_excel(writer, 'sheet1', index=False)
    writer.close()


def gene_pt(writer, file_folder, file_name_lists, index=None, col=None):

    # cols:INV_DATE	BUSINESS_CHANNEL STYLE_CODE	COLOR_CODE
    # SIZE_NO BARCODE PRODUCT_LINE_EN GENDER_EN	INV_QTY

    # sku_detail  SKU	STYLE	CATEGORY	GENDER	INVENTORY	DESCRIPTION	DIVISION
    # Case Length	Case width	Case height	Case weight	Unit Length	Unit width	Unit Height	Unit weight	Units per case

    # r = pd.merge(df, sku, left_on='BARCODE', right_on=)


    if index is None:
        index = ['INV_DATE']
    else:
        index = index

    for i in range(len(file_name_lists)):

        file_name = file_name_lists[i]

        df = pd.read_csv('{}{}.csv'.format(file_folder, file_name), encoding='gbk')

        # # res = df.groupby(index).agg(sumINV=pd.NamedAgg(column='INV_QTY', aggfunc='sum'),
        #                                  countSKU=pd.NamedAgg(column='BARCODE', aggfunc='count')).reset_index()

        res = pd.pivot_table(df, index=index, values=['INV_QTY', 'BARCODE'],
                             columns= col,
                             aggfunc={'INV_QTY':np.sum, 'BARCODE': len}, margins=True).reset_index()

        res.index = range(1, len(res) + 1)
        # print(res)

        res.to_excel(excel_writer=writer, sheet_name=file_name, encoding='gbk')

        return res



def sku_days(writer, file_folder, file_name_lists):

    df_list = []
    for i in range(len(file_name_lists)):
        file_name = file_name_lists[i]
        t = pd.read_csv('{}{}.csv'.format(file_folder, file_name), encoding='gbk')
        # index = ['BARCODE']
        # col = ['INV_DATE']
        # res = pd.pivot_table(df, index=index, columns=col, values=['INV_QTY'], aggfunc=np.sum).reset_index()
        df_list.append(t)

    df = pd.concat(df_list)
    print(df.shape)

    sku = df.groupby('BARCODE').agg(days=pd.NamedAgg(column='INV_DATE', aggfunc='count'),
                                    maxInv=pd.NamedAgg(column='INV_QTY', aggfunc='max')).reset_index()

    ## 筛选有库存的数据
    df_inv = df[['BARCODE', 'INV_DATE', 'INV_QTY']].where(df['INV_QTY']>0).dropna().reset_index()


    max_day = df_inv.iloc[df_inv.groupby(['BARCODE']).apply(lambda x: x['INV_QTY'].idxmax())]
    print(max_day.head(10))
    print(max_day.shape)

    # 增加max_inv的date
    sku = pd.merge(sku, max_day, left_on=['BARCODE', 'maxInv'],
                   right_on=['BARCODE', 'INV_QTY'], how='left')

    print(sku.columns)
    print(sku.shape)
    sku = sku[['BARCODE', 'days', 'INV_DATE', 'maxInv']]
    sku.columns = ['BARCODE', 'days', 'max_day', 'maxInv']
    print(sku.shape)

    first_day = df_inv.groupby('BARCODE').agg(first_day=pd.NamedAgg(column='INV_DATE', aggfunc='min')).reset_index()
    last_day = df_inv.groupby('BARCODE').agg(last_day=pd.NamedAgg(column='INV_DATE', aggfunc='max')).reset_index()

    first_inv = pd.merge(first_day, df_inv, left_on=['BARCODE', 'first_day'],
                          right_on=['BARCODE', 'INV_DATE'] , how='left').reset_index()
    first_inv = first_inv[['BARCODE', 'first_day', 'INV_QTY']]
    first_inv.columns = ['BARCODE', 'first_day', 'first_INV_QTY']

    last_inv = pd.merge(last_day, df_inv, left_on=['BARCODE', 'last_day'],
                          right_on=['BARCODE', 'INV_DATE'] , how='left')
    last_inv = last_inv[['BARCODE', 'last_day', 'INV_QTY']]
    last_inv.columns = ['BARCODE', 'last_day', 'last_INV_QTY']

    day = pd.merge(first_inv, last_inv, on=['BARCODE'], how='left')
    sku_data = pd.merge(sku, day, on=['BARCODE'], how='left')

    sku_data.to_excel(excel_writer=writer, sheet_name='SKU_days', encoding='gbk')


def load_data_to_class(file_folder, stock_file, sku_detail, date):

    config = Config()
    config.run()

    # print(config.PC_CLASS)
    # print(config.CTN_QTY_CLASS)

    inv = pd.read_csv(stock_file, encoding='gbk')
    inv.drop(inv[inv['INV_QTY'] <= 0].index, inplace=True)
    # inv-cols:INV_DATE	BUSINESS_CHANNEL STYLE_CODE	COLOR_CODE
    # SIZE_NO BARCODE PRODUCT_LINE_EN GENDER_EN	INV_QTY

    inv = inv[['INV_DATE','BUSINESS_CHANNEL', 'BARCODE', 'PRODUCT_LINE_EN',
               'GENDER_EN', 'STYLE_CODE','COLOR_CODE','SIZE_NO', 'INV_QTY']]
    inv.columns = ['INV_DATE','BUSINESS_CHANNEL','SKU_ID', 'PRODUCT_LINE_EN',
                   'GENDER_EN', 'STYLE_CODE','COLOR_CODE','SIZE_NO', 'INV_QTY']

    # 月度日均
    # df = inv[['SKU_ID', 'PRODUCT_LINE_EN','GENDER_EN', 'STYLE_CODE',
    #           'COLOR_CODE','SIZE_NO', 'INV_QTY']].drop_duplicates().reset_index()

    # agv_inv = inv.groupby('SKU_ID').agg(sumQty=pd.NamedAgg(column='INV_QTY', aggfunc='mean')).reset_index()
    # agv_inv = pd.merge(agv_inv, df[[]])


    sku = pd.read_excel(sku_detail)

    sku = sku[[' SKU', 'DESCRIPTION', 'Case Length', 'Case width', 'Case height',
               'Unit Length', 'Unit width', 'Unit Height', 'Unit weight', 'Units per case']]

    sku.columns = ['SKU_ID', 'sku_name', 'ctn_length', 'ctn_width', 'ctn_height',
                   'length', 'width', 'height', 'weight', 'fullCaseUnits']

    sku['ctn_length'] = sku['ctn_length'] * 10
    sku['ctn_width'] = sku['ctn_width'] * 10
    sku['ctn_height'] = sku['ctn_height'] * 10
    sku['length'] = sku['length'] * 10
    sku['width'] = sku['width'] * 10
    sku['height'] = sku['height'] * 10


    df = pd.merge(inv, sku, on='SKU_ID', how='left')

    # 只分FTW/APP
    df['Cate'] = 'FTW'
    df.loc[(df['PRODUCT_LINE_EN'] =='Apparel') | (df['PRODUCT_LINE_EN'] == 'Accessories'), ['Cate']] = 'APP'

    # fill none where units_per_case is None
    df.loc[(df['fullCaseUnits'].isna()) & (df['Cate'] =='FTW'), ['fullCaseUnits']] = 6
    df.loc[(df['fullCaseUnits'].isna()) & (df['Cate'] == 'FTW') &
                                          (df['GENDER_EN'] == 'UNISEX-KIDS'), ['fullCaseUnits']] = 12

    df.loc[(df['fullCaseUnits'].isna()) & (df['Cate'] == 'APP'), ['fullCaseUnits']] = 28


    plt_l = 1200
    plt_w = 1000
    plt_h = 1650

    ## sku码托方式
    # 箱规托盘每层码放箱数
    tmp = df[['SKU_ID', 'ctn_length', 'ctn_width', 'ctn_height']].where(df['ctn_length']>0).dropna().reset_index()

    tmp['max_s'] = tmp[['ctn_length', 'ctn_width']].max(axis=1)
    tmp['min_s'] = tmp[['ctn_length', 'ctn_width']].min(axis=1)

    # type(left) = series
    tmp['left'] = np.floor(plt_l / tmp['max_s']) * np.floor(plt_w / tmp['min_s']) \
           + np.floor((plt_l - np.floor(plt_l / tmp['max_s']) * tmp['max_s']) / tmp['min_s']) * np.floor(plt_w / tmp['max_s'])
    tmp['right'] = np.floor(plt_l / tmp['min_s']) * np.floor(plt_w / tmp['max_s']) \
            + np.floor((plt_w - np.floor(plt_w / tmp['max_s']) * tmp['max_s']) / tmp['min_s']) * np.floor(plt_l / tmp['max_s'])


    tmp['cartons_per_layer'] = tmp[['left', 'right']].max(axis=1)
    tmp['layers'] = np.floor( plt_h / tmp['ctn_height'])

    tmp['ctn_per_plt'] = tmp['cartons_per_layer'] * tmp['layers']

    # sku-ctn/plt
    sku_case = tmp[['SKU_ID', 'ctn_per_plt']].drop_duplicates()

    df = pd.merge(df, sku_case, on='SKU_ID', how='left', sort=False)
    print(df.shape)


    # 匹配不上的用类别均值
    df.loc[(df['ctn_per_plt'].isna()) & (df['Cate'] == 'FTW'), ['ctn_per_plt']] = 22
    df.loc[(df['ctn_per_plt'].isna()) & (df['Cate'] == 'APP'), ['ctn_per_plt']] = 18

    df['FPL_Units'] = df['ctn_per_plt'] * df['fullCaseUnits']
    df['HPL_Units'] = np.floor(df['FPL_Units'] / 2)

    ### =======================
    ### version 1 location cal. (1个SKU3种库位类型)

    # inv to case and pallet
    df['all_Case_Num'] = df['INV_QTY'] // df['fullCaseUnits']
    df['all_Case_Qty'] = df['all_Case_Num'] * df['fullCaseUnits']


    # 整托、半托数及对应的件数
    df['FPL_Num'] = df['INV_QTY'] // df['FPL_Units']
    df['FPL_Qty'] = df['FPL_Num'] * df['FPL_Units']

    df['HPL_Num'] = (df['INV_QTY'] - df['FPL_Qty']) // df['HPL_Units']
    df['HPL_Qty'] = df['HPL_Num'] * df['HPL_Units']

    # 箱数和箱件数
    df['Case_Num'] = (df['INV_QTY'] - df['FPL_Qty'] - df['HPL_Qty']) // df['fullCaseUnits']
    df['Case_Qty'] = df['Case_Num'] * df['fullCaseUnits']

    df['PCS'] = df['INV_QTY'] - df['FPL_Qty'] - df['HPL_Qty'] - df['Case_Qty']

    ### =======================
    ### version 2 location cal.
    # df['pl_Num'] = df['INV_QTY'] / df['FPL_Units']
    # df['FPL_locNum'] = 0
    # df['HPL_locNum'] = 0
    # df['Case_locNum'] = 1
    #
    # for index, row in df.iterrows():
    #     if row['pl_Num']>0.5:
    #         df.loc[ index, ['FPL_locNum']] = np.ceil(row['pl_Num'])
    #     elif row['pl_Num']>0.2 and row['pl_Num']<=0.5:
    #         df.loc[ index, ['HPL_locNum']] = 1
    #     else:
    #         df.loc[ index, ['Case_locNum']] = np.ceil((row['pl_Num'] * row['FPL_Units']) / row['fullCaseUnits']) + 1
    #

    print(df.head(10))

    # df = df.head(3000)

    # caseClassNum = len(config.CTN_QTY_INTERVAL)
    # PCClassNum = len(config.PC_CLASS)
    #
    # ### case class
    # df['Case_Num_class'] = np.NAN
    # # df.loc[(df['INV_QTY']<=0),['Case_Num_class']] = '00-NoInv'
    # for i in range(caseClassNum):
    #     if i == caseClassNum - 1:
    #         df.loc[(df['Case_Num'] > config.CTN_QTY_CLASS[i][1]),
    #                ['Case_Num_class']] = config.CTN_QTY_CLASS[i][0]
    #     else:
    #         df.loc[(df['Case_Num'] > config.CTN_QTY_CLASS[i][1]) &
    #                (df['Case_Num'] <= config.CTN_QTY_CLASS[i][2]),
    #                ['Case_Num_class']] = config.CTN_QTY_CLASS[i][0]
    #
    # df['pltNum_class'] = np.NAN
    # df.loc[(df['INV_QTY'] <= 0), ['pltNum_class']] = '00-NoInv'
    # for index, row in df.iterrows():
    #     for i in range(PCClassNum):
    #         if row['pltNum'] > config.PC_CLASS[i][1] and row['pltNum'] <= \
    #                 config.PC_CLASS[i][2]:
    #             df.loc[index, ['pltNum_class']] = config.PC_CLASS[i][0]
    #             break
    #
    # df['location_type'] = np.NAN
    # df.loc[(df['Case_Num'] <= 3), ['location_type']] = 'Case'
    # df.loc[(df['pltNum'] <= 0.5) & (df['location_type'].isna()), ['location_type']] = 'HPL'
    # df.loc[(df['pltNum'] > 0.5) & (df['location_type'].isna()), ['location_type']] = 'FPL'


    ## 日期，箱数分级
    # index1 = ['INV_DATE', 'Case_Num_class']
    # pt1 = pd.pivot_table(df, index=index1,
    #                      values=['SKU_ID', 'INV_QTY', 'Case_Num'],
    #                      aggfunc={'SKU_ID': len, 'INV_QTY':np.sum, 'Case_Num':np.sum}).reset_index()
    # index_num = len(index1)
    # cols = list(pt1.columns[index_num:])
    # # 计算比例
    # for i in range(len(cols)):
    #     pt1[cols[i] + '%'] = pt1[cols[i]] / (pt1[cols[i]].sum())
    #
    # print(pt1.shape)

    ## 日期，托数分级
    # index2 = ['INV_DATE', 'pltNum_class']
    # pt2 = pd.pivot_table(df, index=index2,
    #                      values=['SKU_ID', 'INV_QTY', 'Case_Num', 'pltNum'],
    #                      aggfunc={'SKU_ID': len, 'INV_QTY': np.sum, 'Case_Num': np.sum, 'pltNum':np.sum}).reset_index()
    # index_num = len(index2)
    # cols = list(pt2.columns[index_num:])
    # # 计算比例
    # for i in range(len(cols)):
    #     pt2[cols[i] + '%'] = pt2[cols[i]] / (pt2[cols[i]].sum())
    # print(pt2.shape)
    #
    #
    # ## 日期，类别，箱数分级
    # index3 = ['INV_DATE', 'PRODUCT_LINE_EN', 'Case_Num_class']
    # pt3 = pd.pivot_table(df, index=index3,
    #                      values=['SKU_ID', 'INV_QTY', 'Case_Num'],
    #                      aggfunc={'SKU_ID': len, 'INV_QTY': np.sum, 'Case_Num': np.sum}).reset_index()
    # index_num = len(index3)
    # cols = list(pt3.columns[index_num:])
    # # 计算比例
    # for i in range(len(cols)):
    #     pt3[cols[i] + '%'] = pt3[cols[i]] / (pt3[cols[i]].sum())
    # print(pt3.shape)
    #
    # index4 = ['INV_DATE', 'PRODUCT_LINE_EN', 'pltNum_class']
    # pt4 = pd.pivot_table(df, index=index4,
    #                      values=['SKU_ID', 'INV_QTY', 'pltNum'],
    #                      aggfunc={'SKU_ID': len, 'INV_QTY': np.sum, 'pltNum': np.sum}).reset_index()
    # index_num = len(index4)
    # cols = list(pt4.columns[index_num:])
    # # 计算比例
    # for i in range(len(cols)):
    #     pt4[cols[i] + '%'] = pt4[cols[i]] / (pt4[cols[i]].sum())
    # print(pt4.shape)

    print('原始表：', df.shape)
    # writer = pd.ExcelWriter('{}Inv2Case/dataSource_{}.xlsx'.format(file_folder, date))
    # df.to_excel(writer, sheet_name='inv2case', index=False)
    # writer.save()
    # writer.close()
    #

    writer = pd.ExcelWriter('{}Inv2Case/inv2case_results_{}.xlsx'.format(file_folder, date))

    ## 将FPL,HPL,Case 按APP,FTW汇总
    re = pd.pivot_table(df, index=['Cate'], values=['SKU_ID','INV_QTY','FPL_Num', 'HPL_Num', 'Case_Num',
                                                    'FPL_Qty', 'HPL_Qty', 'Case_Qty', 'PCS'],
                        aggfunc={'SKU_ID': len, 'INV_QTY':np.sum, 'FPL_Num': np.sum, 'HPL_Num': np.sum, 'Case_Num': np.sum,
                                 'FPL_Qty': np.sum, 'HPL_Qty': np.sum, 'Case_Qty': np.sum, 'PCS': np.sum},
                        margins=True)


    # re = pd.pivot_table(df, index=['Cate'], values=['SKU_ID','FPL_locNum','HPL_locNum', 'Case_locNum'],
    #                     aggfunc={'SKU_ID': len, 'FPL_locNum':np.sum, 'HPL_locNum': np.sum, 'Case_locNum': np.sum},
    #                     margins=True)

    re.to_excel(writer)

    # idx1 = ['INV_DATE', 'Cate', 'location_type']
    # res = gene_class(df=df, index=idx1, isCumu=True)
    # res.to_excel(writer, sheet_name='01-Case_Num', index=False)
    #
    # idx2 = ['INV_DATE', 'Cate', 'location_type']
    # res = gene_class(df=df, index=idx2, isCumu=True)
    # res.to_excel(writer, sheet_name='02-PC_class', index=False)
    #
    # idx3 = ['INV_DATE', 'Cate', 'location_type', 'Case_Num_class']
    # res = gene_class(df=df, index=idx3, isCumu=True)
    # res.to_excel(writer, sheet_name='03-cate_Case_Num', index=False)
    #
    # idx4 = ['INV_DATE', 'Cate', 'location_type', 'pltNum_class']
    # res = gene_class(df=df, index=idx4, isCumu=True)
    # res.to_excel(writer, sheet_name='04-cate_PC_class', index=False)


    # pt1.to_excel(writer, sheet_name='01-Case_Num')
    # pt2.to_excel(writer, sheet_name='02-PC_class')
    # pt3.to_excel(writer, sheet_name='03-cate_Case_Num')
    # pt4.to_excel(writer, sheet_name='04-cate_PC_class')
    writer.save()
    writer.close()

def gene_class(df, index, pt_col=None, aggfun = None, isCumu=False):
    if pt_col is None:
        pt_col = ['SKU_ID', 'INV_QTY', 'Case_Num', 'pltNum', 'Case_Qty', 'FPL_Num']
        aggfun = {'SKU_ID': len, 'INV_QTY': np.sum, 'Case_Num': np.sum, 'pltNum': np.sum,
               'Case_Qty': np.sum, 'FPL_Num': np.sum}

    tmp = pd.pivot_table(df, index=index,
                          values=pt_col, aggfunc=aggfun,
                          fill_value=0,
                          margins=True).reset_index()

    ## 重排列
    tmp = tmp[index +  pt_col]

    # index_num = len(index)
    # cols = list(tmp.columns[index_num:])

    # 计算比例
    for i in range(len(pt_col)):
        tmp[pt_col[i] + '%'] = tmp[pt_col[i]] / (tmp[pt_col[i]].sum()/2)

    if isCumu:
        for i in range(len(pt_col)):
            # result_pt[cols[i] + '%_cumu'] = result_pt[cols[i] + '%'].cumsum().apply(lambda x: '%.2f%%' % (x * 100))
            tmp[pt_col[i] + '%_cumu'] = tmp[pt_col[i] + '%'].cumsum()

    for col in list(tmp.columns):
        if 'cumu' in col:
            tmp.loc[(tmp[tmp.columns[0]] == 'All'), [col]] = ''

    return tmp


if __name__ == '__main__':
    time1 = datetime.datetime.now()
    print(time1)

    # ### B2B return east 2020
    # file_folder = 'D:/Work/Project/12SKX/00DataAnalysis/'
    # file_path = '{}Return_B2B_east'.format(file_folder)
    #
    # save_file_name = 'return_east.csv'
    # qtyCol = 'QTYIN'
    # merge(file_path, file_folder, qtyCol=qtyCol, save_file_name=save_file_name)

    # B2B return east 2019
    # file_folder = 'D:/Work/Project/12SKX/00DataAnalysis/2019/'
    # file_path = '{}Return_B2B_east'.format(file_folder)
    #
    # save_file_name = 'return_east2019.csv'
    # qtyCol = 'QTYIN'
    # merge(file_path, file_folder, qtyCol=qtyCol, save_file_name=save_file_name)

    ### B2C return 2019
    # file_folder = 'D:/Work/Project/12SKX/00DataAnalysis/2019/'
    # file_path = '{}2019 ECOM Return'.format(file_folder)
    #
    # save_file_name = 'B2C_return2019.csv'
    # qtyCol = 'QTYIN'
    # merge(file_path, file_folder, qtyCol=qtyCol, save_file_name=save_file_name)


    ### B2C inbound 2019 data cleaning
    # file_folder = 'D:/Work/Project/12SKX/00DataAnalysis/2019/'
    # file_path = '{}2019 ECOM Return'.format(file_folder)
    #
    # save_file_name = 'B2C_return2019.csv'
    # qtyCol = 'QTYIN'
    # merge(file_path, file_folder, qtyCol=qtyCol, save_file_name=save_file_name)


    ### B2C return 2020
    # file_folder = 'D:/Work/Project/12SKX/00DataAnalysis/'
    # file_path = '{}Return'.format(file_folder)
    #
    # save_file_name = 'B2C_return2020.csv'
    # qtyCol = 'QTYIN'
    # merge(file_path, file_folder, qtyCol=qtyCol, save_file_name=save_file_name)


    ####============================================
    #### 2020 B2C by date
    ####============================================

    # file = 'D:/Work/Project/12SKX/00DataAnalysis/B2C_return2020.csv'
    # df = pd.read_csv(file, encoding='gbk', low_memory=False)
    # writer = pd.ExcelWriter('D:/Work/Project/12SKX/00DataAnalysis/B2C_return2020.xlsx')
    #
    # idx1 = ['DATEIN']
    # res = pd.pivot_table(df, index=['DATEIN'], values=['QTYIN'])
    # res.to_excel(writer, sheet_name='01bydate', index=False)
    #
    # idx2 = ['INV_DATE', 'Cate', 'location_type']
    # res = gene_class(df=df, index=idx2, isCumu=True)
    # res.to_excel(writer, sheet_name='02-PC_class', index=False)


    # file_path = '{}202003'.format(file_folder)
    # save_file_name = '202003.csv'
    # merge(file_path, save_file_path, save_file_name)

    # file_path = '{}202006'.format(file_folder)
    # save_file_name = '202006.csv'
    # merge(file_path, save_file_path, save_file_name)

    # file_path = '{}202009'.format(file_folder)
    # save_file_name = '202009.csv'
    # merge(file_path, save_file_path, save_file_name)

    # file_path = '{}202012'.format(file_folder)
    # save_file_name = '202012.csv'
    # merge(file_path, save_file_path, save_file_name)

    # file_path = 'D:/Work/Project/12SKX/00DataAnalysis/Return'
    # save_file_name = 'return.csv'
    # merge(file_path, save_file_path, save_file_name)

    ### 3，6，9，12月SKU在库天数，及first day / last day

    # index=['BARCODE']
    # col=['INV_DATE']

    # file_name_lists = ['202003', '202006', '202009', '202012', 'inv_month_end']
    # gene_pt(writer=writer, file_folder=file_folder, file_name_lists=file_name_lists, index=index, col=col)

    # file_name_lists = ['202003', '202006', '202009', '202012']
    # writer = pd.ExcelWriter('{}SKU_days.xlsx'.format(file_folder))
    # sku_days(writer=writer, file_folder=file_folder, file_name_lists=file_name_lists)
    # writer.save()
    # writer.close()

    ###  SKU折成箱，折成托的分级
    date = '2020-07-31'
    # date = '2019-10-31'

    save_file_path = 'D:/Work/Project/12SKX/00DataAnalysis/Inv/results/'
    stock_file = 'D:/Work/Project/12SKX/00DataAnalysis/Inv/Month_end/inv_{}.csv'.format(date)
    sku_detail = 'D:/Work/Project/12SKX/00DataAnalysis/Inv/sku_detail.xlsx'


    load_data_to_class(save_file_path, stock_file=stock_file, sku_detail=sku_detail, date=date)


    # ## 数据过滤
    # file_folder = 'D:/Work/Project/12SKX/00DataAnalysis/Inv/'
    # file_path = '{}Month_end'.format(file_folder)
    #
    # save_file_name = 'inv20192020.csv'
    # qtyCol = 'INV_QTY'
    # merge(file_path, file_folder, qtyCol=qtyCol, save_file_name=save_file_name)


    ### update JITX merge data
    # folder_path = 'F:/SKX/SourceData/2020 ECOM updated JITX'
    # save_path = 'F:/SKX/SourceData/2020 ECOM ob results updated'
    # qtyCol = 'QTY'
    # save_file = 'ob2020_update_JITX.csv'
    #
    # merge(folder_path, save_path, qtyCol=qtyCol, save_file_name=save_file)


    time2 = datetime.datetime.now()
    print('running time: {} S'.format((time2-time1).seconds))



