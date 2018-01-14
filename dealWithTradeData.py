"""
按照一定的转换规则，处理原始交易数据
处理后的文件包括：原始交易数据、处理后交易数据、基金交易、股票交易、回购交易
"""
import pandas as pd
from WindPy import *
from tools import filetools


# 原始数据文件路径及sheet页
org_file_name = "可穿透资管产品-交易流水处理表-公式版.xlsm"
org_file_path = "D:/work/小程序/13-投资组合报表/最新模板/大表数据/9月/"
org_data_sheet_name = "原始交易数据"
org_data_sheets = [org_data_sheet_name]

# 处理后文件名称路径及sheet页名称
result_file_name = "处理后交易数据.xlsx"
result_file_path = "D:/"
result_all_data_sheet_name = "处理后交易数据"
result_fund_data_sheet_name = "基金交易"
result_stock_data_sheet_name = "股票交易"
result_repo_data_sheet_name = "回购交易"

# 处理后文件列名
columns = ['综合查询标识', '交易日期', '产品名称', '交易所', '证券类别']

# 证券类别转换映射
alter_ast_name_list = ['中行优2']
alter_ast_code_list = ['ZBTZJJ Y']
org_alt_type_key_words = ['债券计划']
alter_ast_type = '另类'
org_bond_type_key_words = ['债券', '债', '融资券', '票据', '存单']
bond_type = '债券'
org_deposit_type_key_words = ['银行存款']
deposit_type = '存款'
org_stock_type_key_words = ['普通股']
stock_type = '股票'
org_repo_type_key_words = ['回购']
repo_type = '回购'
org_fund_type_key_words = ['基金', '开基', '保险投资产品']
fund_type = '基金'
unknown_type = '未知'

sh_exchange_name_list = ['中行优2']
other_exchange_name_list = ['高华证券次级债务']
sh_exchange = '上交所'
sz_exchange = '深交所'
bank_exchange = '银行间'
otc = '场外'
other_exchange = '其他'

reverse_repo_trade_directions = ['逆回购', '银行间逆回购', '银行间逆回购购回', '质押融券购回']
reverse_repo_ctg = '买入返售类'
reverse_repo_name = '逆回购'
positive_repo_trade_directions = ['正回购', '银行间正回购', '银行间正回购购回', '质押融资购回']
positive_repo_ctg = '卖出回购类'
positive_repo_name = '正回购'
hold_until_expiration_ctg = '持有到期类'
loans_ctg = '贷款类'
trade_ctg = '交易类'
available_for_sale_ctg = '可供出售类'
ctg_map = {
    '持有到期投资': hold_until_expiration_ctg,
    '贷款应收款': loans_ctg,
    '交易性金融资产/公允价值': trade_ctg,
    '可供出售金融资产': available_for_sale_ctg,
    '可出售性金融资产': available_for_sale_ctg
}

# 证券代码映射
code_map = {
    otc: '.OF',
    sh_exchange: '.SH',
    sz_exchange: '.SZ',
    bank_exchange: '.IB'
}

# 交易方向映射
dir_map = {
    '存款付息': '利息兑付',
    '存款支取': '存款到期',
    '股息到帐': '现金分红',
    '红股到帐': '份额分红',
    '基金申购': '买入执行',
    '基金申购确认复核': '买入确认',
    '基金赎回到账复核': '卖出到账',
    '基金赎回确认复核': '卖出确认',
    '基金转换强制调减复核': '强制调减',
    '基金转换强制调增复核': '强制调增',
    '逆回购': '融券回购',
    '万份收益结转': '份额分红',
    '万份收益现金分红': '现金分红',
    '债权计划兑付': '本金兑付',
    '债权计划兑息到账': '利息兑付',
    '债权计划付款': '买入',
    '债券兑付': '到期兑付',
    '债券兑息到帐': '利息兑付',
    '债券买入': '买入',
    '债券卖出': '卖出',
    '正回购': '融资回购',
    '证券买入': '场内买入',
    '证券卖出': '场内卖出',
    '质押融券购回': '融券购回',
    '质押融资购回': '融资购回',
    '银行间逆回购': '融券回购',
    '银行间逆回购购回': '融券购回',
    '银行间正回购': '融资回购',
    '银行间正回购购回': '融资购回',
    '基金认购': '买入执行',
    '基金认购确认复核': '买入确认',
    '网下申购扣款': '申购冻结',
    '债券偿还': '提前还本',
    '网下返款': '申购解冻',
    '网下中签': '申购中签',
    '基金场内赎回成交': '卖出',
    '拆分拆大': '份额分红',
    '份额入账': '买入确认',
    '沪基金实时赎回': '赎回到账',
    '基金预分红': '预分红',
    '红利': '现金分红',
    '基金红利再投': '份额分红',
    '基金场内赎回成交确认': '卖出确认',
    '基金场内赎回款到账': '卖出到账',
    '债券回售': '债券回售登记',
    '债券回售确认': '债券回售',
    '存入': '存入',
    '基金预红利再投': '份额分红',
    '理财产品认购确认': '买入',
    '理财产品认购确认复核': '买入确认',
    '理财产品认购': '认购',
    '付息': '利息兑付',
    '赎回': '卖出确认',
    '申购': '买入',
    '新股中签': '申购中签',
    '理财产品红利': '利息兑付',
    '分销买入': '买入',
    '理财产品申购确认': '买入执行',
    '理财产品申购确认复核': '买入确认',
    '股息到账': '现金分红',
    '红股到账': '份额分红',
    '理财产品赎回确认': '卖出确认',
    '理财产品赎回到账': '卖出到账',
    '基金转出确认': '强制调减',
    '基金转入确认': '强制调增'
}

share_calc_map = {
    '存款到期': -1,
    '现金分红': -1,
    '本金兑付': -1,
    '到期兑付': -1,
    '场内买入': 1,
    '场内卖出': -1,
    '融券回购': 1,
    '融券购回': -1,
    '融资回购': -1,
    '融资购回': 1,
    '申购冻结': 0,
    '提前还本': -1,
    '申购解冻': 0,
    '卖出': -1,
    '赎回到账': -1,
    '预分红': -1,
    '份额分红': 1,
    '债券回售登记': -1,
    '债券回售': -1,
    '存入': 1,
    '认购': 0,
    '预分红到账': -1,
    '申购中签': 1,
    '利息兑付': 0,
    '买入': 1,
    '买入执行': 1,
    '买入确认': 1,
    '卖出确认': -1,
    '卖出到账': -1,
    '强制调减': -1,
    '强制调增': 1
}

amt_calc_map = {
    '存款到期': -1,
    '本金兑付': -1,
    '到期兑付': -1,
    '场内买入': 1,
    '场内卖出': -1,
    '融券回购': 1,
    '融券购回': -1,
    '融资回购': -1,
    '融资购回': 1,
    '申购冻结': 1,
    '提前还本': -1,
    '申购解冻': -1,
    '卖出': -1,
    '赎回到账': -1,
    '预分红': -1,
    '债券回售登记': 0,
    '债券回售': -1,
    '存入': 1,
    '认购': 0,
    '预分红到账': -1,
    '申购中签': 1,
    '利息兑付': -1,
    '买入': 1,
    '买入执行': 1,
    '买入确认': 1,
    '现金分红': -1,
    '份额分红': 1,
    '卖出确认': -1,
    '卖出到账': -1,
    '强制调减': -1,
    '强制调增': 1
}

clear_amt_map = {
    '存款到期': -1,
    '本金兑付': -1,
    '到期兑付': -1,
    '场内买入': 1,
    '场内卖出': -1,
    '融券回购': 1,
    '融券购回': -1,
    '融资回购': -1,
    '融资购回': 1,
    '申购冻结': 1,
    '提前还本': -1,
    '申购解冻': -1,
    '卖出': -1,
    '赎回到账': -1,
    '预分红': -1,
    '债券回售登记': 0,
    '债券回售': -1,
    '存入': 1,
    '认购': 0,
    '预分红到账': -1,
    '申购中签': 1,
    '利息兑付': -1,
    '买入': 1,
    '买入执行': 1,
    '买入确认': 1,
    '现金分红': -1,
    '份额分红': 0,
    '卖出确认': -1,
    '卖出到账': -1,
    '强制调减': -1,
    '强制调增': 1
}

new_file_fields = ['交易日期', '产品名称', '交易所', '证券类别',
                   '财务分类', '证券代码', '交易方向', '成交数量',
                   '成交金额', '利息金额', '清算金额', '总费用',
                   '佣金']


def read_trade_data():
    # get original trade date
    original_trade_data = filetools.read_workbook(org_file_name, org_file_path, org_data_sheets)
    # deal with the data
    trade_data_df = pd.DataFrame(original_trade_data.get(org_data_sheet_name)[1:],
                                 columns=original_trade_data.get(org_data_sheet_name)[0])
    trade_data_df = trade_data_df.dropna(axis=0, how='any', thresh=5)
    trade_data_df = trade_data_df.dropna(axis=1, how='any', thresh=5)
    trade_data_df = trade_data_df.fillna(value="")
    return trade_data_df


def judge_key_words(key_types, key_words):
    for key in key_words:
        if key in key_types:
            return True
    return False


def judge_sec_type(sec_code, sec_name, org_sec_type):
    if sec_name in alter_ast_name_list or sec_code in alter_ast_code_list or org_sec_type in org_alt_type_key_words:
        return alter_ast_type
    elif judge_key_words(org_sec_type, org_bond_type_key_words):
        return bond_type
    elif judge_key_words(org_sec_type, org_stock_type_key_words):
        return stock_type
    elif judge_key_words(org_sec_type, org_fund_type_key_words):
        return fund_type
    elif judge_key_words(org_sec_type, org_deposit_type_key_words):
        return deposit_type
    elif judge_key_words(org_sec_type, org_repo_type_key_words):
        return repo_type
    else:
        return unknown_type


def judge_exchange(sec_name, exchange, sec_type):
    if sec_name in sh_exchange_name_list:
        return sh_exchange
    if sec_type == deposit_type or sec_type == alter_ast_type or sec_name in other_exchange_name_list:
        return other_exchange
    return exchange


def judge_acct_sort(sec_type, trade_dir, invest_mark):
    if sec_type == repo_type:
        if trade_dir in reverse_repo_trade_directions:
            return reverse_repo_ctg
        elif trade_dir in positive_repo_trade_directions:
            return positive_repo_ctg
    elif sec_type == deposit_type:
        return hold_until_expiration_ctg
    else:
        return ctg_map.get(invest_mark)


def deal_with_sec_code(exchange, sec_type, sec_code):
    if sec_type == deposit_type:
        return sec_code
    elif exchange == bank_exchange and sec_type == repo_type:
        return "R0" + sec_code[1:3] + ".IB"
    else:
        return sec_code[:-2] + code_map.get(exchange)


def deal_with_sec_name(deal_dir, exchange, sec_type, sec_name, stock_name):
    if deal_dir[:2] == '融券':
        return exchange + reverse_repo_name
    elif deal_dir[:2] == '融资':
        return exchange + positive_repo_name
    elif sec_type == alter_ast_type:
        return sec_name
    else:
        return stock_name


def calc_int_amt(sec_type, deal_dir, amt, share, int_amt):
    if (sec_type + deal_dir) == '存款利息对付':
        return amt - share
    elif int_amt == '':
        return 0.0
    else:
        return float(int_amt) * amt_calc_map.get(deal_dir)


def deal_with_trade_data(trade_data_df):
    ndf = trade_data_df.copy()
    # ndf = pd.DataFrame()
    # trade date
    ndf['交易日期'] = trade_data_df['交易日期'].apply(lambda x: str(x)[:4] + "/" + str(x)[4:6] + "/" + str(x)[6:])
    # fund name
    ndf['产品名称'] = trade_data_df['产品名称'].apply(lambda x: '中英益利开泰1号资管产品' if x == '中英益利-开泰1号-建行托管' else x)
    # s type
    ndf['证券类别'] = list(map(lambda x, y, z: judge_sec_type(x, y, z), trade_data_df['证券代码'],
                           trade_data_df['证券名称'], trade_data_df['证券类别']))
    # exchange
    ndf['交易所'] = list(map(lambda x, y, z: judge_exchange(x, y, z), trade_data_df['证券名称'],
                          trade_data_df['交易所'], ndf['证券类别']))
    # 财务分类
    ndf['财务分类'] = list(map(lambda x, y, z: judge_acct_sort(x, y, z), ndf['证券类别'], trade_data_df['交易方向'],
                           trade_data_df['投资标志']))
    # scode
    ndf['证券代码'] = list(map(lambda x, y, z: deal_with_sec_code(x, y, z), ndf['交易所'], ndf['证券类别'], ndf['证券代码']))
    # trade direction 原文档中的“预分红到账”逻辑未明白：第一次为预分红，之后为预分红到账？
    ndf['交易方向'] = trade_data_df['交易方向'].apply(lambda x: dir_map.get(x))
    # sname, 由于连接wind，暂时注释掉
    w.start()
    all_stock = w.wset("sectorconstituent", "date=2017-10-04;sectorid=a001010100000000;field=wind_code,sec_name")
    all_stock_df = pd.DataFrame(all_stock.Data[1], index=all_stock.Data[0], columns=['stock_name'])
    ndf['证券名称'] = list(map(lambda x, y, z, a, b: deal_with_sec_name(x, y, z, a, b),
                           ndf['交易方向'], ndf['交易所'], ndf['证券类别'],
                           ndf['证券名称'], all_stock_df.loc[ndf['证券代码'], 'stock_name']))
    # print(all_stock_df.loc['000001.SZ', 'stock_name'])
    # deal number
    ndf['份额方向'] = ndf['交易方向'].apply(lambda x: share_calc_map.get(x))
    ndf['成交数量'] = trade_data_df['成交数量'] * ndf['份额方向']
    ndf['成交数量'] = ndf['成交数量'].apply(lambda x: 0 if x == '' else float(x))

    # deal amt
    ndf['金额方向'] = ndf['交易方向'].apply(lambda x: amt_calc_map.get(x))
    ndf['成交金额'] = trade_data_df['成交金额'] * ndf['金额方向']
    ndf['成交金额'] = ndf['成交金额'].apply(lambda x: 0 if x == '' else float(x))

    # int amt
    ndf['利息金额'] = list(map(lambda x, y, z, a, b: calc_int_amt(x, y, z, a, b), ndf['证券类别'], ndf['交易方向'],
                           ndf['成交金额'], ndf['成交数量'], trade_data_df['利息金额']))

    # clear amt TODO 清算金额有问题，待核对
    ndf['清算方向'] = ndf['交易方向'].apply(lambda x: clear_amt_map.get(x))
    ndf['清算金额'] = trade_data_df['清算金额'] * ndf['清算方向']
    ndf['清算金额'] = ndf['清算金额'].apply(lambda x: 0 if x == '' else float(x))

    # fee amt, use original total fee amt
    ndf['总费用'] = trade_data_df['总费用'].apply(lambda x: 0 if x == '' or x == 0 else 0 - float(x))

    # commission fee
    ndf['佣金'] = trade_data_df['佣金'].apply(lambda x: 0 if x == '' or x == 0 else 0 - float(x))

    # print(ndf.loc[: , new_file_fields])
    w.stop()
    return ndf


def save_trade_data(trade_data_df):
    # output to the new file
    filetools.create_workbook(result_file_name, result_file_path)
    result_data = [
        {
            "sheet_name": result_all_data_sheet_name,
            "sheet_data": trade_data_df.loc[:, new_file_fields].values.tolist(),
            "fields": new_file_fields
        }
    ]
    filetools.save_data_to_workbook(result_data, result_file_name, result_file_path)


if __name__ == "__main__":
    df = read_trade_data()
    df = deal_with_trade_data(df)
    save_trade_data(df)
    filetools.apply_number_format(result_file_name, result_file_path, result_all_data_sheet_name,
                        {
                            'A': 'mm-dd-yy',
                            'H': '0.00_);[Red]\(0.00\)',
                            'I': '0.00_);[Red]\(0.00\)',
                            'J': '0.00_);[Red]\(0.00\)',
                            'K': '0.00_);[Red]\(0.00\)',
                            'L': '0.00_);[Red]\(0.00\)',
                            'M': '0.00_);[Red]\(0.00\)'
                        })
