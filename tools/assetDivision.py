"""
根据资产属性确认分类。
"""
import tools.dataTerminator as dt
import datetime

LAST_QUARTER_TOTAL_ASSET = 29411764705.88

CSRC_ASSET_COLUMN_FIRST_CLASS = 'CIRC大类资产'
# 证监会资产大类包括
CSRC_FIRST_CLASS_LIQUIDITY_ASSET = '流动性资产'
CSRC_FIRST_CLASS_FIXED_INCOME_ASSET = '固定收益类资产'
CSRC_FIRST_CLASS_EQUITY_ASSET = '权益类资产'
CSRC_FIRST_CLASS_ESTATE_ASSET = '不动产类资产'
CSRC_FIRST_CLASS_OTHER_ASSET = '其他金融资产'
CSRC_FIRST_CLASS_UNKNOWN = '未知大类资产'

CSRC_ASSET_COLUMN_SECOND_CLASS = 'CIRC资产类别'
# 证监会资产二级分类
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CASH = '现金及现金等价物'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_TERM_DEPOSIT_UNDER_ONE = '定期存款（<1年）'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_DEPOSIT = '活期存款'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_IC_UNDER_ONE = '同业存单<1year'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_LD_UNDER_ONE = '大额存单<1year'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_FUND = '货币市场基金'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_REVERSE_REPO = '债券逆回购'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_GOV_BOND_UNDER_ONE = '剩余期限不足一年的政府债、准政府债'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CP = '短期融资券'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_SCP = '超短期融资券'
CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_PRODUCT = '货币市场类保险资产管理产品'
CSRC_LIQUIDITY_ASSET_LIST = [
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CASH,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_TERM_DEPOSIT_UNDER_ONE,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_DEPOSIT,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_IC_UNDER_ONE,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_LD_UNDER_ONE,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_FUND,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_REVERSE_REPO,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_GOV_BOND_UNDER_ONE,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CP,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_SCP,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_PRODUCT
]
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_TERM_DEPOSIT_UP_ONE = '定期存款（>=1年）'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_AGREEMENT_DEPOSIT = '协议存款'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_IC_UP_ONE = '同业存单>=1year'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_LD_UP_ONE = '大额存单>=1year'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE = '剩余期限1年以上的政府债、准政府债'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FIN_BOND = '金融企业（公司）债'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_SECURED = '非金融企业（公司）债—有担保'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_UNSECURED = '非金融企业（公司）债—无担保'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_FUND = '债券型基金'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_CONVERT = '可转债'
CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FI_PRODUCT = '固定收益类保险资产管理产品'
CSRC_FIXED_INCOME_ASSET_LIST = [
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_TERM_DEPOSIT_UP_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_AGREEMENT_DEPOSIT,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_IC_UP_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_LD_UP_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FIN_BOND,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_SECURED,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_UNSECURED,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_FUND,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_CONVERT,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FI_PRODUCT
]
CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK = '普通股票'
CSRC_EQUITY_ASSET_SECOND_CLASS_PREFERRED = '优先股'
CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK_FUND = '股票基金'
CSRC_EQUITY_ASSET_SECOND_CLASS_MIXED_FUND = '混合型基金'
CSRC_EQUITY_ASSET_SECOND_CLASS_IPO = '新股（IPO）'
CSRC_EQUITY_ASSET_SECOND_CLASS_EQUITY_PRODUCT = '权益类保险资产管理产品'
CSRC_EQUITY_ASSET_SECOND_CLASS_UNLISTED_EQUITY = '未上市股权'
CSRC_EQUITY_ASSET_SECOND_CLASS_UE_PRODUCT = '未上市企业股权投资基金等相关金融产品'
CSRC_EQUITY_ASSET_LIST = [
    CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK,
    CSRC_EQUITY_ASSET_SECOND_CLASS_PREFERRED,
    CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK_FUND,
    CSRC_EQUITY_ASSET_SECOND_CLASS_MIXED_FUND,
    CSRC_EQUITY_ASSET_SECOND_CLASS_IPO,
    CSRC_EQUITY_ASSET_SECOND_CLASS_EQUITY_PRODUCT,
    CSRC_EQUITY_ASSET_SECOND_CLASS_UNLISTED_EQUITY,
    CSRC_EQUITY_ASSET_SECOND_CLASS_UE_PRODUCT
]
CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE = '不动产'
CSRC_ESTATE_ASSET_SECOND_CLASS_INFRASTRUCTURE_PLAN = '基础设施投资计划'
CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PLAN = '不动产投资计划'
CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PRODUCT = '不动产类保险资产管理产品'
CSRC_ESTATE_ASSET_SECOND_CLASS_OTHERS = '其他不动产相关金融产品'
CSRC_ESTATE_ASSET_LIST = [
    CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE,
    CSRC_ESTATE_ASSET_SECOND_CLASS_INFRASTRUCTURE_PLAN,
    CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PLAN,
    CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PRODUCT,
    CSRC_ESTATE_ASSET_SECOND_CLASS_OTHERS
]
CSRC_OTHER_ASSET_SECOND_CLASS_BANK_PRODUCT = '商业银行理财产品'
CSRC_OTHER_ASSET_SECOND_CLASS_BANK_ABS = '银行业金融机构信贷资产支持证券'
CSRC_OTHER_ASSET_SECOND_CLASS_TRUST_PLAN = '信托公司集合资金信托计划'
CSRC_OTHER_ASSET_SECOND_CLASS_SECURITY_PLAN = '证券公司专项资产管理计划'
CSRC_OTHER_ASSET_SECOND_CLASS_INSURANCE_PLAN = '保险资产管理公司资产支持计划'
CSRC_OTHER_ASSET_SECOND_CLASS_OTHER_INSURANCE_PLAN = '其他保险资产管理产品'
CSRC_OTHER_ASSET_SECOND_CLASS_OTHERS = '其他中国保监会允许的投资品种'
CSRC_OTHER_ASSET_LIST = [
    CSRC_OTHER_ASSET_SECOND_CLASS_BANK_PRODUCT,
    CSRC_OTHER_ASSET_SECOND_CLASS_BANK_ABS,
    CSRC_OTHER_ASSET_SECOND_CLASS_TRUST_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_SECURITY_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_INSURANCE_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_OTHER_INSURANCE_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_OTHERS
]
CSRC_SECOND_CLASS_UNKNOWN = '未知资产类别'

CSRC_COLUMN_RISK_POINT = 'CIRC_RISK_POINT'
# 监管合规分类
CSRC_RISK_POINT_LQ = 'LQ'
CSRC_RISK_POINT_BOND_UNDER_AA = 'UA'
CSRC_RISK_POINT_EQ = 'EQ'
CSRC_RISK_POINT_ET = 'ET'
CSRC_RISK_POINT_OTHER = 'OTHER'

# 原始数据一级分类
FIRST_CLASS_FUND = '基金'
FIRST_CLASS_STOCK = '股票'
FIRST_CLASS_BOND = '债券'
FIRST_CLASS_DEPOSIT = '存款'
FIRST_CLASS_NON_STANDARD = '另类'
FIRST_CLASS_MM = '货币市场'
FIRST_CLASS_REPO = '回购'

# 原始数据二级分类
FUND_ASSET_CURRENCY = '货币型基金'
FUND_ASSET_STOCK = '股票型基金'
FUND_ASSET_MIXED = '混合型基金'
FUND_ASSET_BOND = '债券型基金'
FUND_ASSET_FIXED_PRODUCT = '固收类保险资管产品'
FUND_ASSET_EQUITY_PRODUCT = '权益类保险资管产品'
STOCK_ASSET_MOTHERBOARD = '沪深主板'
STOCK_ASSET_MEDIUM = '中小板'
STOCK_ASSET_GEM = '创业板'
BOND_ASSET_CP = '短期融资券'
BOND_ASSET_IC = '同业存单'
BOND_ASSET_CD = '企业债'
BOND_ASSET_BANK = '政策银行债'
BOND_ASSET_FINANCIAL = '金融债'
BOND_ASSET_TREASURY = '国债'
BOND_ASSET_CONVERT = '可转债'
DEPOSIT_ASSET_TERM = '定期存款'
DEPOSIT_ASSET_AGREEMENT = '协议存款'
NON_STANDARD_ASSET_TRUST = '集合资金信托计划'
NON_STANDARD_ASSET_PROJECT = '项目资产支持计划'
NON_STANDARD_ASSET_ESTATE = '不动产债权计划'
NON_STANDARD_ASSET_PREFERRED = '优先股'
NON_STANDARD_ASSET_STOCK = '股权投资基金'
NON_STANDARD_ASSET_OTHER = '其他保险资管产品'
NON_STANDARD_ASSET_INFRASTRUCTURE = '基础设施债权计划'
NON_STANDARD_ASSET_ESTATE_PRODUCT = '不动产金融产品'
MM_ASSET_DEPOSIT = '活期存款'
MM_ASSET_TRANSIT = '其他结算在途'
REPO_ASSET_REVERSE = '融券回购'

SAA_TAA_TYPE_COLUMN_NAME = 'SAA_TAA_TYPE'
COUNTER_PARTY_CLASS_COLUMN_NAME = '交易对手分类'

ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS = dt.ASSET_DETAIL_FIELDS
ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS.append(CSRC_ASSET_COLUMN_FIRST_CLASS)
ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS.append(CSRC_ASSET_COLUMN_SECOND_CLASS)
ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS.append(CSRC_COLUMN_RISK_POINT)
ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS.append(SAA_TAA_TYPE_COLUMN_NAME)
ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS.append(COUNTER_PARTY_CLASS_COLUMN_NAME)

SAA_TAA_TYPE_MM = '货币市场'
SAA_TAA_TYPE_MM_LIST = [
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CASH,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_DEPOSIT,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_IC_UNDER_ONE,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_LD_UNDER_ONE,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_FUND,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_REVERSE_REPO,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CP,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_SCP,
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_PRODUCT
]
SAA_TAA_TYPE_DEPOSIT = '银行存款'
SAA_TAA_TYPE_DEPOSIT_LIST = [
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_TERM_DEPOSIT_UNDER_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_TERM_DEPOSIT_UP_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_AGREEMENT_DEPOSIT,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_IC_UP_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_LD_UP_ONE
]
SAA_TAA_TYPE_IR = '利率产品'
SAA_TAA_TYPE_IR_LIST = [
    CSRC_LIQUIDITY_ASSET_SECOND_CLASS_GOV_BOND_UNDER_ONE,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE
]
SAA_TAA_TYPE_CR = '信用产品'
SAA_TAA_TYPE_CR_LIST = [
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FIN_BOND,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_SECURED,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_UNSECURED,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_FUND,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_CONVERT,
    CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FI_PRODUCT
]
SAA_TAA_TYPE_EQ = '权益投资'
SAA_TAA_TYPE_EQ_LIST = [
    CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK,
    CSRC_EQUITY_ASSET_SECOND_CLASS_PREFERRED,
    CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK_FUND,
    CSRC_EQUITY_ASSET_SECOND_CLASS_MIXED_FUND,
    CSRC_EQUITY_ASSET_SECOND_CLASS_IPO,
    CSRC_EQUITY_ASSET_SECOND_CLASS_EQUITY_PRODUCT,
    CSRC_EQUITY_ASSET_SECOND_CLASS_UNLISTED_EQUITY,
    CSRC_EQUITY_ASSET_SECOND_CLASS_UE_PRODUCT
]
SAA_TAA_TYPE_NON_STANDARD = '另类投资'
SAA_TAA_TYPE_NON_STANDARD_LIST = [
    CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE,
    CSRC_ESTATE_ASSET_SECOND_CLASS_INFRASTRUCTURE_PLAN,
    CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PLAN,
    CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PRODUCT,
    CSRC_ESTATE_ASSET_SECOND_CLASS_OTHERS,
    CSRC_OTHER_ASSET_SECOND_CLASS_BANK_PRODUCT,
    CSRC_OTHER_ASSET_SECOND_CLASS_BANK_ABS,
    CSRC_OTHER_ASSET_SECOND_CLASS_TRUST_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_SECURITY_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_INSURANCE_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_OTHER_INSURANCE_PLAN,
    CSRC_OTHER_ASSET_SECOND_CLASS_OTHERS
]

BANK_NAME_LIST = ['中国建设银行股份有限公司', '中国农业银行股份有限公司', '交通银行股份有限公司']
GROUP_ONE_NAME_LIST = ['中国核工业集团公司', '中国核工业建设集团公司', '中国航天科技集团公司', '中国航天科工集团公司',
                       '中国航空工业集团公司', '中国船舶工业集团公司', '中国船舶重工集团公司', '中国兵器工业集团公司',
                       '中国兵器装备集团公司', '中国电子科技集团公司', '中国石油天然气集团公司', '中国石油化工集团公司',
                       '中国海洋石油总公司', '国家电网公司', '中国南方电网有限责任公司', '中国华能集团公司',
                       '中国大唐集团公司', '中国华电集团公司', '中国国电集团公司', '国家电力投资集团公司',
                       '中国长江三峡集团公司', '神华集团有限责任公司', '中国电信集团公司', '中国联合网络通信集团有限公司',
                       '中国移动通信集团公司', '中国电子信息产业集团有限公司', '中国第一汽车集团公司', '哈尔滨电气集团公司',
                       '中国东方电气集团有限公司', '中国海运（集团）总公司', '中国航空集团公司', '中国东方航空集团公司',
                       '中国南方航空集团公司', '中国中化集团公司', '中粮集团有限公司', '中国五矿集团公司',
                       '中国通用技术（集团）控股有限责任公司', '中国建筑工程总公司', '中国储备粮管理总公司',
                       '国家开发投资公司', '招商局集团有限公司', '华润（集团）有限公司',
                       '中国港中旅集团公司[香港中旅（集团）有限公司]', '中国商用飞机有限责任公司', '中国节能环保集团公司',
                       '中国国际工程咨询公司', '中国诚通控股集团有限公司', '中国化工集团公司', '中国化学工程集团公司',
                       '中国工艺（集团）公司', '中国恒天集团公司', '中国建筑材料集团有限公司', '中国国际技术智力合作公司',
                       '中国中车集团公司 ', '中国铁路通信信号集团公司', '中国铁路工程总公司', '中国铁道建筑总公司',
                       '中国交通建设集团有限公司', '中国普天信息产业集团公司', '中国农业发展集团总公司',
                       '中国外运长航集团有限公司', '中国医药集团总公司', '中国国旅集团有限公司', '中国保利集团公司',
                       '珠海振戎公司', '新兴际华集团有限公司', '中国民航信息集团公司', '中国航空油料集团公司',
                       '中国航空器材集团公司', '中国电力建设集团有限公司', '中国能源建设集团有限公司', '中国黄金集团公司',
                       '中国储备棉管理总公司', '中国广核集团有限公司', '上海贝尔股份有限公司', '南光（集团）有限公司',
                       '中国西电集团公司', '中国铁路物资（集团）总公司', '中国国新控股有限责任公司']
GROUP_TWO_NAME_LIST = ['东风汽车公司', '中国第一重型机械集团公司', '中国机械工业集团有限公司', '鞍钢集团公司', '宝钢集团有限公司',
                       '武汉钢铁（集团）公司', '中国铝业公司', '中国远洋运输（集团）总公司', '中国中煤能源集团公司', '中国煤炭科工集团有限公司',
                       '机械科学研究总院', '中国中钢集团公司', '中国冶金科工集团有限公司', '中国钢研科技集团公司', '中国轻工集团公司',
                       '中国盐业总公司', '中国中材集团公司', '中国有色矿业集团有限公司', '北京有色金属研究总院', '北京矿冶研究总院',
                       '中国建筑科学研究院', '电信科学技术研究院', '中国中纺集团公司', '中国中丝集团公司', '中国林业集团公司',
                       '中国建筑设计研究院', '中国冶金地质总局', '中国煤炭地质总局', '中国华录集团有限公司', '武汉邮电科学研究院',
                       '华侨城集团公司']
CT_CLASS_GROUP_ONE = 'GROUP_ONE'
CT_CLASS_GROUP_TWO = 'GROUP_TWO'
CT_CLASS_SPECIAL_BANK = 'SPECIAL_BANK'
CT_CLASS_OTHER_BANK = 'OTHER_BANK'
CT_CLASS_UP_AA = 'UP_AA'
CT_CLASS_UNDER_AA = 'UNDER_AA'
"""
CSRC: 根据资产一级分类、二级分类、评级、剩余期限、担保情况确认单个资产的CSRC大类资产和资产类别
"""


def csrc_second_class_maker(first_class, second_class, term, guarantor):
    # 存款处理
    if first_class == FIRST_CLASS_DEPOSIT:
        if second_class == DEPOSIT_ASSET_TERM:
            if term < 1:
                return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_TERM_DEPOSIT_UNDER_ONE
            else:
                return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_TERM_DEPOSIT_UP_ONE
        elif second_class == DEPOSIT_ASSET_AGREEMENT:
            return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_AGREEMENT_DEPOSIT
    # 股票处理
    elif first_class == FIRST_CLASS_STOCK:
        return CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK
    # 回购
    elif first_class == FIRST_CLASS_REPO and second_class == REPO_ASSET_REVERSE:
        return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_REVERSE_REPO
    # 货币市场
    elif first_class == FIRST_CLASS_MM:
        return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_DEPOSIT
    # 基金
    elif first_class == FIRST_CLASS_FUND:
        if second_class == FUND_ASSET_STOCK:
            return CSRC_EQUITY_ASSET_SECOND_CLASS_STOCK_FUND
        elif second_class == FUND_ASSET_FIXED_PRODUCT:
            return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FI_PRODUCT
        elif second_class == FUND_ASSET_MIXED:
            return CSRC_EQUITY_ASSET_SECOND_CLASS_MIXED_FUND
        elif second_class == FUND_ASSET_CURRENCY:
            return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_MM_FUND
        elif second_class == FUND_ASSET_EQUITY_PRODUCT:
            return CSRC_EQUITY_ASSET_SECOND_CLASS_EQUITY_PRODUCT
        elif second_class == FUND_ASSET_BOND:
            return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_FUND
    # 另类
    elif first_class == FIRST_CLASS_NON_STANDARD:
        if second_class == NON_STANDARD_ASSET_ESTATE_PRODUCT:
            return CSRC_ESTATE_ASSET_SECOND_CLASS_OTHERS
        elif second_class == NON_STANDARD_ASSET_ESTATE:
            return CSRC_ESTATE_ASSET_SECOND_CLASS_ESTATE_PLAN
        elif second_class == NON_STANDARD_ASSET_STOCK:
            return CSRC_EQUITY_ASSET_SECOND_CLASS_UE_PRODUCT
        elif second_class == NON_STANDARD_ASSET_INFRASTRUCTURE:
            return CSRC_ESTATE_ASSET_SECOND_CLASS_INFRASTRUCTURE_PLAN
        elif second_class == NON_STANDARD_ASSET_TRUST:
            return CSRC_OTHER_ASSET_SECOND_CLASS_TRUST_PLAN
        elif second_class == NON_STANDARD_ASSET_OTHER:
            return CSRC_OTHER_ASSET_SECOND_CLASS_OTHER_INSURANCE_PLAN
        elif second_class == NON_STANDARD_ASSET_PROJECT:
            return CSRC_OTHER_ASSET_SECOND_CLASS_INSURANCE_PLAN
        elif second_class == NON_STANDARD_ASSET_PREFERRED:
            return CSRC_EQUITY_ASSET_SECOND_CLASS_PREFERRED
    # 债券
    elif first_class == FIRST_CLASS_BOND:
        if second_class == BOND_ASSET_CP:
            return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_CP
        if (second_class == BOND_ASSET_TREASURY) or (second_class == BOND_ASSET_BANK):
            if term < 1:
                return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_GOV_BOND_UNDER_ONE
            else:
                return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE
        elif second_class == BOND_ASSET_FINANCIAL:
            return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_FIN_BOND
        elif second_class == BOND_ASSET_CONVERT:
            return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_BOND_CONVERT
        elif second_class == BOND_ASSET_CD:
            if guarantor:
                return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_SECURED
            else:
                return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_UNSECURED
        elif second_class == BOND_ASSET_IC:
            if term < 1:
                return CSRC_LIQUIDITY_ASSET_SECOND_CLASS_IC_UNDER_ONE
            else:
                return CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_IC_UP_ONE
    else:
        return CSRC_SECOND_CLASS_UNKNOWN


def csrc_first_class_maker(second_class):
    if second_class in CSRC_LIQUIDITY_ASSET_LIST:
        return CSRC_FIRST_CLASS_LIQUIDITY_ASSET
    elif second_class in CSRC_FIXED_INCOME_ASSET_LIST:
        return CSRC_FIRST_CLASS_FIXED_INCOME_ASSET
    elif second_class in CSRC_EQUITY_ASSET_LIST:
        return CSRC_FIRST_CLASS_EQUITY_ASSET
    elif second_class in CSRC_ESTATE_ASSET_LIST:
        return CSRC_FIRST_CLASS_ESTATE_ASSET
    elif second_class in CSRC_OTHER_ASSET_LIST:
        return CSRC_FIRST_CLASS_OTHER_ASSET
    else:
        return CSRC_FIRST_CLASS_UNKNOWN


def csrc_risk_point_maker(first_class, second_class, asset_rating):
    # print(str(first_class) + "--" + str(second_class) + "--" + str(asset_rating))
    if first_class == CSRC_FIRST_CLASS_LIQUIDITY_ASSET \
            or second_class == CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_GOV_BOND_UP_ONE:
        return CSRC_RISK_POINT_LQ
    elif first_class == CSRC_FIRST_CLASS_FIXED_INCOME_ASSET \
        and second_class in [CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_SECURED,
                             CSRC_FIXED_INCOME_ASSET_SECOND_CLASS_CD_UNSECURED] \
            and (asset_rating == 'AA-' or asset_rating <= 'AA'):
        return CSRC_RISK_POINT_BOND_UNDER_AA
    elif first_class == CSRC_FIRST_CLASS_EQUITY_ASSET:
        return CSRC_RISK_POINT_EQ
    elif first_class == CSRC_FIRST_CLASS_ESTATE_ASSET:
        return CSRC_RISK_POINT_ET
    elif first_class == CSRC_FIRST_CLASS_OTHER_ASSET:
        return CSRC_RISK_POINT_OTHER


def saa_taa_risk_point_maker(circ_second_class):
    if circ_second_class in SAA_TAA_TYPE_MM_LIST:
        return SAA_TAA_TYPE_MM
    elif circ_second_class in SAA_TAA_TYPE_DEPOSIT_LIST:
        return SAA_TAA_TYPE_DEPOSIT
    elif circ_second_class in SAA_TAA_TYPE_IR_LIST:
        return SAA_TAA_TYPE_IR
    elif circ_second_class in SAA_TAA_TYPE_CR_LIST:
        return SAA_TAA_TYPE_CR
    elif circ_second_class in SAA_TAA_TYPE_EQ_LIST:
        return SAA_TAA_TYPE_EQ
    elif circ_second_class in SAA_TAA_TYPE_NON_STANDARD_LIST:
        return SAA_TAA_TYPE_NON_STANDARD


def counter_party_class_maker(ct_name, ct_rank):
    if ct_name in GROUP_ONE_NAME_LIST:
        return CT_CLASS_GROUP_ONE
    elif ct_name in GROUP_TWO_NAME_LIST:
        return CT_CLASS_GROUP_TWO
    elif ct_name in BANK_NAME_LIST:
        return CT_CLASS_SPECIAL_BANK
    elif '银行' in str(ct_name):
        return CT_CLASS_OTHER_BANK
    # TODO 没有评级默认按AA以上处理
    elif 'A' in str(ct_rank) and (ct_rank < 'AA' or ct_rank == 'AA-'):
        return CT_CLASS_UNDER_AA
    else:
        return CT_CLASS_UP_AA


def csrc_asset_class_maker(single_data):
    single_data[CSRC_ASSET_COLUMN_SECOND_CLASS] \
        = list(map(lambda x, y, z, a: csrc_second_class_maker(x, y, z, a),
                   single_data[dt.BASE_COLUMN_FIRST_CLASS],
                   single_data[dt.BASE_COLUMN_SECOND_CLASS],
                   single_data[dt.BASE_COLUMN_TERM],
                   single_data[dt.BASE_COLUMN_GUARANTOR]))
    single_data[CSRC_ASSET_COLUMN_FIRST_CLASS] = list(map(lambda x: csrc_first_class_maker(x),
                                                          single_data[CSRC_ASSET_COLUMN_SECOND_CLASS]))
    single_data[CSRC_COLUMN_RISK_POINT] \
        = list(map(lambda x, y, z: csrc_risk_point_maker(x, y, z),
                   single_data[CSRC_ASSET_COLUMN_FIRST_CLASS],
                   single_data[CSRC_ASSET_COLUMN_SECOND_CLASS],
                   single_data[dt.BASE_COLUMN_ASSET_RATING]))

    single_data[SAA_TAA_TYPE_COLUMN_NAME] \
        = list(map(lambda x: saa_taa_risk_point_maker(x),
                   single_data[CSRC_ASSET_COLUMN_SECOND_CLASS]))

    single_data[COUNTER_PARTY_CLASS_COLUMN_NAME] = list(map(lambda x, y: counter_party_class_maker(x, y),
                                                            single_data[dt.BASE_COLUMN_COUNTER_PARTY],
                                                            single_data[dt.BASE_COLUMN_COUNTER_PARTY_RANK]))
    return single_data


if __name__ == '__main__':
    rp_date = datetime.date(2017, 10, 12)
    clean_asset_data = dt.data_bowl(rp_date=rp_date)
    clean_asset_data = csrc_asset_class_maker(clean_asset_data, rp_date=rp_date)
    print(clean_asset_data[CSRC_COLUMN_RISK_POINT])
