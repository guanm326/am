"""
获取所有必需的数据，并进行清洗
"""
import datetime
import time
import os
import configparser
import pandas as pd
from tools import filetools

cfg = configparser.ConfigParser()
cfg.read("\\\\10.145.39.42\\北京总部文件资料\\资产管理部\\18-其他\\19-软件安装包\\小工具\\config.ini", encoding='UTF-8')
# cfg.read("d:\\config.ini", encoding='UTF-8')
DT_SECTOR = "dt"

SOURCE_FILE_NAME_PREFIX = cfg.get(DT_SECTOR, "SOURCE_FILE_NAME_PREFIX")
SOURCE_FILE_DIR_PREFIX = cfg.get(DT_SECTOR, "SOURCE_FILE_DIR_PREFIX")
RESULT_FILE_NAME_PREFIX = cfg.get(DT_SECTOR, "RESULT_FILE_NAME_PREFIX")
RESULT_FILE_DIR = cfg.get(DT_SECTOR, "RESULT_FILE_DIR")
REAL_TIME_DATA_FILE_NAME = cfg.get(DT_SECTOR, "REAL_TIME_DATA_FILE_NAME")
REAL_TIME_DATA_FILE_DIR = cfg.get(DT_SECTOR, "REAL_TIME_DATA_FILE_DIR")

DROP_NA_THRESH = 10
DAYS_BEFORE = 10

FUND_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "FUND_ASSET_SHEET_NAME")
STOCK_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "STOCK_ASSET_SHEET_NAME")
BOND_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "BOND_ASSET_SHEET_NAME")
DEPOSIT_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "DEPOSIT_ASSET_SHEET_NAME")
NON_STANDARD_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "NON_STANDARD_ASSET_SHEET_NAME")
MONEY_MARKET_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "MONEY_MARKET_ASSET_SHEET_NAME")
TOU_LIAN_ASSET_SHEET_NAME = cfg.get(DT_SECTOR, "TOU_LIAN_ASSET_SHEET_NAME")
ALL_ASSET_DETAIL_SHEET_NAME = cfg.get(DT_SECTOR, "ALL_ASSET_DETAIL_SHEET_NAME")
BASE_DATA_SHEETS = [FUND_ASSET_SHEET_NAME, STOCK_ASSET_SHEET_NAME, BOND_ASSET_SHEET_NAME,
                    DEPOSIT_ASSET_SHEET_NAME, NON_STANDARD_ASSET_SHEET_NAME,
                    MONEY_MARKET_ASSET_SHEET_NAME, TOU_LIAN_ASSET_SHEET_NAME,
                    ALL_ASSET_DETAIL_SHEET_NAME]

RESULT_DATA_SHEET_NAME = cfg.get(DT_SECTOR, "RESULT_DATA_SHEET_NAME")
RESULT_DATA_CIRC_SHEET_NAME = cfg.get(DT_SECTOR, "RESULT_DATA_CIRC_SHEET_NAME")
RESULT_DATA_SAA_TAA_SHEET_NAME = cfg.get(DT_SECTOR, "RESULT_DATA_SAA_TAA_SHEET_NAME")
RESULT_DATA_CTR_SHEET_NAME = cfg.get(DT_SECTOR, "RESULT_DATA_CTR_SHEET_NAME")
RESULT_DATA_SHEETS = [RESULT_DATA_SHEET_NAME]
REAL_TIME_DATA_SHEET_NAME = cfg.get(DT_SECTOR, "REAL_TIME_DATA_SHEET_NAME")
REAL_TIME_DATA_SHEETS = [REAL_TIME_DATA_SHEET_NAME]

ACCOUNT_METHOD_HTM = cfg.get(DT_SECTOR, "ACCOUNT_METHOD_HTM")
ACCOUNT_METHOD_LOAN = cfg.get(DT_SECTOR, "ACCOUNT_METHOD_LOAN")

REVERSE_REPO_FLAG_IN_ALL_ASSET = cfg.get(DT_SECTOR, "REVERSE_REPO_FLAG_IN_ALL_ASSET")
REVERSE_REPO_COLUMN_FIRST_CLASS = cfg.get(DT_SECTOR, "REVERSE_REPO_COLUMN_FIRST_CLASS")
REVERSE_REPO_COLUMN_BOOK_VALUE = cfg.get(DT_SECTOR, "REVERSE_REPO_COLUMN_BOOK_VALUE")

BASE_COLUMN_QUERY_IDENTIFY = cfg.get(DT_SECTOR, "BASE_COLUMN_QUERY_IDENTIFY")
BASE_COLUMN_SUMMARY_IDENTIFY = cfg.get(DT_SECTOR, "BASE_COLUMN_SUMMARY_IDENTIFY")
BASE_COLUMN_ACCOUNT = cfg.get(DT_SECTOR, "BASE_COLUMN_ACCOUNT")
BASE_COLUMN_PRODUCT = cfg.get(DT_SECTOR, "BASE_COLUMN_PRODUCT")
BASE_COLUMN_MANAGER = cfg.get(DT_SECTOR, "BASE_COLUMN_MANAGER")
BASE_COLUMN_ACCOUNTING_METHOD = cfg.get(DT_SECTOR, "BASE_COLUMN_ACCOUNTING_METHOD")
BASE_COLUMN_ASSET_CODE = cfg.get(DT_SECTOR, "BASE_COLUMN_ASSET_CODE")
FUND_COLUMN_ASSET_CODE = cfg.get(DT_SECTOR, "FUND_COLUMN_ASSET_CODE")
STOCK_COLUMN_ASSET_CODE = cfg.get(DT_SECTOR, "STOCK_COLUMN_ASSET_CODE")
BASE_COLUMN_ASSET_NAME = cfg.get(DT_SECTOR, "BASE_COLUMN_ASSET_NAME")
FUND_COLUMN_ASSET_NAME = cfg.get(DT_SECTOR, "FUND_COLUMN_ASSET_NAME")
STOCK_COLUMN_ASSET_NAME = cfg.get(DT_SECTOR, "STOCK_COLUMN_ASSET_NAME")
BOND_COLUMN_ASSET_NAME = cfg.get(DT_SECTOR, "BOND_COLUMN_ASSET_NAME")
DEPOSIT_COLUMN_ASSET_NAME = cfg.get(DT_SECTOR, "DEPOSIT_COLUMN_ASSET_NAME")
NON_STANDARD_COLUMN_ASSET_NAME = cfg.get(DT_SECTOR, "NON_STANDARD_COLUMN_ASSET_NAME")

BASE_COLUMN_FIRST_CLASS = cfg.get(DT_SECTOR, 'BASE_COLUMN_FIRST_CLASS')
TOU_LIAN_COLUMN_FIRST_CLASS = cfg.get(DT_SECTOR, 'TOU_LIAN_COLUMN_FIRST_CLASS')
BASE_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'BASE_COLUMN_SECOND_CLASS')
FUND_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'FUND_COLUMN_SECOND_CLASS')
STOCK_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'STOCK_COLUMN_SECOND_CLASS')
BOND_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'BOND_COLUMN_SECOND_CLASS')
DEPOSIT_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_SECOND_CLASS')
MONEY_MARKET_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'MONEY_MARKET_COLUMN_SECOND_CLASS')
NON_STANDARD_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_SECOND_CLASS')
TOU_LIAN_COLUMN_SECOND_CLASS = cfg.get(DT_SECTOR, 'TOU_LIAN_COLUMN_SECOND_CLASS')
BASE_COLUMN_THIRD_CLASS = cfg.get(DT_SECTOR, 'BASE_COLUMN_THIRD_CLASS')
FUND_COLUMN_THIRD_CLASS = cfg.get(DT_SECTOR, 'FUND_COLUMN_THIRD_CLASS')
NON_STANDARD_COLUMN_THIRD_CLASS = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_THIRD_CLASS')
BASE_COLUMN_CURRENCY = cfg.get(DT_SECTOR, 'BASE_COLUMN_CURRENCY')
BASE_COLUMN_SHARE = cfg.get(DT_SECTOR, 'BASE_COLUMN_SHARE')
BOND_COLUMN_SHARE = cfg.get(DT_SECTOR, 'BOND_COLUMN_SHARE')
DEPOSIT_COLUMN_SHARE = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_SHARE')
NON_STANDARD_COLUMN_SHARE = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_SHARE')
MONEY_MARKET_COLUMN_SHARE = cfg.get(DT_SECTOR, 'MONEY_MARKET_COLUMN_SHARE')
BASE_COLUMN_COST = cfg.get(DT_SECTOR, 'BASE_COLUMN_COST')
BOND_COLUMN_COST = cfg.get(DT_SECTOR, 'BOND_COLUMN_COST')
MONEY_MARKET_COLUMN_COST = cfg.get(DT_SECTOR, 'MONEY_MARKET_COLUMN_COST')
BASE_COLUMN_BOOK_VALUE = cfg.get(DT_SECTOR, 'BASE_COLUMN_BOOK_VALUE')
DEPOSIT_COLUMN_BOOK_VALUE = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_BOOK_VALUE')
NON_STANDARD_COLUMN_BOOK_VALUE = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_BOOK_VALUE')
BOND_COLUMN_BOOK_VALUE_HTM = cfg.get(DT_SECTOR, 'BOND_COLUMN_BOOK_VALUE_HTM')
BOND_COLUMN_BOOK_VALUE_MTM = cfg.get(DT_SECTOR, 'BOND_COLUMN_BOOK_VALUE_MTM')
MONEY_MARKET_COLUMN_BOOK_VALUE = cfg.get(DT_SECTOR, 'MONEY_MARKET_COLUMN_BOOK_VALUE')
TOU_LIAN_COLUMN_BOOK_VALUE = cfg.get(DT_SECTOR, 'TOU_LIAN_COLUMN_BOOK_VALUE')
BASE_COLUMN_MINUS_VALUE = cfg.get(DT_SECTOR, 'BASE_COLUMN_MINUS_VALUE')
BASE_COLUMN_TERM = cfg.get(DT_SECTOR, 'BASE_COLUMN_TERM')
BASE_COLUMN_TERM_FLOAT = cfg.get(DT_SECTOR, 'BASE_COLUMN_TERM_FLOAT')
BOND_COLUMN_TERM = cfg.get(DT_SECTOR, 'BOND_COLUMN_TERM')
BASE_COLUMN_ASSET_RATING = cfg.get(DT_SECTOR, 'BASE_COLUMN_ASSET_RATING')
BOND_COLUMN_ASSET_RATING = cfg.get(DT_SECTOR, 'BOND_COLUMN_ASSET_RATING')
DEPOSIT_COLUMN_ASSET_RATING = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_ASSET_RATING')
NON_STANDARD_COLUMN_ASSET_RATING = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_ASSET_RATING')
BASE_COLUMN_SUBJECT_RATING = cfg.get(DT_SECTOR, 'BASE_COLUMN_SUBJECT_RATING')
BOND_COLUMN_SUBJECT_RATING = cfg.get(DT_SECTOR, 'BOND_COLUMN_SUBJECT_RATING')
NON_STANDARD_COLUMN_SUBJECT_RATING = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_SUBJECT_RATING')
BASE_COLUMN_GUARANTOR = cfg.get(DT_SECTOR, 'BASE_COLUMN_GUARANTOR')
NON_STANDARD_COLUMN_GUARANTOR = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_GUARANTOR')
BOND_COLUMN_GUARANTOR = cfg.get(DT_SECTOR, 'BOND_COLUMN_GUARANTOR')
BASE_COLUMN_FINANCIERS = cfg.get(DT_SECTOR, 'BASE_COLUMN_FINANCIERS')
FUND_COLUMN_FINANCIERS = cfg.get(DT_SECTOR, 'FUND_COLUMN_FINANCIERS')
STOCK_COLUMN_FINANCIERS = cfg.get(DT_SECTOR, 'STOCK_COLUMN_FINANCIERS')
BOND_COLUMN_FINANCIERS = cfg.get(DT_SECTOR, 'BOND_COLUMN_FINANCIERS')
DEPOSIT_COLUMN_FINANCIERS = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_FINANCIERS')
NON_STANDARD_COLUMN_FINANCIERS = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_FINANCIERS')
BASE_COLUMN_COUNTER_PARTY = cfg.get(DT_SECTOR, 'BASE_COLUMN_COUNTER_PARTY')
BASE_COLUMN_COUNTER_PARTY_RANK = cfg.get(DT_SECTOR, 'BASE_COLUMN_COUNTER_PARTY_RANK')
DEPOSIT_COLUMN_COUNTER_PARTY = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_COUNTER_PARTY')
DEPOSIT_COLUMN_COUNTER_PARTY_RANK = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_COUNTER_PARTY_RANK')
BOND_COLUMN_COUNTER_PARTY = cfg.get(DT_SECTOR, 'BOND_COLUMN_COUNTER_PARTY')
BOND_COLUMN_COUNTER_PARTY_RANK = cfg.get(DT_SECTOR, 'BOND_COLUMN_COUNTER_PARTY_RANK')
NON_STANDARD_COLUMN_COUNTER_PARTY = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_COUNTER_PARTY')
NON_STANDARD_COLUMN_COUNTER_PARTY_RANK = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_COUNTER_PARTY_RANK')
BASE_COLUMN_CIRC_INDUSTRY_FIRST = cfg.get(DT_SECTOR, 'BASE_COLUMN_CIRC_INDUSTRY_FIRST')
STOCK_COLUMN_CIRC_INDUSTRY_FIRST = cfg.get(DT_SECTOR, 'STOCK_COLUMN_CIRC_INDUSTRY_FIRST')
BOND_COLUMN_CIRC_INDUSTRY_FIRST = cfg.get(DT_SECTOR, 'BOND_COLUMN_CIRC_INDUSTRY_FIRST')
DEPOSIT_COLUMN_CIRC_INDUSTRY_FIRST = cfg.get(DT_SECTOR, 'DEPOSIT_COLUMN_CIRC_INDUSTRY_FIRST')
NON_STANDARD_COLUMN_CIRC_INDUSTRY_FIRST = cfg.get(DT_SECTOR, 'NON_STANDARD_COLUMN_CIRC_INDUSTRY_FIRST')

FIRST_CLASS_FUND = cfg.get(DT_SECTOR, 'FIRST_CLASS_FUND')
FIRST_CLASS_STOCK = cfg.get(DT_SECTOR, 'FIRST_CLASS_STOCK')
FIRST_CLASS_BOND = cfg.get(DT_SECTOR, 'FIRST_CLASS_BOND')
FIRST_CLASS_DEPOSIT = cfg.get(DT_SECTOR, 'FIRST_CLASS_DEPOSIT')
FIRST_CLASS_NON_STANDARD = cfg.get(DT_SECTOR, 'FIRST_CLASS_NON_STANDARD')
FIRST_CLASS_MM = cfg.get(DT_SECTOR, 'FIRST_CLASS_MM')

ASSET_DETAIL_FIELDS = [BASE_COLUMN_QUERY_IDENTIFY, BASE_COLUMN_SUMMARY_IDENTIFY, BASE_COLUMN_ACCOUNT,
                       BASE_COLUMN_PRODUCT, BASE_COLUMN_MANAGER, BASE_COLUMN_ACCOUNTING_METHOD,
                       BASE_COLUMN_ASSET_CODE, BASE_COLUMN_ASSET_NAME, BASE_COLUMN_FIRST_CLASS,
                       BASE_COLUMN_SECOND_CLASS, BASE_COLUMN_THIRD_CLASS, BASE_COLUMN_CURRENCY,
                       BASE_COLUMN_SHARE, BASE_COLUMN_COST, BASE_COLUMN_BOOK_VALUE,
                       BASE_COLUMN_MINUS_VALUE, BASE_COLUMN_TERM, BASE_COLUMN_ASSET_RATING,
                       BASE_COLUMN_SUBJECT_RATING, BASE_COLUMN_GUARANTOR, BASE_COLUMN_FINANCIERS,
                       BASE_COLUMN_COUNTER_PARTY, BASE_COLUMN_COUNTER_PARTY_RANK, BASE_COLUMN_CIRC_INDUSTRY_FIRST]

SHEET_NAME_STR = "sheet_name"
SHEET_DATA_STR = "sheet_data"
SHEET_FIELDS_STR = "fields"

NUMBER_MAP = {
    RESULT_DATA_SHEET_NAME:
        {
            'M': '0.00_);[Red]\(0.00\)',
            'N': '0.00_);[Red]\(0.00\)',
            'O': '0.00_);[Red]\(0.00\)',
            'P': '0.00_);[Red]\(0.00\)',
            'Q': '0.00_);[Red]\(0.00\)'
        }
    ,
    RESULT_DATA_CIRC_SHEET_NAME:
        {
            'B': '0.00_);[Red]\(0.00\)',
            'C': '0.00_);[Red]\(0.00\)',
            'D': '0.00%',
            'E': '0.00%',
            'F': '0.00%'
        }
    ,
    RESULT_DATA_SAA_TAA_SHEET_NAME:
        {
            'B': '0.00%',
            'C': '0.00%',
            'D': '0.00%',
            'E': '0.00_);[Red]\(0.00\)',
            'F': '0.00_);[Red]\(0.00\)',
            'G': '0.00%',
            'I': '0.00%'
        }
}

COLUMN_WIDTH_MAP = {
    RESULT_DATA_SHEET_NAME:
        {
            'A': 0,
            'B': 0,
            'C': 7,
            'D': 5,
            'E': 9,
            'F': 10,
            'G': 13,
            'H': 20,
            'I': 8,
            'J': 10,
            'K': 8,
            'L': 5,
            'M': 15,
            'N': 15,
            'O': 15,
            'P': 12,
            'Q': 8
        },
    RESULT_DATA_CIRC_SHEET_NAME:
        {
            'A': 33,
            'B': 15,
            'C': 16,
            'D': 15,
            'E': 15,
            'F': 9,
            'G': 13,
            'H': 26
        },
    RESULT_DATA_SAA_TAA_SHEET_NAME:
        {
            'A': 12,
            'B': 14,
            'C': 14,
            'D': 9,
            'E': 16,
            'F': 16,
            'G': 9,
            'H': 13
        }
}

"""
获取文件名称全路径。
"""


def guess_file_full_name(rp_date=None):
    if not rp_date:
        today = datetime.date.today()
        # 获取最新有数据的日期
        rp_date = today - datetime.timedelta(days=DAYS_BEFORE)
    file_dir = SOURCE_FILE_DIR_PREFIX + '\\' + str(rp_date.year) + "." + str(rp_date.month) + '\\'
    file_name = SOURCE_FILE_NAME_PREFIX + '（' + rp_date.strftime("%Y.%m.%d") + "）.xlsm"
    file_full_name = str(file_dir) + str(file_name)
    # print(file_full_name)
    return file_full_name


"""
基金数据清洗
"""


def fund_asset_data_clean(fund_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = fund_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = fund_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = fund_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = fund_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = fund_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = fund_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = fund_data[FUND_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = fund_data[FUND_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_SECOND_CLASS] = fund_data[FUND_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_THIRD_CLASS] = fund_data[FUND_COLUMN_THIRD_CLASS]
    clean_data[BASE_COLUMN_SHARE] = fund_data[BASE_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = fund_data[BASE_COLUMN_COST]
    clean_data[BASE_COLUMN_BOOK_VALUE] = fund_data[BASE_COLUMN_BOOK_VALUE]
    clean_data[BASE_COLUMN_MINUS_VALUE] = fund_data[BASE_COLUMN_MINUS_VALUE]
    clean_data[BASE_COLUMN_FINANCIERS] = fund_data[FUND_COLUMN_FINANCIERS]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data[BASE_COLUMN_FIRST_CLASS] = FIRST_CLASS_FUND
    clean_data[BASE_COLUMN_CURRENCY] = 'CNY'

    return clean_data


"""
股票数据清洗
"""


def stock_asset_data_clean(stock_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = stock_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = stock_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = stock_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = stock_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = stock_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = stock_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = stock_data[STOCK_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = stock_data[STOCK_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_SECOND_CLASS] = stock_data[STOCK_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_SHARE] = stock_data[BASE_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = stock_data[BASE_COLUMN_COST]
    clean_data[BASE_COLUMN_BOOK_VALUE] = stock_data[BASE_COLUMN_BOOK_VALUE]
    clean_data[BASE_COLUMN_MINUS_VALUE] = stock_data[BASE_COLUMN_MINUS_VALUE]
    clean_data[BASE_COLUMN_FINANCIERS] = stock_data[STOCK_COLUMN_FINANCIERS]
    clean_data[BASE_COLUMN_CIRC_INDUSTRY_FIRST] = stock_data[STOCK_COLUMN_CIRC_INDUSTRY_FIRST]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data[BASE_COLUMN_FIRST_CLASS] = FIRST_CLASS_STOCK
    clean_data[BASE_COLUMN_CURRENCY] = 'CNY'
    clean_data[BASE_COLUMN_THIRD_CLASS] = ""

    return clean_data


"""
债券数据清洗
"""


def judge_bond_value(account_method, htm_value, mtm_value):
    if account_method == ACCOUNT_METHOD_HTM or account_method == ACCOUNT_METHOD_LOAN:
        return htm_value
    else:
        return mtm_value


def bond_asset_data_clean(bond_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = bond_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = bond_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = bond_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = bond_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = bond_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = bond_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = bond_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = bond_data[BOND_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_SECOND_CLASS] = bond_data[BOND_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_SHARE] = bond_data[BOND_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = bond_data[BOND_COLUMN_COST]
    clean_data[BASE_COLUMN_BOOK_VALUE] = list(map(lambda x, y, z: judge_bond_value(x, y, z),
                                                  bond_data[BASE_COLUMN_ACCOUNTING_METHOD],
                                                  bond_data[BOND_COLUMN_BOOK_VALUE_HTM],
                                                  bond_data[BOND_COLUMN_BOOK_VALUE_MTM]
                                                  )
                                              )
    clean_data[BASE_COLUMN_MINUS_VALUE] = bond_data[BASE_COLUMN_MINUS_VALUE]
    clean_data[BASE_COLUMN_TERM] = bond_data[BOND_COLUMN_TERM]
    clean_data[BASE_COLUMN_ASSET_RATING] = bond_data[BOND_COLUMN_ASSET_RATING]
    clean_data[BASE_COLUMN_SUBJECT_RATING] = bond_data[BOND_COLUMN_SUBJECT_RATING]
    clean_data[BASE_COLUMN_GUARANTOR] = bond_data[BOND_COLUMN_GUARANTOR]
    clean_data[BASE_COLUMN_FINANCIERS] = bond_data[BOND_COLUMN_FINANCIERS]
    clean_data[BASE_COLUMN_COUNTER_PARTY] = bond_data[BOND_COLUMN_COUNTER_PARTY]
    clean_data[BASE_COLUMN_COUNTER_PARTY_RANK] = bond_data[BOND_COLUMN_COUNTER_PARTY_RANK]
    clean_data[BASE_COLUMN_CIRC_INDUSTRY_FIRST] = bond_data[BOND_COLUMN_CIRC_INDUSTRY_FIRST]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data[BASE_COLUMN_FIRST_CLASS] = FIRST_CLASS_BOND
    clean_data[BASE_COLUMN_CURRENCY] = 'CNY'
    clean_data[BASE_COLUMN_THIRD_CLASS] = ""

    return clean_data


"""
存款数据清洗
"""


def deposit_asset_data_clean(deposit_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = deposit_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = deposit_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = deposit_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = deposit_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = deposit_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = deposit_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = deposit_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = deposit_data[DEPOSIT_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_SECOND_CLASS] = deposit_data[DEPOSIT_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_CURRENCY] = deposit_data[BASE_COLUMN_CURRENCY]
    clean_data[BASE_COLUMN_SHARE] = deposit_data[DEPOSIT_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = deposit_data[DEPOSIT_COLUMN_SHARE]
    clean_data[BASE_COLUMN_BOOK_VALUE] = deposit_data[DEPOSIT_COLUMN_BOOK_VALUE]
    clean_data[BASE_COLUMN_MINUS_VALUE] = deposit_data[BASE_COLUMN_MINUS_VALUE]
    clean_data[BASE_COLUMN_TERM] = deposit_data[BASE_COLUMN_TERM]
    clean_data[BASE_COLUMN_ASSET_RATING] = deposit_data[DEPOSIT_COLUMN_ASSET_RATING]
    clean_data[BASE_COLUMN_FINANCIERS] = deposit_data[DEPOSIT_COLUMN_FINANCIERS]
    clean_data[BASE_COLUMN_COUNTER_PARTY] = deposit_data[DEPOSIT_COLUMN_COUNTER_PARTY]
    clean_data[BASE_COLUMN_COUNTER_PARTY_RANK] = deposit_data[DEPOSIT_COLUMN_COUNTER_PARTY_RANK]
    # clean_data[BASE_COLUMN_CIRC_INDUSTRY_FIRST] = deposit_data[DEPOSIT_COLUMN_CIRC_INDUSTRY_FIRST]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data[BASE_COLUMN_FIRST_CLASS] = FIRST_CLASS_DEPOSIT
    clean_data[BASE_COLUMN_THIRD_CLASS] = ""

    return clean_data


"""
另类数据清洗
"""


def non_standard_asset_data_clean(non_standard_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = non_standard_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = non_standard_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = non_standard_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = non_standard_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = non_standard_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = non_standard_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = non_standard_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = non_standard_data[NON_STANDARD_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_SECOND_CLASS] = non_standard_data[NON_STANDARD_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_THIRD_CLASS] = non_standard_data[NON_STANDARD_COLUMN_THIRD_CLASS]
    clean_data[BASE_COLUMN_SHARE] = non_standard_data[NON_STANDARD_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = non_standard_data[NON_STANDARD_COLUMN_SHARE]
    clean_data[BASE_COLUMN_BOOK_VALUE] = non_standard_data[NON_STANDARD_COLUMN_BOOK_VALUE]
    clean_data[BASE_COLUMN_MINUS_VALUE] = non_standard_data[BASE_COLUMN_MINUS_VALUE]
    clean_data[BASE_COLUMN_TERM] = non_standard_data[BASE_COLUMN_TERM]
    clean_data[BASE_COLUMN_ASSET_RATING] = non_standard_data[NON_STANDARD_COLUMN_ASSET_RATING]
    clean_data[BASE_COLUMN_SUBJECT_RATING] = non_standard_data[NON_STANDARD_COLUMN_SUBJECT_RATING]
    clean_data[BASE_COLUMN_GUARANTOR] = non_standard_data[NON_STANDARD_COLUMN_GUARANTOR]
    clean_data[BASE_COLUMN_FINANCIERS] = non_standard_data[NON_STANDARD_COLUMN_FINANCIERS]
    clean_data[BASE_COLUMN_COUNTER_PARTY] = non_standard_data[NON_STANDARD_COLUMN_COUNTER_PARTY]
    clean_data[BASE_COLUMN_COUNTER_PARTY_RANK] = non_standard_data[NON_STANDARD_COLUMN_COUNTER_PARTY_RANK]
    clean_data[BASE_COLUMN_CIRC_INDUSTRY_FIRST] = non_standard_data[NON_STANDARD_COLUMN_CIRC_INDUSTRY_FIRST]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data[BASE_COLUMN_FIRST_CLASS] = FIRST_CLASS_NON_STANDARD
    clean_data[BASE_COLUMN_CURRENCY] = 'CNY'

    return clean_data


"""
货币市场数据清洗
"""


def money_market_asset_data_clean(money_market_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = money_market_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = money_market_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = money_market_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = money_market_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = money_market_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ASSET_CODE] = money_market_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = money_market_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_SECOND_CLASS] = money_market_data[MONEY_MARKET_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_SHARE] = money_market_data[MONEY_MARKET_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = money_market_data[MONEY_MARKET_COLUMN_COST]
    clean_data[BASE_COLUMN_BOOK_VALUE] = money_market_data[MONEY_MARKET_COLUMN_BOOK_VALUE]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data = clean_data[clean_data[BASE_COLUMN_ASSET_CODE] != ""]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = "交易类"
    clean_data[BASE_COLUMN_FIRST_CLASS] = FIRST_CLASS_MM
    clean_data[BASE_COLUMN_CURRENCY] = 'CNY'
    clean_data[BASE_COLUMN_THIRD_CLASS] = ""
    clean_data[BASE_COLUMN_MINUS_VALUE] = ""

    return clean_data


"""
投连数据清洗
"""


def tou_lian_asset_data_clean(tou_lian_data):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = tou_lian_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = tou_lian_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = tou_lian_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = tou_lian_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = tou_lian_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = tou_lian_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = tou_lian_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = tou_lian_data[BASE_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_FIRST_CLASS] = tou_lian_data[TOU_LIAN_COLUMN_FIRST_CLASS]
    clean_data[BASE_COLUMN_SECOND_CLASS] = tou_lian_data[TOU_LIAN_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_THIRD_CLASS] = tou_lian_data[BASE_COLUMN_THIRD_CLASS]
    clean_data[BASE_COLUMN_SHARE] = tou_lian_data[BASE_COLUMN_SHARE]
    clean_data[BASE_COLUMN_COST] = tou_lian_data[BASE_COLUMN_COST]
    clean_data[BASE_COLUMN_BOOK_VALUE] = tou_lian_data[TOU_LIAN_COLUMN_BOOK_VALUE]
    clean_data[BASE_COLUMN_MINUS_VALUE] = tou_lian_data[BASE_COLUMN_MINUS_VALUE]

    clean_data = clean_data[clean_data[BASE_COLUMN_SHARE] != ""]
    clean_data[BASE_COLUMN_CURRENCY] = 'CNY'

    return clean_data


"""
从汇总数据中获取指定数据，并进行清洗
"""


def show_me_the_money(all_asset_data, kind_of_money):
    clean_data = pd.DataFrame()
    clean_data[BASE_COLUMN_QUERY_IDENTIFY] = all_asset_data[BASE_COLUMN_QUERY_IDENTIFY]
    clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] = all_asset_data[BASE_COLUMN_SUMMARY_IDENTIFY]
    clean_data[BASE_COLUMN_ACCOUNT] = all_asset_data[BASE_COLUMN_ACCOUNT]
    clean_data[BASE_COLUMN_PRODUCT] = all_asset_data[BASE_COLUMN_PRODUCT]
    clean_data[BASE_COLUMN_MANAGER] = all_asset_data[BASE_COLUMN_MANAGER]
    clean_data[BASE_COLUMN_ACCOUNTING_METHOD] = all_asset_data[BASE_COLUMN_ACCOUNTING_METHOD]
    clean_data[BASE_COLUMN_ASSET_CODE] = all_asset_data[BASE_COLUMN_ASSET_CODE]
    clean_data[BASE_COLUMN_ASSET_NAME] = all_asset_data[BASE_COLUMN_ASSET_NAME]
    clean_data[BASE_COLUMN_FIRST_CLASS] = all_asset_data[REVERSE_REPO_COLUMN_FIRST_CLASS]
    clean_data[BASE_COLUMN_SECOND_CLASS] = all_asset_data[BASE_COLUMN_SECOND_CLASS]
    clean_data[BASE_COLUMN_THIRD_CLASS] = all_asset_data[BASE_COLUMN_THIRD_CLASS]
    clean_data[BASE_COLUMN_CURRENCY] = all_asset_data[BASE_COLUMN_CURRENCY]
    clean_data[BASE_COLUMN_SHARE] = all_asset_data[BASE_COLUMN_COST]
    clean_data[BASE_COLUMN_COST] = all_asset_data[BASE_COLUMN_COST]
    clean_data[BASE_COLUMN_BOOK_VALUE] = all_asset_data[REVERSE_REPO_COLUMN_BOOK_VALUE]
    clean_data[BASE_COLUMN_MINUS_VALUE] = all_asset_data[BASE_COLUMN_MINUS_VALUE]

    clean_data = clean_data[(clean_data[BASE_COLUMN_SHARE] != "")
                            & (clean_data[BASE_COLUMN_SUMMARY_IDENTIFY] == kind_of_money)]

    return clean_data


def what_is_the_org_result_file_name(rp_date):
    return RESULT_FILE_NAME_PREFIX + rp_date.strftime("%Y%m%d") + ".xlsx"


def what_is_the_new_result_file_name(rp_date):
    return RESULT_FILE_NAME_PREFIX + rp_date.strftime("%Y%m%d") + "-" + time.strftime("%H%M%S") + ".xlsx"


def what_is_the_org_result_file_full_name(rp_date):
    return RESULT_FILE_DIR + rp_date.strftime("%Y%m%d") + "\\" + \
           RESULT_FILE_NAME_PREFIX + rp_date.strftime("%Y%m%d") + ".xlsx"


def save_asset_data(file_name, file_path, asset_data_df, sheet_name, fields=ASSET_DETAIL_FIELDS):
    # output to the new file
    result_data = [
        {
            SHEET_NAME_STR: sheet_name,
            SHEET_DATA_STR: asset_data_df.loc[:, fields].values.tolist(),
            SHEET_FIELDS_STR: fields
        }
    ]
    filetools.save_data_to_workbook(result_data, file_name, file_path)
    if NUMBER_MAP.get(sheet_name):
        filetools.apply_number_format(file_name, file_path, sheet_name, NUMBER_MAP.get(sheet_name))
    if COLUMN_WIDTH_MAP.get(sheet_name):
        filetools.apply_column_width(file_name, file_path, sheet_name, COLUMN_WIDTH_MAP.get(sheet_name))


def save_multiple_asset_data(rp_date, asset_data):
    # 判断当日原始数据文件是否已经生成
    if not os.path.exists(RESULT_FILE_DIR):
        os.mkdir(RESULT_FILE_DIR)
    if not rp_date:
        rp_date = datetime.date.today()
    org_file_full_name = what_is_the_org_result_file_full_name(rp_date)
    if os.path.exists(org_file_full_name):
        file_name = what_is_the_new_result_file_name(rp_date)
        file_path = RESULT_FILE_DIR + rp_date.strftime("%Y%m%d") + "\\"
    else:
        file_name = what_is_the_org_result_file_name(rp_date)
        file_path = RESULT_FILE_DIR + rp_date.strftime("%Y%m%d") + "\\"
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    filetools.create_workbook(file_name, file_path)

    for data in asset_data:
        save_asset_data(file_name, file_path, data.get(SHEET_DATA_STR), data.get(SHEET_NAME_STR),
                        data.get(SHEET_FIELDS_STR))

    print("check result file saved at：%s" % file_path + file_name)


"""
获取所有资产的基本数据信息：

"""


def org_data_bowl(rp_date):
    file_full_name = guess_file_full_name(rp_date)
    print("copy data from：%s" % file_full_name)
    trade_data = filetools.read_workbook(file_full_name, "", BASE_DATA_SHEETS)

    # 基金持仓处理
    fund_asset_data = filetools.data_clean_in_one_sheet(trade_data, FUND_ASSET_SHEET_NAME, row_start_num=2,
                                                        field_row_num=1, axis_one_drop_na_flag=False,
                                                        axis_zero_drop_na_flag=False)
    fund_asset_data_after_clean = fund_asset_data_clean(fund_asset_data)

    # 股票持仓处理
    stock_asset_data = filetools.data_clean_in_one_sheet(trade_data, STOCK_ASSET_SHEET_NAME, row_start_num=2,
                                                         field_row_num=1, axis_one_drop_na_flag=False,
                                                         axis_zero_drop_na_flag=False)
    stock_asset_data_after_clean = stock_asset_data_clean(stock_asset_data)

    # 债券持仓处理
    bond_asset_data = filetools.data_clean_in_one_sheet(trade_data, BOND_ASSET_SHEET_NAME, row_start_num=2,
                                                        field_row_num=1, axis_one_drop_na_flag=False,
                                                        axis_zero_drop_na_flag=False)
    bond_asset_data_after_clean = bond_asset_data_clean(bond_asset_data)

    # 存款持仓处理
    deposit_asset_data = filetools.data_clean_in_one_sheet(trade_data, DEPOSIT_ASSET_SHEET_NAME, row_start_num=2,
                                                           field_row_num=1, axis_one_drop_na_flag=False,
                                                           axis_zero_drop_na_flag=False)
    deposit_asset_data_after_clean = deposit_asset_data_clean(deposit_asset_data)

    # 另类持仓处理
    non_standard_asset_data = filetools.data_clean_in_one_sheet(trade_data, NON_STANDARD_ASSET_SHEET_NAME,
                                                                row_start_num=2,
                                                                field_row_num=1, axis_one_drop_na_flag=False,
                                                                axis_zero_drop_na_flag=False)
    non_standard_asset_data_after_clean = non_standard_asset_data_clean(non_standard_asset_data)

    # 货币市场持仓处理
    money_market_asset_data = filetools.data_clean_in_one_sheet(trade_data, MONEY_MARKET_ASSET_SHEET_NAME,
                                                                row_start_num=2,
                                                                field_row_num=1, axis_one_drop_na_flag=False,
                                                                axis_zero_drop_na_flag=False)
    money_market_asset_data_after_clean = money_market_asset_data_clean(money_market_asset_data)

    # 逆回购资产获取，TODO 由于货币市场中未包含回购，故从全资产明细中获取
    all_asset_data = filetools.data_clean_in_one_sheet(trade_data, ALL_ASSET_DETAIL_SHEET_NAME,
                                                       row_start_num=2,
                                                       field_row_num=1, axis_one_drop_na_flag=False,
                                                       axis_zero_drop_na_flag=False)
    reverse_repo_from_all_asset_after_clean = show_me_the_money(all_asset_data, REVERSE_REPO_FLAG_IN_ALL_ASSET)

    # 投连持仓处理 TODO 剔除投连资产
    # tou_lian_asset_data = filetools.data_clean_in_one_sheet(trade_data, TOU_LIAN_ASSET_SHEET_NAME,
    #                                                         row_start_num=2,
    #                                                         field_row_num=1, axis_one_drop_na_flag=False,
    #                                                         axis_zero_drop_na_flag=False)
    # tou_lian_asset_data_after_clean = tou_lian_asset_data_clean(tou_lian_asset_data)

    all_clean_asset_data = pd.concat([fund_asset_data_after_clean, stock_asset_data_after_clean,
                                      bond_asset_data_after_clean, deposit_asset_data_after_clean,
                                      non_standard_asset_data_after_clean, money_market_asset_data_after_clean,
                                      reverse_repo_from_all_asset_after_clean])

    return all_clean_asset_data


def data_bowl_char_convert(org_data):
    # 字符转换成数字
    org_data[BASE_COLUMN_TERM] = org_data[BASE_COLUMN_TERM].apply(
        lambda x: float(x) if x else None)
    org_data[BASE_COLUMN_SHARE] = org_data[BASE_COLUMN_SHARE].apply(
        lambda x: float(x) if x else None
    )
    org_data[BASE_COLUMN_COST] = org_data[BASE_COLUMN_COST].apply(
        lambda x: float(x) if x else None
    )
    org_data[BASE_COLUMN_BOOK_VALUE] = org_data[BASE_COLUMN_BOOK_VALUE].apply(
        lambda x: float(x) if x else None
    )
    org_data[BASE_COLUMN_MINUS_VALUE] = org_data[BASE_COLUMN_MINUS_VALUE].apply(
        lambda x: float(x) if x else None
    )
    return org_data


def result_data_bowl(file_full_name):
    result_data = filetools.read_workbook(file_full_name, "", RESULT_DATA_SHEETS)
    asset_detail_data = filetools.data_clean_in_one_sheet(result_data, RESULT_DATA_SHEET_NAME, row_start_num=1,
                                                          field_row_num=0, axis_one_drop_na_flag=False,
                                                          axis_zero_drop_na_flag=False)
    asset_detail_data = asset_detail_data[asset_detail_data[BASE_COLUMN_ASSET_CODE] != ""]
    return asset_detail_data


def real_time_data_bowl(file_full_name):
    result_data = filetools.read_workbook(file_full_name, "", REAL_TIME_DATA_SHEETS)
    asset_detail_data = filetools.data_clean_in_one_sheet(result_data, REAL_TIME_DATA_SHEET_NAME, row_start_num=1,
                                                          field_row_num=0, axis_one_drop_na_flag=False,
                                                          axis_zero_drop_na_flag=False)
    asset_detail_data = asset_detail_data[asset_detail_data[BASE_COLUMN_ASSET_NAME] != ""]
    return asset_detail_data


def data_bowl(rp_date):
    # 判断当日数据是否已生成，若已生成直接从结果文件读取数据
    result_file_full_name = what_is_the_org_result_file_full_name(rp_date)
    exists_flag = os.path.exists(result_file_full_name)
    if exists_flag:
        print("当前日期 %s 的数据已生成，路径为 %s"
              % (rp_date.strftime("%Y%m%d"), result_file_full_name))
        all_clean_asset_data = result_data_bowl(result_file_full_name)
    else:
        all_clean_asset_data = org_data_bowl(rp_date)

    if exists_flag:
        # 获取实时数据
        real_time_asset_data = real_time_data_bowl(REAL_TIME_DATA_FILE_DIR + REAL_TIME_DATA_FILE_NAME)
        all_data = pd.concat([all_clean_asset_data, real_time_asset_data])
    else:
        all_data = all_clean_asset_data

    all_data = data_bowl_char_convert(all_data)
    return all_data
