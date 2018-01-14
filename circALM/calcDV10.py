import pandas as pd
import numpy as np
from tools import filetools

KEY_YEARS = [0, 0.5, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 35, 40, 45, 50]
CASH_FLOW_START_ROW = 6
DROP_NA_THRESH = 5
CASH_FLOW_STR = 'CASH_FLOW'
TIME_LIMIT_STR = 'TIME_LIMIT'
DISCOUNT_STR = 'DISCOUNT'
DISCOUNT_CASH_FLOW_STR = 'DISCOUNT_CASH_FLOW'

DELT_T = 'DELT_t'
NEW_DISCOUNT_ADD_TEN = 'NEW_DISCOUNT_ADD_TEN'
NEW_DISCOUNT_SUB_TEN = 'NEW_DISCOUNT_SUB_TEN'
NEW_CASH_FLOW_ADD_TEN = 'NEW_CASH_FLOW_ADD_TEN'
NEW_CASH_FLOW_SUB_TEN = 'NEW_CASH_FLOW_SUB_TEN'


def extend_discount_data(right_data, key_year_now, key_year_right):
    delt_T = abs(key_year_right - key_year_now)
    right_data[DELT_T] = abs(right_data[TIME_LIMIT_STR] - key_year_now)
    right_data[NEW_DISCOUNT_ADD_TEN] = right_data[DISCOUNT_STR] + \
                                       (10 * (delt_T - right_data[DELT_T]) / delt_T) / 10000
    right_data[NEW_DISCOUNT_SUB_TEN] = right_data[DISCOUNT_STR] - \
                                       (10 * (delt_T - right_data[DELT_T]) / delt_T) / 10000
    right_data[NEW_CASH_FLOW_ADD_TEN] = right_data[CASH_FLOW_STR] / (
        (1 + right_data[NEW_DISCOUNT_ADD_TEN]) ** right_data[TIME_LIMIT_STR])
    right_data[NEW_CASH_FLOW_SUB_TEN] = right_data[CASH_FLOW_STR] / (
        (1 + right_data[NEW_DISCOUNT_SUB_TEN]) ** right_data[TIME_LIMIT_STR])


def calc_dv10_from_cash_flow(sheet_name, sheet_data, key_years):
    dv10 = pd.DataFrame(columns=KEY_YEARS)
    max_time = sheet_data[TIME_LIMIT_STR].max()
    last_loop = False
    for i in range(len(key_years)):
        if last_loop:
            break
        # 如果year超过期限，则此轮循环后跳出循环
        year = key_years[i]
        if float(year) >= float(max_time):
            last_loop = True
        left_data = None
        right_data = None
        if i == 0:
            right_data = sheet_data[sheet_data[TIME_LIMIT_STR] < key_years[1]].copy()
            extend_discount_data(right_data, key_years[i], key_years[i+1])

        elif i == len(key_years) - 1:
            left_data = sheet_data[
                (sheet_data[TIME_LIMIT_STR] > key_years[i - 1]) & (sheet_data[TIME_LIMIT_STR] <= key_years[i])].copy()
            extend_discount_data(left_data, key_years[i], key_years[i-1])
            right_data = sheet_data[sheet_data[TIME_LIMIT_STR] > key_years[i]].copy()
            extend_discount_data(right_data, key_years[i], max_time)
        else:
            left_data = sheet_data[
                (sheet_data[TIME_LIMIT_STR] > key_years[i - 1]) & (sheet_data[TIME_LIMIT_STR] <= key_years[i])].copy()
            extend_discount_data(left_data, key_years[i], key_years[i - 1])
            right_data = sheet_data[(sheet_data[TIME_LIMIT_STR] > key_years[i]) & (sheet_data[TIME_LIMIT_STR] <= key_years[i+1])].copy()
            extend_discount_data(right_data, key_years[i], key_years[i+1])

        dv10_value = 0.0
        left_dv10_value = 0.0
        right_dv10_value = 0.0
        if not (right_data is None):
            right_dv10_value = right_data[NEW_CASH_FLOW_SUB_TEN].sum() - right_data[NEW_CASH_FLOW_ADD_TEN].sum()
        if not (left_data is None):
            left_dv10_value = left_data[NEW_CASH_FLOW_SUB_TEN].sum() - left_data[NEW_CASH_FLOW_ADD_TEN].sum()
        if not np.isnan(left_dv10_value):
            dv10_value += left_dv10_value
        if not np.isnan(right_dv10_value):
            dv10_value += right_dv10_value
        dv10.loc[sheet_name, key_years[i]] = dv10_value / 2

    return dv10


# 根据特定的估值文件，按照key years 计算所有有效估值sheet页内的DV10
def calc_all_dv10(file_full_name, dv10_file_full_name, key_years=KEY_YEARS):
    # 读取所有sheet页的数据
    dv10 = pd.DataFrame(columns=KEY_YEARS)
    cash_flow_data = filetools.read_workbook(file_full_name)
    for sheet_name in cash_flow_data:
        if (len(cash_flow_data.get(sheet_name)) > 5) and (len(cash_flow_data.get(sheet_name)[0]) > 9) and\
                (cash_flow_data.get(sheet_name)[3][7] == '最终估值') and \
                (cash_flow_data.get(sheet_name)[3][8] != '#VALUE!') and \
                (cash_flow_data.get(sheet_name)[3][8] != '#N/A'):
            sheet_data = pd.DataFrame(cash_flow_data.get(sheet_name)[CASH_FLOW_START_ROW:])
            # sheet_data = sheet_data.dropna(axis=0, how='any', thresh=DROP_NA_THRESH)
            # sheet_data = sheet_data.dropna(axis=1, how='any', thresh=DROP_NA_THRESH)
            sheet_data = sheet_data.loc[:, [2, 4, 7, 8]].rename(
                columns={2: CASH_FLOW_STR, 4: TIME_LIMIT_STR, 7: DISCOUNT_STR, 8: DISCOUNT_CASH_FLOW_STR})
            sheet_data = sheet_data[sheet_data[TIME_LIMIT_STR] > 0]
            dv10 = dv10.append(calc_dv10_from_cash_flow(sheet_name, sheet_data, key_years))

        else:
            continue
    # 遍历并筛选有效的sheet页进行计算，每个页的有效数据从第七行开始
    # 读取现金流期限、金额、折现率数据
    # 按照KEY YEARS进行DV10计算，每个KEY YEAR节点上下浮动时，只影响相邻节点，且为线性关系
    # 将结果保存至新的pd，column为KEY_YEARS，row id 为品种名称
    # 将dv10的pd保存至dv10sheet，插入至最前列

    # print(dv10)
    dv10.fillna(value=0.0)
    dv10.to_excel(dv10_file_full_name, 'dv10')


if __name__ == '__main__':
    # calc_all_dv10("D:\\work\\会计核算方法\\含权债券估值方法\\20171120\\20170630非标和存款资产估值（20171120）- 数值版.xlsx",
    #               "D:\\work\\会计核算方法\\含权债券估值方法\\20171120\\20170630非标资产估值 - DV10.xlsx")
    # calc_all_dv10("D:\\work\\会计核算方法\\含权债券估值方法\\20171120\\20170630债券现金流（20171120）.xlsm",
    #               "D:\\work\\会计核算方法\\含权债券估值方法\\20171120\\20170630债券数据 - DV10.xlsx")
    # calc_all_dv10("D:\\work\\会计核算方法\\含权债券估值方法\\20171120\\次级债估值.xlsx",
    #               "D:\\work\\会计核算方法\\含权债券估值方法\\20171120\\次级债估值 - DV10.xlsx")
    calc_all_dv10("D:\\work\\保监会ALM量化评估测试\\量化测试估算 - hw\\20171120\\20170630非标和存款资产估值（20171122）-股权基金及理财.xlsm",
                  "D:\\work\\保监会ALM量化评估测试\\量化测试估算 - hw\\20171120\\股权基金及理财 - DV10-期限修正版.xlsx")



