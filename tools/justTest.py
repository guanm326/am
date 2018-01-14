from sympy import *
import pandas as pd
import numpy as np
import os
import tools.filetools as ft

# local_file_path = 'D:/投资收益月度核对/'
# remote_file_path = '//10.145.39.42/北京总部文件资料/资产管理部/投资收益月度核对/'
# tb_file_path_frag = 'TB文件/'
# check_result_file_path_frag = '核对结果/'
# matrix_file_name = 'TB-MI-MATRIX.xlsx'
# # 判断是否能够连上共享，不能的话使用本地路径
# file_path = remote_file_path
# if not os.path.exists(file_path):
#     file_path = local_file_path
# print("file_path: ", file_path)
#
# matrix_full_path = file_path + matrix_file_name
# print("matrix_full_path: ", matrix_full_path)
#
# print("请输入 %s 路径中的TB文件名称: " % (file_path + tb_file_path_frag))
# tb_file_name = input("> ")
# tb_file_path = file_path + tb_file_path_frag + tb_file_name
# print("tb_file_path: ", tb_file_path)
# tb_file_flag = os.path.exists(tb_file_path) and os.path.isfile(tb_file_path) and os.access(tb_file_path, os.R_OK)
# while not tb_file_flag:
#     print("输入的文件不存在或者无法访问，请重新输入TB文件名称: ")
#     tb_file_name = input("> ")
#     tb_file_path = file_path + tb_file_path_frag + tb_file_name
#     print("tb_file_path: ", tb_file_path)
#     tb_file_flag = os.path.exists(tb_file_path) and os.path.isfile(tb_file_path) and os.access(tb_file_path, os.R_OK)
# # print("请输入核对结果保存文件路径，类似 d:/TB_CHECK_201709.xlsx : ")
# # file_path = input("> ")
# check_result_file_name = "CHECK_" + tb_file_name
# save_file_path = file_path + check_result_file_path_frag + check_result_file_name
# print("save_file_path: ", save_file_path)

# input("输入任意键结束...")


def funa(a, *b):
    print(a)
    print(b)

a = "a"
b = pd.DataFrame()
b['az'] = [1, 2, 3, 4, 5, 6]
b['ad'] = [1, 2, 3, 4, 5, 6]
b['af'] = [1, 2, 3, 4, 5, 6]
c = pd.DataFrame()
c['az'] = [1, 2, 3, 4, 5, 6]
c[0.5] = [1, 2, 3, 4, 5, 6]
c['ae'] = [1, 2, 3, 4, 5, 6]
c = c.ix[:, ['az', 0.5]]
b = pd.merge(b, c, on=['az'])
for item in [0.5]:
    b.loc[:, item] = b.loc[:, 'az'] * b.loc[:, item]
print(b)
# funa(a, b, c)
# d = None
# print(d is not None)
# a = [1, 2, 3]
# b = [3, 4]
# b.extend(a)
# b.extend([4, 6])
# print(b)
# for item in b:
#     print(item)
# test = pd.DataFrame()
# test['az'] = ['a', 'a', 'b', 'b', 'c', 'd']
# test['number'] = [1, 2, 3, 4, 5, 6]
# test_group = test['number'].groupby(test['az']).sum()
# test_group.columns = ['lala', 'amount']
# # print(test_group.values)
# # test_group.columns
# suma = pd.DataFrame()
# suma['lala'] = ['a', 'b', 'c', 'd', 'e', 'f']
# suma['org'] = 4
# suma['dt'] = ['2017/01/01', '2017/03/01', '2017/02/01', '2017/01/21', '2017/01/11', '2017/01/02']
# print(suma)
# for index, row in suma.iterrows():
#     if index == 3:
#         suma.drop([index], inplace=True)
#
# print(suma)
# suma['dtm'] = suma.to_period('M')
# testa = pd.DataFrame()
# testa['lala'] = test_group.index
# testa['number'] = test_group.values
#
# # print(testa)
#
# suma = pd.merge(suma, testa, on='lala', how='left')
# # suma['dt2'] = suma['dt']
# suma['dt'] = pd.to_datetime(suma['dt'])
# # suma = suma.sort_index()
# # print(suma)
# suma['ttt'] = suma['org'] * suma['number'] / 100
# # print(suma)
# suma = suma.loc[:, ['dt', 'ttt', 'number', 'org']]
# suma = suma.sort_values(['dt'])
# suma = suma.set_index('dt')
# suma = suma.to_period('M')
# # print(suma)
# suma_group = suma.groupby(suma.index).sum()
# suma_group.insert(0, 'test', suma_group.index)
# # suma_group['test'] = pd.to_datetime(suma_group['test'])
# print(suma_group)
# writer = pd.ExcelWriter("d:/save_test.xlsx")
# ff = '%0.2f%%'
# suma_group.to_excel(writer, "sheet1")
# suma_group.to_excel(writer, "sheet2", index=False)
# writer.save()
# print(suma)
# print(suma.shape[0])
# last_one = suma.shape[0]
# suma.loc[last_one] = suma.loc[0]
# suma.loc[last_one, 'ttt'] = 5
# suma.loc[last_one, 'number'] = 5
# suma.loc[last_one, 'org'] = 5
# suma['dt'] = pd.to_datetime(suma['dt'])
# print('-' * 50)
# print(suma)
# print(suma.shape[0])
# print(suma.columns.values.tolist())
# data_map = [
#         {
#             "sheet_name": "detail",
#             "sheet_data": suma_group.values.tolist(),
#             "fields": suma_group.columns.values.tolist()
#         }
# ]
# ft.save_data_to_workbook(data_map, "d:/save_test.xlsx", "")
# print(suma)
# print(suma)
# print(suma.groupby(suma.index).sum())
# rng = pd.period_range(start='20170101', end='20171201', freq='M')
# date_df = pd.DataFrame(data={
#     "temp": ""
# }, index=rng)
# print(date_df)
# suma = pd.merge(date_df, suma, how='left', left_index=True, right_index=True)
# print(suma)
# print(suma.groupby(suma.index).sum())
# print(suma.groupby(rng).sum())
