"""
通过TB校验MI和PL之间相差的科目信息及金额
"""
import pandas as pd
import numpy as np
import tools.filetools as ft
import os


TB_MI_MATRIX_SHEET_NAME = 'Sheet1'
TB_MI_MATRIX_SHEET_NAME_LIST = [TB_MI_MATRIX_SHEET_NAME]
TB_INFO_SHEET_NAME = "Sheet1"
TB_INFO_SHEET_NAME_LIST = [TB_INFO_SHEET_NAME]

MATRIX_DESC_COLUMN = 'DESC'

TB_ACCOUNT_NAME = '说明'
TB_COMPANY = '公司'
TB_ACCOUNT = '科目'
TB_DESC = '描述'
TB_START_AMOUNT = '起初发生额'
TB_DURATION_AMOUNT = '期间发生额'
TB_BALANCE = '期末余额'
TB_PL_FLAG_COLUMN = 'PL_FLAG'
TB_MI_FLAG_COLUMN = 'MI_FLAG'
TB_PL_FLAG = 'PL'
TB_SUMMARY_COLUMN = 'SUMMARY'

SUMMARY_DESC = "DESC"
SUMMARY_AMOUNT = "AMOUNT"
SUMMARY_FIELDS = [SUMMARY_DESC, SUMMARY_AMOUNT]
DETAIL_FIELDS = [TB_ACCOUNT_NAME, TB_COMPANY, TB_ACCOUNT, TB_DESC, TB_START_AMOUNT, TB_DURATION_AMOUNT, TB_BALANCE,
                 TB_PL_FLAG_COLUMN, TB_MI_FLAG_COLUMN, TB_SUMMARY_COLUMN]

TB_COMPANY_EXCLUSION_LIST = ['100102', '100600']
SUB_DEBT_COMPANY = '100102'
PL_ACCOUNT_LIST = ['60110102', '60110201', '60110202', '60110301', '60110401', '60110701', '60110702', '61110101',
                   '61110102', '61110103', '61110104', '61110105', '61110201', '61110202', '61110301', '61110302',
                   '61110303', '61110304', '61110305', '61110901']
FAIR_VALUE_ACCOUNT = '40030102'
IN_MI_NOT_IN_PL_FLAG = "IN MI NOT IN PL"
IN_PL_NOT_IN_MI_FLAG = "IN PL NOT IN MI"

NUMBER_FORMAT = '_ * #,##0.00_ ;_ * \-#,##0.00_ ;_ * "-"??_ ;_ @_ '

SUMMARY_NUMBER_FORMAT = {
    "B": NUMBER_FORMAT
}
SUMMARY_WIDTH = {
    "A": 50,
    "B": 20
}
DETAIL_NUMBER_FORMAT = {
    "E": NUMBER_FORMAT,
    "F": NUMBER_FORMAT,
    "G": NUMBER_FORMAT
}
DETAIL_WIDTH = {
    "A": 50,
    "B": 7,
    "C": 9,
    "D": 9,
    "E": 20,
    "F": 20,
    "G": 20,
    "H": 8,
    "I": 40,
    "J": 17
}


def get_tb_mi_matrix(file_path=r'\\10.145.39.42\北京总部文件资料\资产管理部\投资收益月度核对\TB-MI-MATRIX.xlsx'):
    org_data = ft.read_workbook(file_path, "", TB_MI_MATRIX_SHEET_NAME_LIST)
    matrix_df = ft.data_clean_in_one_sheet(
        org_data, TB_MI_MATRIX_SHEET_NAME, axis_one_drop_na_flag=False, axis_zero_drop_na_flag=False)
    return matrix_df


def get_tb_info(file_path=r'\\10.145.39.42\北京总部文件资料\资产管理部\投资收益月度核对\TB文件\TB1710-XUN.xlsx', sheet_name=TB_INFO_SHEET_NAME):
    org_data = ft.read_workbook(file_path, "", TB_INFO_SHEET_NAME_LIST)
    tb_info_df = ft.data_clean_in_one_sheet(
        org_data, sheet_name, axis_one_drop_na_flag=False, axis_zero_drop_na_flag=False)
    if tb_info_df.columns.values.tolist().count(TB_ACCOUNT) > 1:
        tb_info_df.columns = ['科目DEL', TB_ACCOUNT_NAME, '科目说明', TB_COMPANY, TB_ACCOUNT, '渠道',
                              '部门', '险种', '往来', TB_DESC, '备用',
                              TB_START_AMOUNT, TB_DURATION_AMOUNT, TB_BALANCE]
    return tb_info_df


def mark_mi_flag(desc, account, matrix):
    mi_flag = ""
    if desc in matrix[MATRIX_DESC_COLUMN].values:
        if account in matrix.columns:
            mi_flag = matrix.loc[matrix[MATRIX_DESC_COLUMN] == desc, account].values[0]
        elif account[:4] in matrix.columns:
            mi_flag = matrix.loc[matrix[MATRIX_DESC_COLUMN] == desc, account[:4]].values[0]
    elif desc[:5] in matrix[MATRIX_DESC_COLUMN].values:
        if account in matrix.columns:
            mi_flag = matrix.loc[matrix[MATRIX_DESC_COLUMN] == desc[:5], account].values[0]
        elif account[:4] in matrix.columns:
            mi_flag = matrix.loc[matrix[MATRIX_DESC_COLUMN] == desc[:5], account[:4]].values[0]
    if mi_flag == "":
        mi_flag = np.NaN
    return mi_flag


def add_tag_to_tb(tb_info, matrix):
    for index, row in tb_info.iterrows():
        account = row[TB_ACCOUNT]
        company = row[TB_COMPANY]
        desc = row[TB_DESC]
        # 增加PL标志
        if account in PL_ACCOUNT_LIST:
            tb_info.loc[index, TB_PL_FLAG_COLUMN] = TB_PL_FLAG
        # 增加MI标志
        # if (company not in TB_COMPANY_EXCLUSION_LIST) and (account != FAIR_VALUE_ACCOUNT):
        if company not in TB_COMPANY_EXCLUSION_LIST:
            if account in ['60110102', '60110401']:
                tb_info.loc[index, TB_MI_FLAG_COLUMN] = '定期存款（>=1年）'
            elif account == '60110101':
                tb_info.loc[index, TB_MI_FLAG_COLUMN] = '定期存款(<1年）'
            else:
                tb_info.loc[index, TB_MI_FLAG_COLUMN] = mark_mi_flag(desc, account, matrix)

    tb_info = tb_info.fillna("")
    tb_info[TB_BALANCE] = tb_info[TB_BALANCE].replace("", 0)
    return tb_info


def difference_summary(tb_tag_info, fair_value_at_begin):
    # print(tb_tag_info.head())
    # 将期初资本公积数值列支为一项负值
    fair_value_at_begin = 0 - fair_value_at_begin
    last_one = tb_tag_info.shape[0]
    tb_tag_info.loc[last_one] = tb_tag_info.loc[0]
    tb_tag_info.loc[last_one, TB_ACCOUNT_NAME] = '其他综合收益-其他综合收益-可供出售金融资产公允'
    tb_tag_info.loc[last_one, TB_COMPANY] = ''
    tb_tag_info.loc[last_one, TB_ACCOUNT] = '40030102'
    tb_tag_info.loc[last_one, '渠道'] = ''
    tb_tag_info.loc[last_one, '部门'] = ''
    tb_tag_info.loc[last_one, '险种'] = ''
    tb_tag_info.loc[last_one, '往来'] = ''
    tb_tag_info.loc[last_one, TB_DESC] = ''
    tb_tag_info.loc[last_one, '备用'] = ''
    tb_tag_info.loc[last_one, TB_START_AMOUNT] = 0
    tb_tag_info.loc[last_one, TB_DURATION_AMOUNT] = 0
    tb_tag_info.loc[last_one, TB_BALANCE] = fair_value_at_begin
    tb_tag_info.loc[last_one, TB_PL_FLAG_COLUMN] = ''
    tb_tag_info.loc[last_one, TB_MI_FLAG_COLUMN] = '期初资本公积'

    tb_tag_info.loc[
        (tb_tag_info[TB_PL_FLAG_COLUMN] != "") & (tb_tag_info[TB_MI_FLAG_COLUMN] == ""), TB_SUMMARY_COLUMN
    ] = IN_PL_NOT_IN_MI_FLAG
    tb_tag_info.loc[
        (tb_tag_info[TB_PL_FLAG_COLUMN] == "") & (tb_tag_info[TB_MI_FLAG_COLUMN] != ""), TB_SUMMARY_COLUMN
    ] = IN_MI_NOT_IN_PL_FLAG

    # 汇总PL的期末值
    pl_sum = tb_tag_info.loc[tb_tag_info[TB_PL_FLAG_COLUMN] == TB_PL_FLAG, TB_BALANCE].sum()
    # 汇总 IN MI NOT IN PL 的汇总值
    in_mi_not_in_pl_sum = tb_tag_info.loc[tb_tag_info[TB_SUMMARY_COLUMN] == IN_MI_NOT_IN_PL_FLAG, TB_BALANCE].sum()
    # 汇总MI的期末值
    mi_sum = tb_tag_info.loc[tb_tag_info[TB_MI_FLAG_COLUMN] != "", TB_BALANCE].sum()
    # 汇总 IN PL NOT IN MI 的汇总值
    in_pl_not_in_mi_sum = tb_tag_info.loc[tb_tag_info[TB_SUMMARY_COLUMN] == IN_PL_NOT_IN_MI_FLAG, TB_BALANCE].sum()
    # 按科目维度汇总 IN PL NOT IN MI 的值
    in_pl_not_in_mi_df = tb_tag_info.loc[tb_tag_info[TB_SUMMARY_COLUMN] == IN_PL_NOT_IN_MI_FLAG].copy()
    in_pl_not_in_mi_grouped_df = in_pl_not_in_mi_df[TB_BALANCE].groupby(in_pl_not_in_mi_df[TB_ACCOUNT_NAME]).sum()
    in_pl_not_in_mi_grouped_df.columns = [SUMMARY_DESC, SUMMARY_AMOUNT]
    # 按科目维度汇总 IN PL NOT IN MI 的值 - 不包含 100102
    in_pl_not_in_mi_df_not_sub_debt = in_pl_not_in_mi_df.loc[in_pl_not_in_mi_df[TB_COMPANY] != SUB_DEBT_COMPANY].copy()
    in_pl_not_in_mi_df_not_sub_debt_grouped = in_pl_not_in_mi_df_not_sub_debt[TB_BALANCE]\
        .groupby(in_pl_not_in_mi_df_not_sub_debt[TB_ACCOUNT_NAME]).sum()
    in_pl_not_in_mi_df_not_sub_debt_sum = in_pl_not_in_mi_df_not_sub_debt.loc[:, TB_BALANCE].sum()
    # 按科目维度汇总 IN PL NOT IN MI 的值 - 只包含 100102
    in_pl_not_in_mi_df_sub_debt = in_pl_not_in_mi_df.loc[in_pl_not_in_mi_df[TB_COMPANY] == SUB_DEBT_COMPANY].copy()
    in_pl_not_in_mi_df_sub_debt_grouped = in_pl_not_in_mi_df_sub_debt[TB_BALANCE] \
        .groupby(in_pl_not_in_mi_df_sub_debt[TB_ACCOUNT_NAME]).sum()
    in_pl_not_in_mi_df_sub_debt_sum = in_pl_not_in_mi_df_sub_debt.loc[:, TB_BALANCE].sum()
    # 按科目维护汇总 IN MI NOT IN PL 的值
    in_mi_not_in_pl_df = tb_tag_info.loc[tb_tag_info[TB_SUMMARY_COLUMN] == IN_MI_NOT_IN_PL_FLAG].copy()
    in_mi_not_in_pl_grouped_df = in_mi_not_in_pl_df[TB_BALANCE].groupby(in_mi_not_in_pl_df[TB_ACCOUNT_NAME]).sum()
    in_mi_not_in_pl_grouped_df.columns = [SUMMARY_DESC, SUMMARY_AMOUNT]
    # 汇总信息拼接成一个DF，写入D盘带日期的summary文件
    summary_desc_list = ['PL_SUM', 'IN_MI_NOT_IN_PL_SUM', 'MI_SUM', 'IN_PL_NOT_IN_MI_SUM',
                         'SUM_VALUE_CHECK', ' ', 'IN_MI_NOT_IN_PL_LIST']
    summary_desc_list.extend(in_mi_not_in_pl_grouped_df.index.values)
    summary_desc_list.extend([' ', 'IN_PL_NOT_IN_MI_LIST_NOT_100102'])
    summary_desc_list.extend(in_pl_not_in_mi_df_not_sub_debt_grouped.index.values)
    summary_desc_list.extend([' ', 'IN_PL_NOT_IN_MI_LIST_100102'])
    summary_desc_list.extend(in_pl_not_in_mi_df_sub_debt_grouped.index.values)

    summary_amount_list = [pl_sum, in_mi_not_in_pl_sum, mi_sum, in_pl_not_in_mi_sum,
                           (pl_sum + in_mi_not_in_pl_sum - mi_sum - in_pl_not_in_mi_sum), np.NaN, in_mi_not_in_pl_sum]
    summary_amount_list.extend(in_mi_not_in_pl_grouped_df.values)
    summary_amount_list.extend([np.NaN, in_pl_not_in_mi_df_not_sub_debt_sum])
    summary_amount_list.extend(in_pl_not_in_mi_df_not_sub_debt_grouped.values)
    summary_amount_list.extend([np.NaN, in_pl_not_in_mi_df_sub_debt_sum])
    summary_amount_list.extend(in_pl_not_in_mi_df_sub_debt_grouped.values)

    summary_df = pd.DataFrame({
        SUMMARY_DESC: summary_desc_list,
        SUMMARY_AMOUNT: summary_amount_list
    })
    return summary_df


def save_result(file_path, summary_df, tb_tag_info):
    data_map = [
        {
            "sheet_name": "detail",
            "sheet_data": tb_tag_info.loc[:, DETAIL_FIELDS].values.tolist(),
            "fields": DETAIL_FIELDS
        },
        {
            "sheet_name": "summary",
            "sheet_data": summary_df.loc[:, SUMMARY_FIELDS].values.tolist(),
            "fields": SUMMARY_FIELDS
        }
    ]
    ft.save_data_to_workbook(data_map, file_path, "")
    ft.apply_number_format(file_path, "", "detail", DETAIL_NUMBER_FORMAT)
    ft.apply_column_width(file_path, "", "detail", DETAIL_WIDTH)
    ft.apply_number_format(file_path, "", "summary", SUMMARY_NUMBER_FORMAT)
    ft.apply_column_width(file_path, "", "summary", SUMMARY_WIDTH)

    print("核对结果保存成功，文件路径为：", file_path, "。")


if __name__ == '__main__':
    local_file_path = 'D:/90-投资收益月度核对/'
    remote_file_path = '//10.145.39.42/北京总部文件资料/资产管理部/14-运营支持部/投资收益月度核对/'
    tb_file_path_frag = 'TB文件/'
    check_result_file_path_frag = '核对结果/'
    matrix_file_name = 'TB-MI-MATRIX.xlsx'
    fair_value_at_begin_file_name = '期初资本公积.xlsx'
    # 判断是否能够连上共享，不能的话使用本地路径
    file_path = remote_file_path
    if not os.path.exists(file_path):
        file_path = local_file_path

    matrix_full_path = file_path + matrix_file_name
    fair_value_at_begin_full_path = file_path + fair_value_at_begin_file_name
    # 获取映射矩阵和期初资本公积数值
    fair_value_at_begin = ft.read_workbook_range_in_single_sheet(fair_value_at_begin_full_path).value
    matrix = get_tb_mi_matrix(file_path=matrix_full_path)

    print("请输入 %s 路径中的TB文件名称: " % (file_path + tb_file_path_frag))
    tb_file_name = input("> ")
    tb_file_path = file_path + tb_file_path_frag + tb_file_name
    tb_file_flag = os.path.exists(tb_file_path) and os.path.isfile(tb_file_path) and os.access(tb_file_path, os.R_OK)
    while not tb_file_flag:
        print("输入的文件不存在或者无法访问，请重新输入TB文件名称: ")
        tb_file_name = input("> ")
        tb_file_path = file_path + tb_file_path_frag + tb_file_name
        tb_file_flag = os.path.exists(tb_file_path) and os.path.isfile(tb_file_path) and os.access(tb_file_path, os.R_OK)
    # print("请输入核对结果保存文件路径，类似 d:/TB_CHECK_201709.xlsx : ")
    # file_path = input("> ")
    check_result_file_name = "CHECK_" + tb_file_name
    save_file_path = file_path + check_result_file_path_frag + check_result_file_name
    print("期初资本公积余额为：", fair_value_at_begin)
    print("读取TB文件数据......")
    tb_info = get_tb_info(file_path=tb_file_path)
    print("处理原始数据......")
    tb_tag_info = add_tag_to_tb(tb_info, matrix)
    print("信息汇总及处理结果保存......")
    summary_df = difference_summary(tb_tag_info, fair_value_at_begin)
    save_result(save_file_path, summary_df, tb_tag_info)

    input("输入任意键结束......")
