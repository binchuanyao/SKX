# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


def groupby_date_hour(file, save_file):
    # file = 'D:/Work/Project/04中通云仓/sale.xlsx'
    df = pd.read_excel(file)
    df.rename(columns={'scaledAt ': 'scaledAt'}, inplace=True)

    print(type(df))

    df['oqc2scaled'] = df['scaledAt'] - df['oqcEndAt']
    df['oqc2ship'] = df['actualShipDateTime'] - df['oqcEndAt']
    df['scaled2ship'] = df['actualShipDateTime'] - df['scaledAt']

    df['oqc2scaled_seconds'] = (df['scaledAt'] - df['oqcEndAt']).astype('timedelta64[s]')
    df['oqc2ship_seconds'] = (df['actualShipDateTime'] - df['oqcEndAt']).astype('timedelta64[s]')
    df['scaled2ship_seconds'] = (df['actualShipDateTime'] - df['scaledAt']).astype('timedelta64[s]')

    df['scaled_date'] = df['scaledAt'].dt.date
    df['scaled_hour'] = df['scaledAt'].dt.hour

    df['oqc_date'] = df['oqcEndAt'].dt.date
    df['oqc_hour'] = df['oqcEndAt'].dt.hour

    # groupby date & hour
    idx = ['scaled_date', 'scaled_hour']
    # all_date_hour = df.groupby(['scaled_date', 'scaled_hour']).agg(
    #     CountOrder=pd.NamedAgg(column='waybillCode', aggfunc='count'),
    #     SumQty=pd.NamedAgg(column='totalQty', aggfunc='sum')).reset_index

    idx2 = ['oqc_date', 'oqc_hour']

    all_date_hour = pd.pivot_table(df, index=idx2, values=['waybillCode', 'totalQty'],
                                   aggfunc={'waybillCode': 'count', 'totalQty': 'sum'}, margins=True).reset_index()

    print(all_date_hour)

    df_order = pd.pivot_table(df, index=['oqc_hour'], columns=['oqc_date'],
                              values=['waybillCode'], aggfunc='count', margins=True).reset_index()

    df_qty = pd.pivot_table(df, index=['oqc_hour'], columns=['oqc_date'],
                            values=['totalQty'], aggfunc='sum', margins=True).reset_index()

    # save_file = 'D:/Work/Project/04中通云仓/output.xlsx'
    writer = pd.ExcelWriter(save_file)

    df.to_excel(excel_writer=writer, sheet_name='sourceData', na_rep='', index=False)

    print(type(all_date_hour))

    all_date_hour.to_excel(excel_writer=writer, sheet_name='01all_date_hour', na_rep=0, index=False)
    df_order.to_excel(excel_writer=writer, sheet_name='02order_date_hour', na_rep=0)
    df_qty.to_excel(excel_writer=writer, sheet_name='03qty_date_hour', na_rep=0)

    writer.save()
    writer.close()


if __name__ == '__main__':

    file = 'D:/Work/Project/04中通云仓/sale.xlsx'
    save_file = 'D:/Work/Project/04中通云仓/output2.xlsx'
    groupby_date_hour(file, save_file)



