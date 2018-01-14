"""
根据BASIC_INFO，生成所输入期限内的月度现金流
"""
import circALM.caclDuration as calcD
import pandas as pd
import os

CASH_FLOW_DETAILS_LIST = [calcD.VALUATION_DATE, calcD.ASSET_TYPE,
                          calcD.ASSET_CODE, calcD.CASH_FLOW_DATE, calcD.CASH_FLOW_INTEREST_AMOUNT,
                          calcD.CASH_FLOW_PRINCIPAL_AMOUNT, calcD.CASH_FLOW_AMOUNT]


def calc_cash_flow_details(cash_flow_basic_df, valuation_date_str):
    calcD.w.start()
    cash_flow_details = calcD.calc_cash_flow(cash_flow_basic_df, valuation_date_str)
    term_mask = cash_flow_details[calcD.CASH_FLOW_TERM] > 0
    cash_flow_details = cash_flow_details[term_mask]
    cash_flow_details = cash_flow_details.ix[:, CASH_FLOW_DETAILS_LIST]
    cash_flow_details = cash_flow_details.sort_values([calcD.CASH_FLOW_DATE])
    calcD.w.stop()
    return cash_flow_details


def calc_cash_flow_for_product(clean_df, cash_flow_details):
    if not clean_df.empty:
        prd_asset_df = pd.DataFrame()
        for prd in clean_df[calcD.BASIC_DATA_COLUMN_ASSET_PRODUCT].unique():
            unit_hold_column = prd + '-HOLDING'
            interest_amout = prd + '-INTEREST'
            capital_amount = prd + '-CAPITAL'
            total_amount = prd + '-TOTAL'

            prd_asset_sum = clean_df.loc[clean_df[calcD.BASIC_DATA_COLUMN_ASSET_PRODUCT] == prd, calcD.BASIC_DATA_COLUMN_UNIT_HOLDING].groupby(clean_df[calcD.BASIC_DATA_COLUMN_ASSET_CODE]).sum()
            prd_asset_group_df = pd.DataFrame()
            prd_asset_group_df[calcD.ASSET_CODE] = prd_asset_sum.index
            prd_asset_group_df[unit_hold_column] = prd_asset_sum.values

            if prd_asset_df.empty:
                prd_asset_df = prd_asset_group_df
            else:
                prd_asset_df = pd.merge(prd_asset_df, prd_asset_group_df, how='outer', on=calcD.ASSET_CODE)
            cash_flow_details = pd.merge(cash_flow_details, prd_asset_group_df, how='left', on=calcD.ASSET_CODE)
            cash_flow_details[interest_amout] = cash_flow_details[calcD.CASH_FLOW_INTEREST_AMOUNT] * cash_flow_details[unit_hold_column] / 100
            cash_flow_details[capital_amount] = cash_flow_details[calcD.CASH_FLOW_PRINCIPAL_AMOUNT] * cash_flow_details[unit_hold_column] / 100
            cash_flow_details[total_amount] = cash_flow_details[calcD.CASH_FLOW_AMOUNT] * cash_flow_details[unit_hold_column] / 100

    return cash_flow_details, prd_asset_df


def calc_cash_flow_monthly(cash_flow_details, start_date=None, end_date=None):
    min_date = cash_flow_details[calcD.CASH_FLOW_DATE].min()
    max_date = cash_flow_details[calcD.CASH_FLOW_DATE].max()
    if start_date is None:
        start_date = min_date
    if end_date is None:
        end_date = max_date

    # prepare the statistic date range
    rng = pd.period_range(start=start_date, end=end_date, freq='M')
    date_df = pd.DataFrame(data={
        "TEMP": ""
    }, index=rng)

    # cash flow set date index, and turn the index to month
    temp_cf = cash_flow_details.copy()
    temp_cf.drop([calcD.VALUATION_DATE, calcD.ASSET_CODE, calcD.CASH_FLOW_INTEREST_AMOUNT,
                  calcD.CASH_FLOW_PRINCIPAL_AMOUNT, calcD.CASH_FLOW_AMOUNT], axis=1, inplace=True)
    temp_cf[calcD.CASH_FLOW_DATE] = pd.to_datetime(temp_cf[calcD.CASH_FLOW_DATE])
    temp_cf = temp_cf.set_index(calcD.CASH_FLOW_DATE)
    temp_cf = temp_cf.to_period('M')
    temp_cf = temp_cf.sort_index()

    # combine the date range and monthly cash flow
    monthly_df = pd.merge(date_df, temp_cf, how='left', left_index=True, right_index=True)
    monthly_sum = monthly_df.groupby(monthly_df.index).sum()
    monthly_sum.insert(0, 'CASH_FLOW_MONTH', monthly_sum.index)

    return monthly_sum


def save_result(cash_flow_details, monthly_sum_info, file_path):
    writer = pd.ExcelWriter(file_path)
    monthly_sum_info.to_excel(writer, "monthly", index=False)
    cash_flow_details.to_excel(writer, "detail", index=False)
    writer.save()
    # data_map = [
    #     {
    #         "sheet_name": "detail",
    #         "sheet_data": cash_flow_details.values.tolist(),
    #         "fields": cash_flow_details.columns.values.tolist()
    #     },
    #     {
    #         "sheet_name": "monthly",
    #         "sheet_data": monthly_sum_info.values.tolist(),
    #         "fields": monthly_sum_info.columns.values.tolist()
    #     }
    # ]
    # ft.save_data_to_workbook(data_map, file_path, "")


if __name__ == '__main__':
    local_file_path = 'D:/每日基础数据数值版/'
    remote_file_path = '//10.145.39.42/北京总部文件资料/资产管理部/8-风控合规部/每日基础数据更新/每日基础数据数值版/'
    file_name_prefix = '基础数据数值版'
    file_name_suffix = ".xlsx"
    file_path = remote_file_path
    if not os.path.exists(file_path):
        file_path = local_file_path
    print("请输入基础数据日期，类似 20170101: ")
    rp_date_str = input("> ")
    file_name = file_name_prefix + rp_date_str + file_name_suffix
    file_full_path = file_path + file_name
    file_flag = os.path.exists(file_full_path) and os.path.isfile(file_full_path) and os.access(file_full_path, os.R_OK)
    while not file_flag:
        print("输入的文件不存在或者无法访问 %s 。" % file_full_path)
        print("请重新输入基础数据日期，类似 20170101: ")
        rp_date_str = input("> ")
        file_name = file_name_prefix + rp_date_str + file_name_suffix
        file_full_path = file_path + file_name
        file_flag = os.path.exists(file_full_path) and os.path.isfile(file_full_path) and os.access(file_full_path,
                                                                                                    os.R_OK)

    print("从 %s 获取基础数据......" % file_full_path)
    basic_info_df = calcD.get_basic_info(file_name=file_name, file_path=file_path)
    print("提取品种基础信息......")
    clean_df = calcD.get_clean_basic_info_for_cash_flow_calc(basic_info_df)
    # clean_df.to_csv("d:/temp/clean_df.csv", index=False)
    print("获取现金流计算所需信息......")
    cash_flow_basic_df = calcD.get_cash_flow_basic_info(clean_df)
    # ---- CALC CASH FLOW DATA
    print("计算品种现金流信息......")
    cash_flow_details = calc_cash_flow_details(cash_flow_basic_df, rp_date_str)
    # cash_flow_details.to_csv("d:/temp/test_cf.csv", index=False)
    # ---- READ THE EXISTING DATE AND TEST
    # cash_flow_details = pd.read_csv("d:/temp/test_cf.csv", parse_dates=[calcD.CASH_FLOW_DATE])
    print("计算各产品持仓现金流信息......")
    cash_flow_details, prd_asset = calc_cash_flow_for_product(clean_df, cash_flow_details)
    # cash_flow_details.to_csv("d:/temp/test_cf_prd.csv", index=False)
    # prd_asset.to_csv("d:/temp/prd_asset.csv", index=False)
    print("按月度汇总现金流信息......")
    monthly_sum_info = calc_cash_flow_monthly(cash_flow_details)
    # monthly_sum_info.to_csv("d:/temp/monthly_sum_info.csv", index=True)
    output_file_name = 'CASH_FLOW_FOR_' + file_name
    output_file_full_path = file_path + output_file_name
    print("文件输出：%s " % output_file_full_path)
    save_result(cash_flow_details, monthly_sum_info, output_file_full_path)
    print("保存成功。")
    input("输入任意键结束......")
