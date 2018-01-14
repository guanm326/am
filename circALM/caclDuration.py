"""
按照ALM的要求计算估值和久期
input：债券、非标、存款的基础数据信息
    非债券类资产的信息包括：代码、起息日、到期日、首个付息日、票面利率、年付息次数、计息基准、评级
    债券信息：债券代码
output：资产的现金流、估值、修正久期、有效久期和关键久期
"""
import pandas as pd
import numpy as np
import datetime
import calendar
from WindPy import w
import tools.financial as financal
from scipy.optimize import fsolve
import circALM.calcDV10 as calc_dv10
import tools.filetools as ft
import os


VALUATION_DATE_STR = '20171231'
RISK_FREE_CURVE_NUMBER = 1231

# COLUMN INFO
ASSET_TYPE = 'ASSET_TYPE'
ASSET_CODE = 'ASSET_CODE'
ASSET_COST = 'ASSET_COST'
VALUE_DATE = 'VALUE_DATE'
MATURE_DATE = 'MATURE_DATE'
FIRST_PAY_DATE = 'FIRST_PAY_DATE'
COUPON_RATE = 'COUPON_RATE'
YTM = 'YTM'
ANNUAL_NUMBER = 'ANNUAL_NUMBER'
PAYMENT_BASE = 'PAYMENT_BASE'
BASE_CURVE = 'BASE_CURVE'
RATING = 'RATING'
VALUATION = 'VALUATION'
OPTION = 'OPTION'
NEXT_OPTION_DATE = 'NEXT_OPTION_DATE'
REMAINING_TERM = 'REMAINING_TERM'
TERM = 'TERM'
VALUATION_DATE = 'VALUATION_DATE'
SPREAD = 'SPREAD'
IRR_RATE = 'IRR_RATE'
IRR_VALUATION = 'IRR_VALUATION'
IRR_DISCOUNT = 'IRR_DISCOUNT'
CASH_FLOW_DATE = 'CASH_FLOW_DATE'
CASH_FLOW_AMOUNT = 'CASH_FLOW_AMOUNT'
CASH_FLOW_INTEREST_AMOUNT = 'CASH_FLOW_INTEREST_AMOUNT'
CASH_FLOW_PRINCIPAL_AMOUNT = 'CASH_FLOW_PRINCIPAL_AMOUNT'
CASH_FLOW_TERM = 'CASH_FLOW_TERM'
VALUATION_DATE_CURVE = 'VALUATION_DATE_CURVE'
DISCOUNT_RATE = 'DISCOUNT_RATE'
DISCOUNT_AMOUNT = 'DISCOUNT_AMOUNT'
VALUE_DATE_CURVE = 'VALUE_DATE_CURVE'
DISCOUNT_RATE_ADD_BP = 'DISCOUNT_RATE_ADD_BP'
DISCOUNT_AMOUNT_ADD_BP = 'DISCOUNT_AMOUNT_ADD_BP'
DISCOUNT_RATE_MINUS_BP = 'DISCOUNT_RATE_MINUS_BP'
DISCOUNT_AMOUNT_MINUS_BP = 'DISCOUNT_AMOUNT_MINUS_BP'

MOD_DURATION = 'MOD_DURATION'
EFFECTIVE_DURATION = 'EFFECTIVE_DURATION'
EFFECTIVE_DURATION_RANGE = 0.005
DV10_SUM = 'DV10_SUM'
KEY_DURATION = 'KEY_DURATION'

# ROW'S KEY  INFO
BOND_TYPE = 'BOND'

# Date operation
YEAR_MONTH = [[0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
              [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]]

"""
from monthly cash flow
"""
BASIC_DATA_FILE_NAME = '基础数据数值版20171130_HW_TEST.xlsx'
BASIC_DATA_FILE_PATH = '//10.145.39.42/北京总部文件资料/资产管理部/13-风控合规部/每日基础数据更新/每日基础数据数值版/'
BASIC_DATA_SHEET_NAME = '基础数据数值表'
BASIC_DATA_SHEETS = [BASIC_DATA_SHEET_NAME]

BASIC_DATA_COLUMN_ASSET_ACCOUNT = '账户'
BASIC_DATA_COLUMN_ASSET_PRODUCT = '产品'
BASIC_DATA_COLUMN_ASSET_MANAGER = '管理人'
BASIC_DATA_COLUMN_ASSET_CODE = '代码'
BASIC_DATA_COLUMN_ASSET_NAME = '名称'
BASIC_DATA_COLUMN_FIRST_CLASS = '数据库分类'
BASIC_DATA_COLUMN_SECOND_CLASS = '二级分类'
BASIC_DATA_COLUMN_THIRD_CLASS = '三级分类'
BASIC_DATA_COLUMN_STATISTICS_CLASS = '统计大类'
BASIC_DATA_COLUMN_ASSET_COUPON = '票息'
BASIC_DATA_COLUMN_PAY_BASE = '计息基准'
BASIC_DATA_COLUMN_PAY_NUMBER = '付息'
BASIC_DATA_COLUMN_VALUE_DATE = '起息日'
BASIC_DATA_COLUMN_FIRST_PAY_DATE = '首次付息日'
BASIC_DATA_COLUMN_MATURE_DATE = '到期日'
BASIC_DATA_COLUMN_UNIT_HOLDING = 'Unit Holding'
BASIC_DATA_COLUMN_BOOK_VALUE = '估值账面净价'
BASIC_DATA_COLUMN_CURRENCY = '币种'
BASIC_DATA_COLUMN_RATING = '债项外部信用评级'

CASH_FLOW_FIRST_CLASS_LIST = ['存款', '债券', '另类']
NON_OPEN_MARKET_BOND_LIST = ['ZW000001']

TOTAL_VALUATION_SHEET = 'TOTAL_VALUATION'
BASIC_INFO_SHEET = 'BASIC_INFO'
CASH_FLOW_INFO_SHEET = 'CASH_FLOW_INFO'

CALC_ITEM = [VALUATION, MOD_DURATION, EFFECTIVE_DURATION]
CALC_ITEM.extend(calc_dv10.KEY_YEARS)
CALC_ITEM.extend([DV10_SUM, KEY_DURATION])

MERGE_ITEM_ON_BASIC = [ASSET_CODE]
MERGE_ITEM_ON_BASIC.extend(CALC_ITEM)


def get_file_path_info():
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
    return file_path, file_name, rp_date_str


def get_basic_info(file_name=BASIC_DATA_FILE_NAME, file_path=BASIC_DATA_FILE_PATH, sheet_name=BASIC_DATA_SHEET_NAME):
    file_path = file_path + file_name
    basic_info = ft.read_workbook(file_path, "", BASIC_DATA_SHEETS)
    basic_info_df = ft.data_clean_in_one_sheet(basic_info, sheet_name, row_start_num=2, field_row_num=1,
                                               axis_one_drop_na_flag=False, axis_zero_drop_na_flag=False)

    return basic_info_df


def get_clean_basic_info_for_cash_flow_calc(basic_info_df):
    clean_df = pd.DataFrame()

    # 数据转移
    clean_df[BASIC_DATA_COLUMN_ASSET_ACCOUNT] = basic_info_df[BASIC_DATA_COLUMN_ASSET_ACCOUNT]
    clean_df[BASIC_DATA_COLUMN_ASSET_PRODUCT] = basic_info_df[BASIC_DATA_COLUMN_ASSET_PRODUCT]
    clean_df[BASIC_DATA_COLUMN_ASSET_MANAGER] = basic_info_df[BASIC_DATA_COLUMN_ASSET_MANAGER]
    clean_df[ASSET_CODE] = basic_info_df[BASIC_DATA_COLUMN_ASSET_CODE]
    clean_df[BASIC_DATA_COLUMN_ASSET_NAME] = basic_info_df[BASIC_DATA_COLUMN_ASSET_NAME]
    clean_df[BASIC_DATA_COLUMN_FIRST_CLASS] = basic_info_df[BASIC_DATA_COLUMN_FIRST_CLASS]
    clean_df[BASIC_DATA_COLUMN_SECOND_CLASS] = basic_info_df[BASIC_DATA_COLUMN_SECOND_CLASS]
    clean_df[BASIC_DATA_COLUMN_THIRD_CLASS] = basic_info_df[BASIC_DATA_COLUMN_THIRD_CLASS]
    clean_df[BASIC_DATA_COLUMN_STATISTICS_CLASS] = basic_info_df[BASIC_DATA_COLUMN_STATISTICS_CLASS]
    clean_df[BASIC_DATA_COLUMN_ASSET_COUPON] = basic_info_df[BASIC_DATA_COLUMN_ASSET_COUPON]
    if BASIC_DATA_COLUMN_PAY_BASE in basic_info_df.columns:
        clean_df[BASIC_DATA_COLUMN_PAY_BASE] = basic_info_df[BASIC_DATA_COLUMN_PAY_BASE]
    else:
        clean_df[BASIC_DATA_COLUMN_PAY_BASE] = 365
    clean_df[BASIC_DATA_COLUMN_PAY_NUMBER] = basic_info_df[BASIC_DATA_COLUMN_PAY_NUMBER]
    clean_df[BASIC_DATA_COLUMN_VALUE_DATE] = pd.to_datetime(basic_info_df[BASIC_DATA_COLUMN_VALUE_DATE])
    clean_df[BASIC_DATA_COLUMN_FIRST_PAY_DATE] = pd.to_datetime(basic_info_df[BASIC_DATA_COLUMN_FIRST_PAY_DATE])
    clean_df[BASIC_DATA_COLUMN_MATURE_DATE] = pd.to_datetime(basic_info_df[BASIC_DATA_COLUMN_MATURE_DATE])
    clean_df[BASIC_DATA_COLUMN_UNIT_HOLDING] = basic_info_df[BASIC_DATA_COLUMN_UNIT_HOLDING]
    clean_df[BASIC_DATA_COLUMN_BOOK_VALUE] = basic_info_df[BASIC_DATA_COLUMN_BOOK_VALUE]
    clean_df[BASIC_DATA_COLUMN_CURRENCY] = basic_info_df[BASIC_DATA_COLUMN_CURRENCY]
    clean_df[BASIC_DATA_COLUMN_RATING] = basic_info_df[BASIC_DATA_COLUMN_RATING]

    # 数据筛选
    pay_mask = clean_df[BASIC_DATA_COLUMN_STATISTICS_CLASS] != '权益'
    clean_df = clean_df[pay_mask]

    class_mask = (clean_df[BASIC_DATA_COLUMN_FIRST_CLASS] == '存款') | (clean_df[BASIC_DATA_COLUMN_FIRST_CLASS] == '另类') | (clean_df[BASIC_DATA_COLUMN_FIRST_CLASS] == '债券')
    clean_df = clean_df[class_mask]

    # 外币存款的unit holding使用估值账面价值
    clean_df.loc[clean_df[BASIC_DATA_COLUMN_CURRENCY] != 'CNY', BASIC_DATA_COLUMN_UNIT_HOLDING] = \
        clean_df.loc[clean_df[BASIC_DATA_COLUMN_CURRENCY] != 'CNY', BASIC_DATA_COLUMN_BOOK_VALUE]

    return clean_df


def rating_to_curve(rating):
    if rating == 'AAA':
        return 1261
    elif rating == 'AA+':
        return 1441
    elif rating == 'AA':
        return 1251
    else:
        return 1231


def get_cash_flow_basic_info(clean_df):
    cash_flow_basic = pd.DataFrame()
    clean_df = clean_df.replace("#N/A", "")
    cash_flow_basic[ASSET_CODE] = clean_df[ASSET_CODE]
    cash_flow_basic[VALUE_DATE] = pd.to_datetime(clean_df[BASIC_DATA_COLUMN_VALUE_DATE])
    cash_flow_basic[MATURE_DATE] = pd.to_datetime(clean_df[BASIC_DATA_COLUMN_MATURE_DATE])
    cash_flow_basic[FIRST_PAY_DATE] = pd.to_datetime(clean_df[BASIC_DATA_COLUMN_FIRST_PAY_DATE])
    cash_flow_basic[COUPON_RATE] = pd.to_numeric(clean_df[BASIC_DATA_COLUMN_ASSET_COUPON])
    cash_flow_basic[ANNUAL_NUMBER] = pd.to_numeric(clean_df[BASIC_DATA_COLUMN_PAY_NUMBER])
    cash_flow_basic[PAYMENT_BASE] = pd.to_numeric(clean_df[BASIC_DATA_COLUMN_PAY_BASE])
    cash_flow_basic[BASIC_DATA_COLUMN_FIRST_CLASS] = clean_df[BASIC_DATA_COLUMN_FIRST_CLASS]
    cash_flow_basic[RATING] = clean_df[BASIC_DATA_COLUMN_RATING]
    cash_flow_basic[BASE_CURVE] = cash_flow_basic[RATING].map(rating_to_curve)

    # 存款的评级置空（按照ALM要求，存款按无评级计算）
    cash_flow_basic.loc[cash_flow_basic[BASIC_DATA_COLUMN_FIRST_CLASS] == '存款', RATING] = ''

    # 增加类别
    cash_flow_basic.loc[cash_flow_basic[BASIC_DATA_COLUMN_FIRST_CLASS] == '债券', ASSET_TYPE] = 'BOND'
    cash_flow_basic.loc[cash_flow_basic[BASIC_DATA_COLUMN_FIRST_CLASS] != '债券', ASSET_TYPE] = 'OTHER'

    # ZW000001，非公开市场债券，单独处理
    cash_flow_basic.loc[cash_flow_basic[ASSET_CODE] == 'ZW000001', ASSET_TYPE] = 'OTHER'
    cash_flow_basic = cash_flow_basic.drop_duplicates([ASSET_CODE])

    return cash_flow_basic


def save_result(file_path, total_valuation, basic_info, cash_flow_info):
    writer = pd.ExcelWriter(file_path)
    if total_valuation is not None:
        total_valuation.to_excel(writer, TOTAL_VALUATION_SHEET, index=False)
    if basic_info is not None:
        basic_info.to_excel(writer, BASIC_INFO_SHEET, index=False)
    if cash_flow_info is not None:
        cash_flow_info.to_excel(writer, CASH_FLOW_INFO_SHEET, index=False)
    writer.save()


def get_new_info(file_path):
    clean_df = pd.read_excel(file_path,
                             sheetname=TOTAL_VALUATION_SHEET,
                             parse_dates=[BASIC_DATA_COLUMN_VALUE_DATE, BASIC_DATA_COLUMN_MATURE_DATE,
                                          BASIC_DATA_COLUMN_FIRST_PAY_DATE],
                             parse_floats=[BASIC_DATA_COLUMN_ASSET_COUPON, BASIC_DATA_COLUMN_PAY_BASE,
                                           BASIC_DATA_COLUMN_PAY_NUMBER, BASIC_DATA_COLUMN_UNIT_HOLDING,
                                           BASIC_DATA_COLUMN_BOOK_VALUE])
    clean_df.fillna("")
    cash_flow_basic_df = pd.read_excel(file_path,
                                       sheetname=BASIC_INFO_SHEET,
                                       parse_dates=[VALUE_DATE, MATURE_DATE, FIRST_PAY_DATE, NEXT_OPTION_DATE])
    cash_flow_basic_df.fillna("")
    cash_flow_info = pd.read_excel(file_path,
                                   sheetname=CASH_FLOW_INFO_SHEET,
                                   parse_dates=[CASH_FLOW_DATE])
    cash_flow_info.fillna("")

    return clean_df, cash_flow_basic_df, cash_flow_info


"""
get from monthly cash flow end
"""


def check_info_integrity(cash_flow_basic_df, cash_flow_info):
    check_flag = True
    result_str = ""
    # 判断基础信息中是否有起息日基准利率列，以及 起息日基准利率是否有空数据
    basic_columns = cash_flow_basic_df.columns
    if VALUE_DATE_CURVE not in basic_columns:
        check_flag = False
        result_str += "基础信息缺失 %s 列；" % VALUE_DATE_CURVE
    else:
        value_date_curve_info = cash_flow_basic_df.loc[cash_flow_basic_df[ASSET_TYPE] == 'OTHER', VALUE_DATE_CURVE]
        value_date_curve_nan_count = len(value_date_curve_info[np.isnan(value_date_curve_info)])
        if value_date_curve_nan_count > 0:
            check_flag = False
            result_str += "基础信息中，OTHER 类资产 %s 列有 %d 条空数据；" % (VALUE_DATE_CURVE, value_date_curve_nan_count)
    # 判断现金流信息中是否有估值日基准利率列，以及 起息日基准利率是否有空数据
    cash_flow_columns = cash_flow_info.columns
    if VALUATION_DATE_CURVE not in cash_flow_columns:
        check_flag = False
        result_str += "现金流信息缺失 %s 列；" % VALUATION_DATE_CURVE
    else:
        valuation_date_curve_info = cash_flow_info.loc[cash_flow_info[CASH_FLOW_TERM] > 0, VALUATION_DATE_CURVE]
        valuation_date_curve_nan_count = len(valuation_date_curve_info[np.isnan(valuation_date_curve_info)])
        if valuation_date_curve_nan_count > 0:
            check_flag = False
            result_str += "现金流信息的 %s 列有 %d 条空数据；" % (VALUATION_DATE_CURVE, valuation_date_curve_nan_count)

    return check_flag, result_str


def add_months(begin_date, months):
    n = begin_date.year * 12 + begin_date.month - 1
    n = n + months
    ryear = int(n / 12)
    rmonth = int(n % 12 + 1)
    rday = int(begin_date.day)
    if calendar.isleap(ryear):
        if rday > YEAR_MONTH[1][rmonth]:
            rday = YEAR_MONTH[1][rmonth]
    else:
        if rday > YEAR_MONTH[0][rmonth]:
            rday = YEAR_MONTH[0][rmonth]

    return begin_date.replace(year=ryear, month=rmonth, day=rday)


def to_date_type(what):
    if (type(what) is pd.Timestamp) or (type(what) is datetime.datetime):
        return what.date()
    else:
        return what


def calc_bond_spread(x, *args):
    spread = x
    cf_info = args[0]
    bond_valuation = args[1]

    return [(cf_info.CASH_FLOW_AMOUNT / (((cf_info.VALUATION_DATE_CURVE / 100 + spread) + 1) ** cf_info.CASH_FLOW_TERM)).sum() - bond_valuation]


def calc_non_standard_ytm(x, *args):
    ytm = x
    cf_info = args[0]
    valuation = args[1]

    return [(cf_info.CASH_FLOW_AMOUNT / ((ytm + 1) ** cf_info.CASH_FLOW_TERM)).sum() - valuation]


"""
获取资产基本信息
"""


def fetch_basic_info(file_path=r'd:\BASIC_INFO.csv'):
    df = pd.read_csv(file_path, parse_dates=['VALUE_DATE', 'MATURE_DATE', 'FIRST_PAY_DATE'])
    return df


"""
根据基本信息计算现金流，并根据行权判断获取校正的现金流
"""


def calc_cash_flow(basic_info, valuation_date_str=VALUATION_DATE_STR):
    cash_flow = pd.DataFrame()
    for index, row in basic_info.iterrows():
        # 循环计算品种的现金流
        temp = pd.DataFrame()
        code = row[ASSET_CODE]
        base_curve = row[BASE_CURVE]
        if row[ASSET_TYPE] == BOND_TYPE:
            basic_info.loc[index, BASE_CURVE] = RISK_FREE_CURVE_NUMBER
            base_curve = RISK_FREE_CURVE_NUMBER
            # 获取债券起息日、到期日、年付息次数、票面、到期收益率
            bond_base_info = w.wss(code, "carrydate,maturitydate,interestfrequency,couponrate2,ytm_b,amount,nxoptiondate,ptmyear,term",
                                   "tradeDate="+valuation_date_str+";returnType=1;ratingAgency=101;date="+valuation_date_str+";type=All")
            bond_base_info = pd.DataFrame(bond_base_info.Data, index=bond_base_info.Fields, columns=['info'])
            value_date = bond_base_info.loc['CARRYDATE', 'info']
            mature_date = bond_base_info.loc['MATURITYDATE', 'info']
            basic_info.loc[index, VALUE_DATE] = value_date
            basic_info.loc[index, MATURE_DATE] = mature_date
            basic_info.loc[index, TERM] = bond_base_info.loc['TERM', 'info']
            basic_info.loc[index, COUPON_RATE] = bond_base_info.loc['COUPONRATE2', 'info'] / 100
            basic_info.loc[index, ANNUAL_NUMBER] = bond_base_info.loc['INTERESTFREQUENCY', 'info']
            basic_info.loc[index, RATING] = bond_base_info.loc['AMOUNT', 'info']
            # 获取估值日期的中债估值信息
            bond_valuation_info = w.wsd(code, "price_cnbd,dirty_cnbd,yield_cnbd,,matu_cnbd,modidura_cnbd", valuation_date_str,
                                        valuation_date_str, "credibility=1", "credibility=1;Days=Alldays")
            bond_valuation_info = pd.DataFrame(bond_valuation_info.Data, index=bond_valuation_info.Fields,
                                               columns=['info'])
            basic_info.loc[index, VALUATION] = bond_valuation_info.loc['DIRTY_CNBD', 'info']
            basic_info.loc[index, YTM] = bond_valuation_info.loc['YIELD_CNBD', 'info'] / 100
            # 在获取债券估值信息时，获取修正久期信息
            basic_info.loc[index, MOD_DURATION] = bond_valuation_info.loc['MODIDURA_CNBD', 'info']
            # 债券现金流从wind获取
            bond_cash_flow = w.wsd(code, "dailycf", value_date, mature_date, "Days=Alldays")
            bond_cash_flow = pd.DataFrame(bond_cash_flow.Data, index=bond_cash_flow.Fields,
                                          columns=bond_cash_flow.Times)
            bond_cash_flow = bond_cash_flow.T
            cash_flow_mask = bond_cash_flow['DAILYCF'] > 0
            bond_cash_flow = bond_cash_flow[cash_flow_mask]
            temp = bond_cash_flow.copy()
            temp.columns = [CASH_FLOW_AMOUNT]
            temp[CASH_FLOW_DATE] = bond_cash_flow.index

            # 补充每次现金流的利息和本金信息
            temp[CASH_FLOW_PRINCIPAL_AMOUNT] = 0
            temp.loc[to_date_type(mature_date), CASH_FLOW_PRINCIPAL_AMOUNT] = 100
            temp[CASH_FLOW_INTEREST_AMOUNT] = temp[CASH_FLOW_AMOUNT] - temp[CASH_FLOW_PRINCIPAL_AMOUNT]

            # 行权判断采用中债推荐
            recommend_term = round(bond_valuation_info.loc['MATU_CNBD', 'info'], 2)
            term = round(bond_base_info.loc['PTMYEAR', 'info'], 2)
            next_option_date = bond_base_info.loc['NXOPTIONDATE', 'info']
            basic_info.loc[index, REMAINING_TERM] = recommend_term
            # 比较两个期限
            if abs(recommend_term - term) < 0.02:
                # 不行权
                basic_info.loc[index, OPTION] = False
                basic_info.loc[index, NEXT_OPTION_DATE] = ""
            else:
                # 行权，修正现金流为下一行权日
                basic_info.loc[index, OPTION] = True
                basic_info.loc[index, NEXT_OPTION_DATE] = next_option_date
                if next_option_date is not None:
                    next_option_date = to_date_type(datetime.datetime.strptime(next_option_date, "%Y-%m-%d"))
                    option_date_mask = temp[CASH_FLOW_DATE] <= next_option_date
                    temp = temp[option_date_mask]
                    # 行权日的现金流加上票面100
                    temp.loc[next_option_date, CASH_FLOW_AMOUNT] = temp.loc[next_option_date, CASH_FLOW_AMOUNT] + 100
                    temp.loc[next_option_date, CASH_FLOW_PRINCIPAL_AMOUNT] = 100
        else:
            # 程序计算现金流
            calc_base = row[PAYMENT_BASE]
            if calc_base == "" or np.isnan(calc_base):
                calc_base = 365
            rate = row[COUPON_RATE]
            time_per_year = row[ANNUAL_NUMBER]
            value_date = row[VALUE_DATE]
            mature_date = row[MATURE_DATE]
            # 补充剩余期限
            basic_info.loc[index, REMAINING_TERM] = (to_date_type(mature_date) - datetime.datetime.strptime(
                valuation_date_str, "%Y%m%d").date()).days / 365
            basic_info.loc[index, TERM] = (to_date_type(mature_date) - to_date_type(value_date)).days / 365
            # 年付息次数为0，或为空，默认按到期一次返本派息计算
            if time_per_year > 0:
                month_gap = 12 / time_per_year
                assume_first_date = add_months(value_date, month_gap)
                first_pay_date = row[FIRST_PAY_DATE]
                if not (first_pay_date > value_date):
                    first_pay_date = assume_first_date
                first_pay_date_flag = first_pay_date == assume_first_date

                dates = [to_date_type(first_pay_date)]
                # 计算首个付息日付息金额
                if first_pay_date_flag:
                    first_pay_amount = 100 * rate / time_per_year
                else:
                    first_pay_amount = 100 * rate * (first_pay_date - value_date).days / calc_base
                if mature_date == first_pay_date:
                    first_pay_amount += 100
                cf = [first_pay_amount]

                # 计算首个付息日至到期日的现金流
                cf_date = first_pay_date
                while (mature_date - add_months(cf_date, month_gap)).days >= 0:
                    cf_date = add_months(cf_date, month_gap)
                    cf_amount = 100 * rate / time_per_year
                    if mature_date == cf_date:
                        cf_amount += 100
                    dates.append(to_date_type(cf_date))
                    cf.append(cf_amount)

                # 循环结束后，判断是否cf_date是否小于mature_date，若是，则还有最后一期现金流
                if (mature_date - cf_date).days > 0:
                    dates.append(to_date_type(mature_date))
                    last_amount = 100 * rate * (mature_date - cf_date).days / calc_base + 100
                    cf.append(last_amount)
            else:
                dates = [to_date_type(mature_date)]
                pay_amt = 100 * rate * (mature_date - value_date).days / 365 + 100
                cf = [pay_amt]

            temp[CASH_FLOW_DATE] = dates
            temp[CASH_FLOW_DATE].astype(np.object)
            temp[CASH_FLOW_AMOUNT] = cf
            # 补充本金和利息金额
            temp[CASH_FLOW_PRINCIPAL_AMOUNT] = 0
            temp.loc[temp[CASH_FLOW_DATE] == to_date_type(mature_date), CASH_FLOW_PRINCIPAL_AMOUNT] = 100
            temp[CASH_FLOW_INTEREST_AMOUNT] = temp[CASH_FLOW_AMOUNT] - temp[CASH_FLOW_PRINCIPAL_AMOUNT]
            # 行权判断在单元格中进行，若行权直接修改品种到期日
            # 判断方法为：使用远期的即期利率（再融资利率）与实际利率进行比较，GAP为30bp默认不行权
            pass

        temp[ASSET_CODE] = code
        temp[ASSET_TYPE] = row[ASSET_TYPE]
        if base_curve:
            temp[BASE_CURVE] = base_curve
        else:
            temp[BASE_CURVE] = 1231
        cash_flow = pd.concat([cash_flow, temp])

    if not cash_flow.empty:
        cash_flow = cash_flow.reset_index(drop=True)
        cash_flow[CASH_FLOW_TERM] = cash_flow[CASH_FLOW_DATE].transform(
            lambda x: (x - to_date_type(datetime.datetime.strptime(valuation_date_str, "%Y%m%d"))).days/365)
        cash_flow[VALUATION_DATE] = valuation_date_str
        cash_flow[VALUATION_DATE_CURVE] = ""
        basic_info[VALUATION_DATE] = valuation_date_str
        # term_mask = cash_flow[CASH_FLOW_TERM] > 0
        # cash_flow = cash_flow[term_mask]
    return cash_flow


"""
现金流中补充IRR等信息
"""


def extend_irr_info(basic_info, basic_cash_flow):
    if not basic_info.empty:
        asset_code_flag = ASSET_COST in basic_info.columns
        for index, row in basic_info.iterrows():
            code = row[ASSET_CODE]
            code_mask = basic_cash_flow[ASSET_CODE] == code
            cf = basic_cash_flow[code_mask]
            if not cf.empty:
                price = 100
                if asset_code_flag:
                    price = row[ASSET_COST]
                if np.isnan(price):
                    price = 100
                first_cf = 0 - price
                irr_cf = [first_cf]
                irr_cf.extend(cf[CASH_FLOW_AMOUNT])

                irr_dates = [to_date_type(row[VALUE_DATE])]
                irr_dates.extend(cf[CASH_FLOW_DATE])

                irr_info = list(zip(irr_dates, irr_cf))
                if irr_info:
                    irr = financal.xirr(irr_info)

                    # IRR 更新到basic info
                    basic_info.loc[index, IRR_RATE] = irr
                    basic_cash_flow.loc[basic_cash_flow[ASSET_CODE] == code, IRR_RATE] = irr
                    basic_cash_flow.loc[((basic_cash_flow[ASSET_CODE] == code) & (basic_cash_flow[CASH_FLOW_TERM] > 0)),
                                        IRR_DISCOUNT] = cf[CASH_FLOW_AMOUNT] / ((1 + irr) ** cf[CASH_FLOW_TERM])
                    irr_valuation = basic_cash_flow.loc[basic_cash_flow[ASSET_CODE] == code, IRR_DISCOUNT].sum()
                    basic_info.loc[index, IRR_VALUATION] = irr_valuation


"""
根据现金流和基本信息，填充：
    step1、df中相关要素：
           债券的SPREAD基于中债全价估值进行推算
           其他有评级的为基于标准资产的流动性溢价G_SPREAD
           其他无评级为基于无风险利率的综合利差Z_SPREAD
    step2、cf中各剩余期限现金流折现率、折现金额
    step3、df中补充pv
    step4、折算非债券资产的YTM
"""


def fill_fit_curve(basic_info, cash_flow):
    # 获取估值日基准曲线的同期限利率
    # TODO 上一步骤在excel中用函数实现，通过读取excel方式获取
    if not basic_info.empty:
        for index, row in basic_info.iterrows():
            code = row[ASSET_CODE]
            valuation = row[VALUATION]
            # 债券类通过获取同期限国债基准利率现金流信息折算倒算综合利差
            if row[ASSET_TYPE] == BOND_TYPE:
                term_mask = (cash_flow[ASSET_CODE] == code) & (cash_flow[CASH_FLOW_TERM] > 0)
                scf = cash_flow[term_mask]
                spread = fsolve(calc_bond_spread, 0.025, args=(scf, valuation))
                cash_flow.loc[term_mask, SPREAD] = spread
                cash_flow.loc[term_mask, DISCOUNT_RATE] = cash_flow.loc[term_mask, VALUATION_DATE_CURVE] / 100 + spread
                cash_flow.loc[term_mask, DISCOUNT_AMOUNT] = cash_flow.loc[term_mask, CASH_FLOW_AMOUNT] / (
                        (1 + cash_flow.loc[term_mask, DISCOUNT_RATE]) ** cash_flow.loc[term_mask, CASH_FLOW_TERM])
                basic_info.loc[index, SPREAD] = spread
            # 非债券类品种获取起息日同期限基准利率作为基准，计算流动性溢价
            else:
                # 计算利差，拟合折现率，计算pv
                irr_rate = row[IRR_RATE]
                value_date_curve = row[VALUE_DATE_CURVE]
                spread = irr_rate - value_date_curve / 100
                basic_info.loc[index, SPREAD] = spread

                term_mask = (cash_flow[ASSET_CODE] == code) & (cash_flow[CASH_FLOW_TERM] > 0)
                scf = cash_flow[term_mask]
                cash_flow.loc[term_mask, SPREAD] = spread
                cash_flow.loc[term_mask, DISCOUNT_RATE] = cash_flow.loc[term_mask, VALUATION_DATE_CURVE] / 100 + spread
                cash_flow.loc[term_mask, DISCOUNT_AMOUNT] = cash_flow.loc[term_mask, CASH_FLOW_AMOUNT] / (
                        (1 + cash_flow.loc[term_mask, DISCOUNT_RATE]) ** cash_flow.loc[term_mask, CASH_FLOW_TERM])
                pv = cash_flow.loc[term_mask, DISCOUNT_AMOUNT].sum()
                basic_info.loc[index, VALUATION] = pv

                # 计算资产的YTM
                ytm = fsolve(calc_non_standard_ytm, irr_rate, args=(scf, pv))
                basic_info.loc[index, YTM] = ytm


"""
计算修正久期：
债券的修正久期从wind获取
其他的通过alm公式计算
"""


def calc_mod_duration(basic_info, cash_flow):
    if not basic_info.empty:
        for index, row in basic_info.iterrows():
            if not (row[ASSET_TYPE] == BOND_TYPE):
                ytm = row[YTM]
                pv = row[VALUATION]
                code = row[ASSET_CODE]
                time_per_year = row[ANNUAL_NUMBER]
                code_and_term_mask = (cash_flow[ASSET_CODE] == code) & (cash_flow[CASH_FLOW_TERM] > 0)
                scf = cash_flow[code_and_term_mask].copy()
                scf = scf.reset_index()
                cf_count = scf.CASH_FLOW_AMOUNT.count()
                # 处于最后一个计息周期的计算
                if cf_count > 1:
                    scf[MOD_DURATION] = ((scf.index + 1) * scf[CASH_FLOW_AMOUNT]) / \
                                        ((1 + ytm / time_per_year) ** (scf.index + 2)) / pv / time_per_year
                    mod_duration = scf.MOD_DURATION.sum()
                    basic_info.loc[index, MOD_DURATION] = mod_duration
                    cash_flow.loc[code_and_term_mask, MOD_DURATION] = scf[MOD_DURATION].data
                # 年付息次数大于0时，使用最后一期现金流计算FV
                elif cf_count == 1:
                    scf[MOD_DURATION] = scf[CASH_FLOW_AMOUNT] * scf[CASH_FLOW_TERM] / \
                                        ((1 + ytm * scf[CASH_FLOW_TERM]) ** 2) / pv
                    mod_duration = scf.MOD_DURATION.sum()
                    basic_info.loc[index, MOD_DURATION] = mod_duration
                    cash_flow.loc[code_and_term_mask, MOD_DURATION] = scf[MOD_DURATION].data
                else:
                    print(code, " : no cash flows, the basic info data will be removed.")
                    basic_info.drop([index], inplace=True)


"""
计算有效久期:
    债券通过ytm加减50bp重新定价的浮动作为计算依据
    其他资产通过调整折现率重新定价作为计算依据
"""


def calc_effective_duration(basic_info, cash_flow, valuation_date_str=VALUATION_DATE_STR):
    if not basic_info.empty:
        bond_codes = []
        bond_vars_add = []
        bond_vars_minus = []
        pvs = []
        columns = basic_info.columns
        for index, row in basic_info.iterrows():
            code = row[ASSET_CODE]
            pv = row[VALUATION]
            if row[ASSET_TYPE] == BOND_TYPE:
                ytm = row[YTM]
                time_per_year = row[ANNUAL_NUMBER]
                value_date = row[VALUE_DATE]
                mature_date = row[MATURE_DATE]
                if NEXT_OPTION_DATE in columns:
                    next_option_date = row[NEXT_OPTION_DATE]
                    option_choice = row[OPTION]
                    if option_choice:
                        mature_date = next_option_date
                coupon_rate = row[COUPON_RATE]
                bond_info_df = w.wss(code, "issue_issueprice,interestfrequency,couponrate2,baserate2")
                bond_info_df = pd.DataFrame(bond_info_df.Data, index=bond_info_df.Fields, columns=['info'])
                issue_price = bond_info_df.loc['ISSUE_ISSUEPRICE', 'info']
                if not (time_per_year > 0):
                    time_per_year = 0
                bond_codes.append(code)
                bond_vars_add.append("balanceDate=" + valuation_date_str + ";yield=" + str((ytm + EFFECTIVE_DURATION_RANGE) * 100) + ";bondPriceType=2;maturityDate=" + datetime.datetime.strftime(mature_date, '%Y%m%d') + ";paymentFreq=" + str(int(time_per_year)) + ";parRate=" + str(coupon_rate * 100) + ";parValue=100;valueDate=" + datetime.datetime.strftime(value_date, '%Y%m%d') + ";issuePrice=" + str(issue_price))
                bond_vars_minus.append("balanceDate=" + valuation_date_str + ";yield=" + str((
                                                                                                   ytm - EFFECTIVE_DURATION_RANGE) * 100) + ";bondPriceType=2;maturityDate=" + datetime.datetime.strftime(
                    mature_date, '%Y%m%d') + ";paymentFreq=" + str(int(time_per_year)) + ";parRate=" + str(
                    coupon_rate * 100) + ";parValue=100;valueDate=" + datetime.datetime.strftime(value_date,
                                                                                                 '%Y%m%d') + ";issuePrice=" + str(
                    issue_price))
                pvs.append(pv)
            else:
                code_and_term_mask = (cash_flow[ASSET_CODE] == code) & (cash_flow[CASH_FLOW_TERM] > 0)
                cash_flow.loc[code_and_term_mask, DISCOUNT_RATE_ADD_BP] = \
                    cash_flow.loc[code_and_term_mask, DISCOUNT_RATE] + EFFECTIVE_DURATION_RANGE
                cash_flow.loc[code_and_term_mask, DISCOUNT_RATE_MINUS_BP] = \
                    cash_flow.loc[code_and_term_mask, DISCOUNT_RATE] - EFFECTIVE_DURATION_RANGE
                cash_flow.loc[code_and_term_mask, DISCOUNT_AMOUNT_ADD_BP] = \
                    cash_flow.loc[code_and_term_mask, CASH_FLOW_AMOUNT] / ((1 + cash_flow.loc[code_and_term_mask, DISCOUNT_RATE_ADD_BP]) ** cash_flow.loc[code_and_term_mask, CASH_FLOW_TERM])
                cash_flow.loc[code_and_term_mask, DISCOUNT_AMOUNT_MINUS_BP] = \
                    cash_flow.loc[code_and_term_mask, CASH_FLOW_AMOUNT] / (
                            (1 + cash_flow.loc[code_and_term_mask, DISCOUNT_RATE_MINUS_BP]) **
                            cash_flow.loc[code_and_term_mask, CASH_FLOW_TERM])
                add_bp_pv = cash_flow.loc[code_and_term_mask, DISCOUNT_AMOUNT_ADD_BP].sum()
                minus_bp_pv = cash_flow.loc[code_and_term_mask, DISCOUNT_AMOUNT_MINUS_BP].sum()
                effective_duration = (minus_bp_pv - add_bp_pv) / (pv * 0.01)
                basic_info.loc[index, EFFECTIVE_DURATION] = effective_duration

        for i in range(len(bond_codes)):
            add_bp_df = w.wss(bond_codes[i], "calc_price", bond_vars_add[i])
            add_bp_df = pd.DataFrame(add_bp_df.Data, index=add_bp_df.Fields, columns=['info'])
            add_bp_pv = add_bp_df.loc['CALC_PRICE', 'info']

            minus_bp_df = w.wss(bond_codes[i], "calc_price", bond_vars_minus[i])
            minus_bp_df = pd.DataFrame(minus_bp_df.Data, index=minus_bp_df.Fields, columns=['info'])
            minus_bp_pv = minus_bp_df.loc['CALC_PRICE', 'info']

            effective_duration = (minus_bp_pv - add_bp_pv) / (pvs[i] * 0.01)
            basic_info.loc[basic_info[ASSET_CODE] == bond_codes[i], EFFECTIVE_DURATION] = effective_duration


"""
计算关键久期
"""


def calc_key_duration(basic_info, cash_flow):
    if not basic_info.empty:
        key_years = calc_dv10.KEY_YEARS
        all_info = pd.DataFrame(columns=key_years)
        for index, row in basic_info.iterrows():
            scf = pd.DataFrame()
            code = row[ASSET_CODE]
            term_mask = (cash_flow[ASSET_CODE] == code) & (cash_flow[CASH_FLOW_TERM] > 0)
            scf[calc_dv10.TIME_LIMIT_STR] = cash_flow.loc[term_mask, CASH_FLOW_TERM]
            scf[calc_dv10.CASH_FLOW_STR] = cash_flow.loc[term_mask, CASH_FLOW_AMOUNT]
            scf[calc_dv10.DISCOUNT_STR] = cash_flow.loc[term_mask, DISCOUNT_RATE]
            dv10 = calc_dv10.calc_dv10_from_cash_flow(code, scf, key_years)
            all_info = pd.concat([all_info, dv10])
        all_info[DV10_SUM] = all_info.apply(lambda x: x.sum(), axis=1)
        all_info[ASSET_CODE] = all_info.index

        basic_info = pd.merge(basic_info, all_info, on=ASSET_CODE)
        basic_info[KEY_DURATION] = 1000 * basic_info[DV10_SUM] / basic_info[VALUATION]
        return basic_info


"""
从d盘《VALUE_DATE_BASE_RATE.csv》获取已经保存的起息日基准利率
"""


def extend_valuation_date_base(basic_info):
    base_curve_rate = pd.read_csv(r"d:\VALUE_DATE_BASE_RATE.csv")
    if not basic_info.empty:
        for index, row in basic_info.iterrows():
            code = row[ASSET_CODE]
            code_mask = base_curve_rate[ASSET_CODE] == code
            code_df = base_curve_rate[code_mask]
            if code_df[ASSET_CODE].count() > 0:
                base_rate = code_df.iloc[0, 1]
                basic_info.loc[basic_info[ASSET_CODE] == code, VALUE_DATE_CURVE] = base_rate


def update_position_info(clean_df, cash_flow_basic_df):
    merge_cash_flow_basic_df = cash_flow_basic_df.ix[:, MERGE_ITEM_ON_BASIC]
    clean_df = pd.merge(clean_df, merge_cash_flow_basic_df, how='left', on=ASSET_CODE)
    for item in CALC_ITEM:
        if item == VALUATION:
            clean_df[item] = clean_df[BASIC_DATA_COLUMN_UNIT_HOLDING] * clean_df[item] / 100
        else:
            clean_df[item] = clean_df[BASIC_DATA_COLUMN_UNIT_HOLDING] * clean_df[item]
    return clean_df


if __name__ == "__main__":
    w.start()
    # 获取文件路径信息
    file_path, file_name, rp_date_str = get_file_path_info()
    # 输出文件
    output_file_name = 'ALM_VALUATION_FOR_' + file_name
    output_file_full_path = file_path + output_file_name
    out_file_flag = os.path.exists(output_file_full_path) and os.path.isfile(output_file_full_path) and os.access(output_file_full_path, os.R_OK)
    if not out_file_flag:
        print("未检测到临时保存文件，首先从基础数据文件获取信息......")
        # 获取基本信息
        basic_info_df = get_basic_info(file_name=file_name, file_path=file_path)
        # 清洗数据，摘取需要估值的仓位信息
        print("清洗数据，获取固收类型的存款、另类和债券资产......")
        clean_df = get_clean_basic_info_for_cash_flow_calc(basic_info_df)
        # 获取品种的去重值
        print("获取量化计算所需信息......")
        cash_flow_basic_df = get_cash_flow_basic_info(clean_df)
        # 根据基础信息补充相关信息，并进行基础计算
        cash_flow_info = calc_cash_flow(cash_flow_basic_df)
        extend_irr_info(cash_flow_basic_df, cash_flow_info)
        extend_valuation_date_base(cash_flow_basic_df)
        # 信息临时保存
        print("文件临时保存至：%s " % output_file_full_path)
        save_result(output_file_full_path, clean_df, cash_flow_basic_df, cash_flow_info)
        print("临时保存成功......")
        # 提示用户补充信息
        print("请在 %s Sheet页补充另类和存款资产起息日基准利率信息，步骤如下：" % BASIC_INFO_SHEET)
        print("-" * 50)
        print("1、确认 %s Sheet页存在 %s 列；" % (BASIC_INFO_SHEET, VALUE_DATE_CURVE))
        print("2、筛选 OTHER 类资产、%s 列为空的单元格；" % BASIC_INFO_SHEET)
        print("3、输入公式：=b_calc_curve_chinabond(曲线ID,品种起息日期,期限)，获取起息日基准利率。")
        print("-" * 50)
        input("输入任意键进入下一环节......")
        print("请在 %s Sheet页补充估值日基准利率信息，步骤如下：" % CASH_FLOW_INFO_SHEET)
        print("-" * 50)
        print("1、确认在 %s Sheet页存在列 %s ；" % (CASH_FLOW_INFO_SHEET, VALUATION_DATE_CURVE))
        print("2、输入公式：=b_calc_curve_chinabond(曲线ID,估值日期,现金流剩余期限) ，获取估值日基准利率。")
        print("-" * 50)
        input("输入任意键进入下一环节......")
    else:
        print("发现临时保存文件 %s ，从临时文件获取基础信息......" % output_file_name)
    # 确认用户是否已补充信息，若校验失败，提示用户再次进行补充
    print("提取补充完整的数据......")
    clean_df, cash_flow_basic_df, cash_flow_info = get_new_info(output_file_full_path)

    info_check_flag = False
    info_check_flag, check_result_str = check_info_integrity(cash_flow_basic_df, cash_flow_info)
    while not info_check_flag:
        print("数据完整性校验失败: %s." % check_result_str)
        print("请参考上述步骤重新补充数据......")
        input("输入任意键，程序开始重新提取并校验数据......")
        print("重新提取数据......")
        clean_df, cash_flow_basic_df, cash_flow_info = get_new_info(output_file_full_path)
        info_check_flag, check_result_str = check_info_integrity(cash_flow_basic_df, cash_flow_info)

    # 计算久期信息
    print("开始拟合收益率曲线......")
    fill_fit_curve(cash_flow_basic_df, cash_flow_info)
    print("计算修正久期......")
    calc_mod_duration(cash_flow_basic_df, cash_flow_info)
    print("计算有效久期......")
    calc_effective_duration(cash_flow_basic_df, cash_flow_info, rp_date_str)
    print("计算关键久期......")
    cash_flow_basic_df = calc_key_duration(cash_flow_basic_df, cash_flow_info)
    # 将估值信息填充至持仓信息中
    print("结合持仓进行汇总......")
    clean_df = update_position_info(clean_df, cash_flow_basic_df)
    # 保存文件
    print("文件输出至：%s " % output_file_full_path)
    save_result(output_file_full_path, clean_df, cash_flow_basic_df, cash_flow_info)
    print("保存成功。")
    input("输入任意键结束......")

    """
    old logic
    """
    # print("请输入计算步骤（1 OR 2): ")
    # print("-" * 60)
    # print("step 1、获取基础数据，生成现金流和IRR信息；")
    # print("step 2、获取手工补充的标准资产基准信息，计算估值和久期信息。")
    # print("-" * 60)
    # step_str = input("> ")
    # if step_str == '1':
    #     file_path = input("请输入基本信息文件路径：> ")
    #     df = fetch_basic_info(file_path)
    #     cf = calc_cash_flow(df)
    #     temp_file = r"D:\work\temp\CASH_FLOW_TEMP.csv"
    #     temp_df_file = r"D:\work\temp\DF_TEMP.csv"
    #     # cf.to_csv(temp_file, index=False)
    #     # df.to_csv(temp_df_file, index=False)
    #     extend_irr_info(df, cf)
    #     extend_valuation_date_base(df)
    #     df_file = input("请输入基本信息保存文件路径：> ")
    #     cf_file = input("请输入现金流信息保存文件路径：> ")
    #     df.to_csv(df_file, index=False)
    #     cf.to_csv(cf_file, index=False)
    #     print("处理完毕。")
    # elif step_str == '2':
    #     df_file = input("请输入基本信息文件路径：> ")
    #     cf_file = input("请输入现金流信息文件路径：> ")
    # #     df_file = r"D:\alm\20170630\all\basic.csv"
    # #     cf_file = r"D:\alm\20170630\all\cashflow.csv"
    #     df = pd.read_csv(df_file, parse_dates=[VALUE_DATE, MATURE_DATE, FIRST_PAY_DATE, NEXT_OPTION_DATE])
    #     cf = pd.read_csv(cf_file, parse_dates=[CASH_FLOW_DATE])
    #     fill_fit_curve(df, cf)
    #     calc_mod_duration(df, cf)
    #     calc_effective_duration(df, cf, VALUATION_DATE_STR)
    #     df = calc_key_duration(df, cf)
    #     df_file = df_file[:-4] + "_done" + df_file[-4:]
    #     cf_file = cf_file[:-4] + "_done" + cf_file[-4:]
    #     cf.to_csv(cf_file, index=False)
    #     df.to_csv(df_file, index=False)
    #     print("处理完毕。")

    w.stop()

