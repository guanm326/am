"""
根据公司和监管各项监管要求，以及SAA和TAA标准，对资产数据进行收集、分析
"""
import datetime
import tools.riskArbitrator as ra
import pandas as pd


def no_risk_check():
    print("请输入持仓计算基准日期，类似 20170101: ")
    rp_date_str = input("> ")
    rp_date = datetime.datetime.strptime(rp_date_str, '%Y%m%d')

    # print("start: ", datetime.datetime.now())
    # 数据处理 -- 基础数据
    clean_asset_data = ra.ad.dt.data_bowl(rp_date=rp_date)
    clean_asset_data = ra.ad.csrc_asset_class_maker(clean_asset_data)
    # 数据处理 -- CIRC check
    csrc_risk_check_map = ra.csrc_risk_arbitrator(clean_asset_data)
    # 数据处理 -- TAA & SAA
    saa_taa_risk_check_map = ra.saa_taa_risk_arbitrator(clean_asset_data)
    # 数据处理 -- 集中度合规点
    ctr_risk_check_map = ra.concentration_risk_arbitrator(clean_asset_data)

    # 汇总判断，将RESULT为false的数据筛选出，并打印
    all_check_map = pd.concat([csrc_risk_check_map, saa_taa_risk_check_map, ctr_risk_check_map])
    false_result = all_check_map[all_check_map[ra.CSRC_RISK_POINT_RESULT]==False]
    if false_result.empty:
        print("Congratulations. No Risk.")
    else:
        print("False items:")
        print(false_result[ra.CSRC_RISK_POINT_DESP].values)

    # 数据保存
    data_map = [
        {
            ra.ad.dt.SHEET_DATA_STR: clean_asset_data,
            ra.ad.dt.SHEET_NAME_STR: ra.ad.dt.RESULT_DATA_SHEET_NAME,
            ra.ad.dt.SHEET_FIELDS_STR: ra.ad.ASSET_DETAIL_FIELDS_WITH_CSRC_CLASS
        }
        ,
        {
            ra.ad.dt.SHEET_DATA_STR: saa_taa_risk_check_map,
            ra.ad.dt.SHEET_NAME_STR: ra.ad.dt.RESULT_DATA_SAA_TAA_SHEET_NAME,
            ra.ad.dt.SHEET_FIELDS_STR: ra.SAA_TAA_RISK_POINT_FIELDS
        }
        ,
        {
            ra.ad.dt.SHEET_DATA_STR: csrc_risk_check_map,
            ra.ad.dt.SHEET_NAME_STR: ra.ad.dt.RESULT_DATA_CIRC_SHEET_NAME,
            ra.ad.dt.SHEET_FIELDS_STR: ra.CSRC_RISK_POINT_FIELDS
        }
        ,
        {
            ra.ad.dt.SHEET_DATA_STR: ctr_risk_check_map,
            ra.ad.dt.SHEET_NAME_STR: ra.ad.dt.RESULT_DATA_CTR_SHEET_NAME,
            ra.ad.dt.SHEET_FIELDS_STR: ra.CTR_RISK_POINT_FIELDS
        }
    ]
    ra.ad.dt.save_multiple_asset_data(rp_date, data_map)
    # print("end: ", datetime.datetime.now())


while True:
    try:
        no_risk_check()
    except Exception as e:
        print("oo, mistake!")
        print(e)
        error_file = "d:\\errors.txt"
        with open(error_file, 'a') as f:
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f'))
            f.write("\r\n")
            f.write("-" * 88)
            f.write(repr(e))
            f.write("\r\n")
        print("error message saved to: ", error_file)

    # no_risk_check()
    end_str = input("Continue？ y OR n : > ")
    if end_str == 'n' or end_str == 'N':
        break
