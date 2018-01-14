"""
汇总公司及监管各项规则，并进行校验
"""
import pandas as pd
import datetime
import configparser
import tools.assetDivision as ad

cfg = configparser.ConfigParser()
cfg.read("\\\\10.145.39.42\\北京总部文件资料\\资产管理部\\18-其他\\19-软件安装包\\小工具\\config.ini", encoding='UTF-8')
# cfg.read("d:\\config.ini", encoding='UTF-8')
RA_SECTOR = "ra"
LAST_QUARTER_TOTAL_ASSET = cfg.getfloat(RA_SECTOR, "LAST_QUARTER_TOTAL_ASSET")

CSRC_RISK_POINT_FILTER = 'CIRC_RISK_POINT'
CSRC_RISK_POINT_RULE_COLUMN = 'RULE_COLUMN'
CSRC_RISK_POINT_RULE_VALUE = 'RULE_VALUE'
CSRC_RISK_POINT_BENCHMARK = 'BENCHMARK'
CSRC_RISK_POINT_MAX_VALUE = 'RULE_MAX_VALUE'
CSRC_RISK_POINT_MIN_VALUE = 'RULE_MIN_VALUE'
CSRC_RISK_POINT_DESP = 'DESCRIPTION'
CSRC_RISK_POINT_RESULT = 'CHECK_RESULT'
CSRC_RISK_POINT_ERR_INFO = 'ERROR_INFO'
CSRC_RISK_POINT_REAL_VALUE = 'REAL_PRP'
CSRC_RISK_POINT_REAL_AMOUNT = 'REAL_AMT'

CSRC_RISK_POINT_PROPORTION = 'Proportion'
CSRC_RISK_POINT_MAX = 'max'

CSRC_RISK_POINT_FIELDS = [CSRC_RISK_POINT_DESP, CSRC_RISK_POINT_REAL_AMOUNT,
                          CSRC_RISK_POINT_BENCHMARK, CSRC_RISK_POINT_MIN_VALUE,
                          CSRC_RISK_POINT_MAX_VALUE, CSRC_RISK_POINT_REAL_VALUE,
                          CSRC_RISK_POINT_RESULT, CSRC_RISK_POINT_ERR_INFO]

SAA_TAA_RISK_POINT_RULE_COLUMN = CSRC_RISK_POINT_RULE_COLUMN
SAA_TAA_RISK_POINT_SAA_MIN_VALUE = 'SAA_MIN_VALUE'
SAA_TAA_RISK_POINT_SAA_MAX_VALUE = 'SAA_MAX_VALUE'
SAA_TAA_RISK_POINT_TAA_VALUE = 'TAA_VALUE'
SAA_TAA_RISK_POINT_TAA_VALUE_GAP = 'TAA_GAP'
SAA_TAA_RISK_POINT_CHECK_COLUMN = ad.SAA_TAA_TYPE_COLUMN_NAME
SAA_TAA_RISK_POINT_FIELDS = [CSRC_RISK_POINT_DESP, SAA_TAA_RISK_POINT_SAA_MIN_VALUE,
                             SAA_TAA_RISK_POINT_SAA_MAX_VALUE, SAA_TAA_RISK_POINT_TAA_VALUE,
                             CSRC_RISK_POINT_REAL_AMOUNT, CSRC_RISK_POINT_BENCHMARK,
                             CSRC_RISK_POINT_REAL_VALUE, CSRC_RISK_POINT_RESULT,
                             SAA_TAA_RISK_POINT_TAA_VALUE_GAP, CSRC_RISK_POINT_ERR_INFO]

RISK_POINT_GROUP_BY_COLUMN = 'GROUP_BY'
CONCENTRATION_TOP_THREE_INFO = 'INFO'
CT_NAME_FILTER = 'CT_NAME_FILTER'
CTR_RISK_POINT_FIELDS = [CSRC_RISK_POINT_DESP, CSRC_RISK_POINT_RESULT,
                         CONCENTRATION_TOP_THREE_INFO]

"""
采用map形式存储csrc风险检查规则，原理为：
1、通过具体列的筛选规则筛选出数据，目前支持两列的or和and合并，目前每列只支持一个参数
   如果筛选逻辑复杂，考虑在AssetDivision中增加一列进行标识
2、检查规则包括汇总比例校验（Proportion），最大值检查（Max），最小值检查（Min），平均数检查等等
   目前只支持汇总比例校验
3、设置比例的benchmark、最大值和最小值
4、设置校验规则的描述信息
5、---调用校验程序
6、设置校验结果和错误描述信息
"""


def csrc_risk_arbitrator(org_data):
    csrc_risk_rules = {
        '1':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_LQ,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MIN_VALUE: 0.05,
                CSRC_RISK_POINT_DESP: '流动性资产与剩余期限在1年以上的政府债券、准政府债券>=5%*ACL上季末总资产'
            },
        '2':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_BOND_UNDER_AA,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CSRC_RISK_POINT_DESP: '境内的具有国内信用评级机构评定的AA级(含)以下长期信用评级的债券<=10%*ACL上季末总资产'
            },
        '3':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_EQ,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CSRC_RISK_POINT_DESP: '权益类资产<=30%*ACL上季末总资产'
            },
        '4':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_EQ,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.2,
                CSRC_RISK_POINT_DESP: '权益类资产<=20%*ACL上季末总资产'
            },
        '5':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_ET,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CSRC_RISK_POINT_DESP: '不动产类资产<=30%*ACL上季末总资产'
            },
        '6':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_ET,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.2,
                CSRC_RISK_POINT_DESP: '不动产类资产<=20%*ACL上季末总资产'
            },
        '7':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_OTHER,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.25,
                CSRC_RISK_POINT_DESP: '其他金融资产<=25%*ACL上季末总资产'
            },
        '8':
            {
                CSRC_RISK_POINT_FILTER: ad.CSRC_RISK_POINT_OTHER,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_PROPORTION,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.15,
                CSRC_RISK_POINT_DESP: '其他金融资产<=15%*ACL上季末总资产'
            }
    }
    for rule in csrc_risk_rules:
        info = csrc_risk_rules.get(rule)
        if CSRC_RISK_POINT_FILTER in info:
            rule_df = org_data[org_data.CIRC_RISK_POINT == info[CSRC_RISK_POINT_FILTER]]
        else:
            rule_df = org_data
        real_sum = rule_df[info[CSRC_RISK_POINT_RULE_COLUMN]].sum()
        info[CSRC_RISK_POINT_REAL_AMOUNT] = real_sum
        if info[CSRC_RISK_POINT_RULE_VALUE] == CSRC_RISK_POINT_PROPORTION:
            prp = real_sum / info[CSRC_RISK_POINT_BENCHMARK]
            info[CSRC_RISK_POINT_REAL_VALUE] = prp
            max_flag = True
            min_flag = True
            err_info = ""
            if CSRC_RISK_POINT_MAX_VALUE in info and prp > info[CSRC_RISK_POINT_MAX_VALUE]:
                max_flag = False
                err_info += " (超越上限) "
            if CSRC_RISK_POINT_MIN_VALUE in info and prp < info[CSRC_RISK_POINT_MIN_VALUE]:
                min_flag = False
                err_info += " (低于下限) "
            result = max_flag and min_flag
            info[CSRC_RISK_POINT_RESULT] = result
            info[CSRC_RISK_POINT_ERR_INFO] = err_info

    rule_map_df = pd.DataFrame(csrc_risk_rules)
    rule_map_df_t = rule_map_df.T

    # 数据统一保存
    # ad.dt.save_asset_data(rule_map_df_t, "大类资产及可投资品种合规点", rp_date=rp_date,
    #                       fields=CSRC_RISK_POINT_FIELDS)

    return rule_map_df_t


def saa_taa_risk_arbitrator(org_data):
    saa_taa_risk_rules = {
        '1':
            {
                SAA_TAA_RISK_POINT_CHECK_COLUMN: ad.SAA_TAA_TYPE_MM,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                SAA_TAA_RISK_POINT_SAA_MIN_VALUE: 0.01,
                SAA_TAA_RISK_POINT_SAA_MAX_VALUE: 0.25,
                SAA_TAA_RISK_POINT_TAA_VALUE: 0.023,
                CSRC_RISK_POINT_DESP: ad.SAA_TAA_TYPE_MM
            },
        '2':
            {
                SAA_TAA_RISK_POINT_CHECK_COLUMN: ad.SAA_TAA_TYPE_DEPOSIT,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                SAA_TAA_RISK_POINT_SAA_MIN_VALUE: 0.02,
                SAA_TAA_RISK_POINT_SAA_MAX_VALUE: 0.20,
                SAA_TAA_RISK_POINT_TAA_VALUE: 0.042,
                CSRC_RISK_POINT_DESP: ad.SAA_TAA_TYPE_DEPOSIT
            },
        '3':
            {
                SAA_TAA_RISK_POINT_CHECK_COLUMN: ad.SAA_TAA_TYPE_IR,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                SAA_TAA_RISK_POINT_SAA_MIN_VALUE: 0.03,
                SAA_TAA_RISK_POINT_SAA_MAX_VALUE: 0.30,
                SAA_TAA_RISK_POINT_TAA_VALUE: 0.037,
                CSRC_RISK_POINT_DESP: ad.SAA_TAA_TYPE_IR
            },
        '4':
            {
                SAA_TAA_RISK_POINT_CHECK_COLUMN: ad.SAA_TAA_TYPE_CR,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                SAA_TAA_RISK_POINT_SAA_MIN_VALUE: 0.2,
                SAA_TAA_RISK_POINT_SAA_MAX_VALUE: 0.65,
                SAA_TAA_RISK_POINT_TAA_VALUE: 0.276,
                CSRC_RISK_POINT_DESP: ad.SAA_TAA_TYPE_CR
            },
        '5':
            {
                SAA_TAA_RISK_POINT_CHECK_COLUMN: ad.SAA_TAA_TYPE_EQ,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                SAA_TAA_RISK_POINT_SAA_MIN_VALUE: 0,
                SAA_TAA_RISK_POINT_SAA_MAX_VALUE: 0.25,
                SAA_TAA_RISK_POINT_TAA_VALUE: 0.074,
                CSRC_RISK_POINT_DESP: ad.SAA_TAA_TYPE_EQ
            },
        '6':
            {
                SAA_TAA_RISK_POINT_CHECK_COLUMN: ad.SAA_TAA_TYPE_NON_STANDARD,
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                SAA_TAA_RISK_POINT_SAA_MIN_VALUE: 0.2,
                SAA_TAA_RISK_POINT_SAA_MAX_VALUE: 0.6,
                SAA_TAA_RISK_POINT_TAA_VALUE: 0.548,
                CSRC_RISK_POINT_DESP: ad.SAA_TAA_TYPE_NON_STANDARD
            }
    }

    for rule in saa_taa_risk_rules:
        info = saa_taa_risk_rules.get(rule)
        if SAA_TAA_RISK_POINT_CHECK_COLUMN in info:
            rule_df = org_data[org_data.SAA_TAA_TYPE == info[SAA_TAA_RISK_POINT_CHECK_COLUMN]]
        else:
            rule_df = org_data
        real_sum = rule_df[info[CSRC_RISK_POINT_RULE_COLUMN]].sum()
        # 汇总账面全价
        benchmark = org_data[info[CSRC_RISK_POINT_RULE_COLUMN]].sum()
        info[CSRC_RISK_POINT_BENCHMARK] = benchmark
        info[CSRC_RISK_POINT_REAL_AMOUNT] = real_sum
        prp = real_sum / benchmark
        info[CSRC_RISK_POINT_REAL_VALUE] = prp
        max_flag = True
        min_flag = True
        err_info = ""
        if SAA_TAA_RISK_POINT_SAA_MAX_VALUE in info and prp > info[SAA_TAA_RISK_POINT_SAA_MAX_VALUE]:
            max_flag = False
            err_info += " (超越SAA上限) "
        if SAA_TAA_RISK_POINT_SAA_MIN_VALUE in info and prp < info[SAA_TAA_RISK_POINT_SAA_MIN_VALUE]:
            min_flag = False
            err_info += " (低于SAA下限) "
        result = max_flag and min_flag
        info[CSRC_RISK_POINT_RESULT] = result
        info[CSRC_RISK_POINT_ERR_INFO] = err_info
        if SAA_TAA_RISK_POINT_TAA_VALUE in info:
            info[SAA_TAA_RISK_POINT_TAA_VALUE_GAP] = prp - float(info[SAA_TAA_RISK_POINT_TAA_VALUE])

    rule_map_df = pd.DataFrame(saa_taa_risk_rules)
    rule_map_df_t = rule_map_df.T

    return rule_map_df_t


def top_three_filter(df_info, rule_info, group_column, sum_column):
    group_df = df_info.groupby(group_column).agg({sum_column: sum})
    top_three = group_df[sum_column].nlargest(3)
    if rule_info[CSRC_RISK_POINT_RULE_VALUE] == CSRC_RISK_POINT_MAX:
        top_one_rate = top_three[0] / rule_info[CSRC_RISK_POINT_BENCHMARK]
        max_flag = True
        err_info = ""
        if CSRC_RISK_POINT_MAX_VALUE in rule_info and top_one_rate > rule_info[CSRC_RISK_POINT_MAX_VALUE]:
            max_flag = False
            err_info += " (超越上限) "
        rule_info[CSRC_RISK_POINT_RESULT] = max_flag
        rule_info[CSRC_RISK_POINT_ERR_INFO] = err_info
        top_three_str = "top three: " + "、".join(top_three.index) + "\n  percent: "
        top_three_rate = top_three.values / rule_info[CSRC_RISK_POINT_BENCHMARK] * 100
        percent_str = ""
        for rate in top_three_rate:
            percent_str += " " + str("%.4f" % rate) + '%'
        rule_info[CONCENTRATION_TOP_THREE_INFO] = top_three_str + percent_str


# 单一法人检查
def ctr_legal_risk_arbitrator(org_data):
    ctr_legal_risk_rules = {
        '1':
            {
                CSRC_RISK_POINT_RULE_COLUMN: ad.dt.BASE_COLUMN_BOOK_VALUE,
                RISK_POINT_GROUP_BY_COLUMN: ad.dt.BASE_COLUMN_FINANCIERS,
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.2,
                CSRC_RISK_POINT_DESP: '单一法人主体余额<=20%*ACL上季末总资产'
            }
    }
    for rule in ctr_legal_risk_rules:
        info = ctr_legal_risk_rules.get(rule)
        if RISK_POINT_GROUP_BY_COLUMN in info:
            rule_df = org_data[org_data[ad.CSRC_ASSET_COLUMN_SECOND_CLASS] !=
                               ad.CSRC_LIQUIDITY_ASSET_SECOND_CLASS_GOV_BOND_UNDER_ONE]
            rule_df = rule_df[rule_df[ad.CSRC_ASSET_COLUMN_SECOND_CLASS] !=
                              ad.CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE]
            rule_df = rule_df[(rule_df[ad.dt.BASE_COLUMN_FIRST_CLASS] == ad.dt.FIRST_CLASS_BOND) |
                              (rule_df[ad.dt.BASE_COLUMN_FIRST_CLASS] == ad.dt.FIRST_CLASS_STOCK) |
                              (rule_df[ad.dt.BASE_COLUMN_FIRST_CLASS] == ad.dt.FIRST_CLASS_DEPOSIT) |
                              (rule_df[ad.dt.BASE_COLUMN_FIRST_CLASS] == ad.dt.FIRST_CLASS_NON_STANDARD)]
            group_column = info[RISK_POINT_GROUP_BY_COLUMN]
            top_three_filter(rule_df, info, group_column, info[CSRC_RISK_POINT_RULE_COLUMN])

    rule_map_df = pd.DataFrame(ctr_legal_risk_rules)
    rule_map_df_t = rule_map_df.T

    return rule_map_df_t


# 单一交易对手检查
def ctr_counter_party_risk_arbitrator(org_data):
    group_column = ad.dt.BASE_COLUMN_COUNTER_PARTY
    sum_column = ad.dt.BASE_COLUMN_BOOK_VALUE
    ctr_ct_risk_rules = {
        '1':
            {
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.025,
                CT_NAME_FILTER: ad.CT_CLASS_UP_AA,
                CSRC_RISK_POINT_DESP: '一般企业（AA评级以上）<=2.5%*ACL上季末总资产'
            }
        ,
        '2':
            {
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0,
                CT_NAME_FILTER: ad.CT_CLASS_UNDER_AA,
                CSRC_RISK_POINT_DESP: '一般企业（AA评级以下）<=0%*ACL上季末总资产'
            }
        ,
        '3':
            {
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.075,
                CSRC_RISK_POINT_DESP: '建设/交通/农业银行<=7.5%*ACL上季末总资产',
                CT_NAME_FILTER: ad.CT_CLASS_SPECIAL_BANK
            }
        ,
        '4':
            {
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.05,
                CSRC_RISK_POINT_DESP: '其他银行<=5%*ACL上季末总资产',
                CT_NAME_FILTER: ad.CT_CLASS_OTHER_BANK
            }
        ,
        '5':
            {
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CSRC_RISK_POINT_DESP: '中央国有企业分组1<=10%*ACL上季末总资产',
                CT_NAME_FILTER: ad.CT_CLASS_GROUP_ONE
            }
        ,
        '6':
            {
                CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.025,
                CSRC_RISK_POINT_DESP: '中央国有企业分组2<=2.5%*ACL上季末总资产',
                CT_NAME_FILTER: ad.CT_CLASS_GROUP_TWO
            }
    }
    rule_df = org_data[(org_data[ad.dt.BASE_COLUMN_FIRST_CLASS].isin([ad.dt.FIRST_CLASS_BOND, ad.dt.FIRST_CLASS_DEPOSIT,
                                                                      ad.dt.FIRST_CLASS_NON_STANDARD]))]
    rule_df = rule_df[rule_df[ad.CSRC_ASSET_COLUMN_SECOND_CLASS] !=
                      ad.CSRC_LIQUIDITY_ASSET_SECOND_CLASS_GOV_BOND_UNDER_ONE]
    rule_df = rule_df[rule_df[ad.CSRC_ASSET_COLUMN_SECOND_CLASS] !=
                      ad.CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE]
    for rule in ctr_ct_risk_rules:
        info = ctr_ct_risk_rules.get(rule)

        if CT_NAME_FILTER in info:
            temp_df = rule_df[rule_df[ad.COUNTER_PARTY_CLASS_COLUMN_NAME] == info[CT_NAME_FILTER]]
        else:
            temp_df = rule_df
        if temp_df.empty:
            info[CSRC_RISK_POINT_RESULT] = True
            info[CONCENTRATION_TOP_THREE_INFO] = 'No Asset.'
            continue
        top_three_filter(temp_df, info, group_column, sum_column)

    rule_map_df = pd.DataFrame(ctr_ct_risk_rules)
    rule_map_df_t = rule_map_df.T

    return rule_map_df_t


# 单一品种检查
def ctr_single_asset_risk_arbitrator(org_data):
    rule = {"rule": {
            CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
            CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
            CSRC_RISK_POINT_MAX_VALUE: 0.05,
            CSRC_RISK_POINT_DESP: '单一固定收益类资产、权益类资产、不动产类资产、其他金融资产的账面余额<=5%*ACL上季末总资产'}
    }
    rule_df = org_data[(org_data[ad.CSRC_ASSET_COLUMN_FIRST_CLASS].isin([ad.CSRC_FIRST_CLASS_FIXED_INCOME_ASSET,
                                                                         ad.CSRC_FIRST_CLASS_ESTATE_ASSET,
                                                                         ad.CSRC_FIRST_CLASS_EQUITY_ASSET,
                                                                         ad.CSRC_FIRST_CLASS_OTHER_ASSET]))]
    info = rule.get("rule")
    if rule_df.empty:
        info[CSRC_RISK_POINT_RESULT] = True
        info[CONCENTRATION_TOP_THREE_INFO] = 'No Asset.'
    else:
        group_column = ad.dt.BASE_COLUMN_ASSET_NAME
        sum_column = ad.dt.BASE_COLUMN_BOOK_VALUE
        top_three_filter(rule_df, info, group_column, sum_column)

    rule_map_df = pd.DataFrame(rule)
    rule_map_df_t = rule_map_df.T

    return rule_map_df_t


# 账户内单一品种检查
def ctr_single_asset_in_account_risk_arbitrator(org_data):
    rule = {"rule": {
        CSRC_RISK_POINT_RULE_VALUE: CSRC_RISK_POINT_MAX,  # max, min
        CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
        CSRC_RISK_POINT_MAX_VALUE: 0.01,
        CSRC_RISK_POINT_DESP: '单只股票或非货币基金在单一委托账户（万能险账户合并计算，投连账户除外）<=1%*ACL上季末总资产'}
    }
    rule_df = org_data[(org_data[ad.CSRC_ASSET_COLUMN_SECOND_CLASS].isin([ad.CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK,
                                                                          ad.CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK_FUND,
                                                                          ad.CSRC_EQUITY_ASSET_SECOND_CLASS_MIXED_FUND,
                                                                          ad.CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_FUND]))]
    info = rule.get("rule")
    if rule_df.empty:
        info[CSRC_RISK_POINT_RESULT] = True
        info[CONCENTRATION_TOP_THREE_INFO] = 'No Asset.'
    else:
        # group_column = "[" + ad.dt.BASE_COLUMN_ASSET_NAME + "', '" + ad.dt.BASE_COLUMN_ACCOUNT + "']"
        group_column = [ad.dt.BASE_COLUMN_ASSET_NAME, ad.dt.BASE_COLUMN_ACCOUNT]
        sum_column = ad.dt.BASE_COLUMN_BOOK_VALUE
        # top_three_filter(rule_df, info, group_column, sum_column)
        group_df = rule_df.groupby(group_column).agg({sum_column: sum})
        top_three = group_df[sum_column].nlargest(3)
        if info[CSRC_RISK_POINT_RULE_VALUE] == CSRC_RISK_POINT_MAX:
            top_one_rate = top_three[0] / info[CSRC_RISK_POINT_BENCHMARK]
            max_flag = True
            err_info = ""
            if CSRC_RISK_POINT_MAX_VALUE in info and top_one_rate > info[CSRC_RISK_POINT_MAX_VALUE]:
                max_flag = False
                err_info += " (超越上限) "
            info[CSRC_RISK_POINT_RESULT] = max_flag
            info[CSRC_RISK_POINT_ERR_INFO] = err_info
            top_three_str = "top three: "
            for index_str in top_three.index:
                top_three_str += index_str[0] + "(" + index_str[1] + ") "
            top_three_str += "\npercent: "
            top_three_rate = top_three.values / info[CSRC_RISK_POINT_BENCHMARK] * 100
            percent_str = ""
            for rate in top_three_rate:
                percent_str += " " + str("%.4f" % rate) + '%'
            info[CONCENTRATION_TOP_THREE_INFO] = top_three_str + percent_str

    rule_map_df = pd.DataFrame(rule)
    rule_map_df_t = rule_map_df.T

    return rule_map_df_t


def ctr_industry_risk_arbitrator(org_data):
    ctr_industry_risk_rules = {
        '1':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.6,
                CT_NAME_FILTER: "金融业",
                CSRC_RISK_POINT_DESP: '金融业 限额：60%'
            }
        ,
        '2':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CT_NAME_FILTER: "交通运输、仓储和邮政业",
                CSRC_RISK_POINT_DESP: '交通运输、仓储和邮政业 限额：30%'
            }
        ,
        '3':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CT_NAME_FILTER: "电力、热力、燃气及水生产和供应业",
                CSRC_RISK_POINT_DESP: '电力、热力、燃气及水生产和供应业 限额：30%'
            }
        ,
        '4':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CT_NAME_FILTER: "采矿业",
                CSRC_RISK_POINT_DESP: '采矿业 限额：30%'
            }
        ,
        '5':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CT_NAME_FILTER: "综合",
                CSRC_RISK_POINT_DESP: '综合 限额：30%'
            }
        ,
        '6':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.2,
                CT_NAME_FILTER: "建筑业",
                CSRC_RISK_POINT_DESP: '建筑业 限额：20%'
            }
        ,
        '7':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.15,
                CT_NAME_FILTER: "制造业",
                CSRC_RISK_POINT_DESP: '制造业 限额：15%'
            }
        ,
        '8':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "批发和零售业",
                CSRC_RISK_POINT_DESP: '批发和零售业 限额：10%'
            }
        ,
        '9':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.3,
                CT_NAME_FILTER: "信息传输、软件和信息技术服务业",
                CSRC_RISK_POINT_DESP: '信息传输、软件和信息技术服务业 限额：10%'
            }
        ,
        '10':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "科学研究和技术服务业",
                CSRC_RISK_POINT_DESP: '科学研究和技术服务业 限额：10%'
            }
        ,
        '11':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.25,
                CT_NAME_FILTER: "房地产业",
                CSRC_RISK_POINT_DESP: '房地产业 限额：25%'
            }
        ,
        '12':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "租赁和商务服务业",
                CSRC_RISK_POINT_DESP: '租赁和商务服务业 限额：10%'
            }
        ,
        '13':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "文化、体育和娱乐业",
                CSRC_RISK_POINT_DESP: '文化、体育和娱乐业 限额：10%'
            }
        ,
        '14':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.15,
                CT_NAME_FILTER: "水利、环境和公共设施管理业",
                CSRC_RISK_POINT_DESP: '水利、环境和公共设施管理业 限额：15%'
            }
        ,
        '15':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "农、林、牧、渔业",
                CSRC_RISK_POINT_DESP: '农、林、牧、渔业 限额：10%'
            }
        ,
        '16':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "教育",
                CSRC_RISK_POINT_DESP: '教育 限额：10%'
            }
        ,
        '17':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "卫生和社会工作业",
                CSRC_RISK_POINT_DESP: '卫生和社会工作业 限额：10%'
            }
        ,
        '18':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "住宿和餐饮业",
                CSRC_RISK_POINT_DESP: '住宿和餐饮业 限额：10%'
            }
        ,
        '19':
            {
                CSRC_RISK_POINT_BENCHMARK: LAST_QUARTER_TOTAL_ASSET,
                CSRC_RISK_POINT_MAX_VALUE: 0.1,
                CT_NAME_FILTER: "其他证监会新增行业分类",
                CSRC_RISK_POINT_DESP: '其他证监会新增行业分类 限额：10%'
            }
    }
    benchmark = org_data[ad.dt.BASE_COLUMN_BOOK_VALUE].sum()
    group_column = ad.dt.BASE_COLUMN_CIRC_INDUSTRY_FIRST
    sum_column = ad.dt.BASE_COLUMN_BOOK_VALUE
    group_df = org_data.groupby(group_column).agg({sum_column: sum})
    for rule in ctr_industry_risk_rules:
        info = ctr_industry_risk_rules.get(rule)
        str_filter = info[CT_NAME_FILTER]
        if str_filter in group_df.index:
            rule_amt = group_df[group_df.index == str_filter]
            prp = rule_amt / benchmark
            real_amt = prp.values[0][0]
            flag = True
            if real_amt > info[CSRC_RISK_POINT_MAX_VALUE]:
                flag = False
            info[CSRC_RISK_POINT_RESULT] = flag
            real_amt *= 100
            info[CONCENTRATION_TOP_THREE_INFO] = "实际占比: " + str("%.4f" % real_amt) + '%'
        else:
            info[CSRC_RISK_POINT_RESULT] = True
            info[CONCENTRATION_TOP_THREE_INFO] = "No Asset."

    rule_map_df = pd.DataFrame(ctr_industry_risk_rules)
    rule_map_df_t = rule_map_df.T

    return rule_map_df_t


def concentration_risk_arbitrator(org_data):
    legal_rule_map_df_t = ctr_legal_risk_arbitrator(org_data)
    counter_party_rule_map_df_t = ctr_counter_party_risk_arbitrator(org_data)
    single_asset_rule_map_df_t = ctr_single_asset_risk_arbitrator(org_data)
    single_asset_with_account_rule_map_df_t = ctr_single_asset_in_account_risk_arbitrator(org_data)
    industry_rule_map_df_t = ctr_industry_risk_arbitrator(org_data)

    rule_map_df_t = pd.concat([legal_rule_map_df_t, counter_party_rule_map_df_t, single_asset_rule_map_df_t,
                               single_asset_with_account_rule_map_df_t, industry_rule_map_df_t])

    return rule_map_df_t


# if __name__ == '__main__':
#     rp_date = datetime.date(2017, 10, 19)
#     clean_asset_data = ad.dt.data_bowl(rp_date=rp_date)
#     clean_asset_data = ad.csrc_asset_class_maker(clean_asset_data)
#     # ad.dt.save_asset_data(clean_asset_data, "detail", rp_date=datetime.date(2017, 10, 12),
#     #                       fields=ad.ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS)
#     risk_check_map = csrc_risk_arbitrator(clean_asset_data)
#     saa_taa_check_map = saa_taa_risk_arbitrator(clean_asset_data)
#     concentration_risk_arbitrator(clean_asset_data)
