import pandas as pd
import numpy as np

# 马来西亚排放因子库（和你Excel里的因子库对齐）
EMISSION_FACTORS = {
    # Scope 1: 燃料燃烧
    "scope1": {
        "diesel": {
            "conversion_factor": 0.0364,  # GJ/L
            "emission_factor": 0.0717      # mt CO₂e/GJ
        }
    },
    # Scope 2: 电力（马来西亚各区域电网因子）
    "scope2": {
        "Sabah - Sabah Electricity Sdn Bhd": 0.53,  # mt CO₂e/MWh
        "Peninsular Malaysia - Tenaga Nasional Berhad": 0.48,
        "Sarawak - Sarawak Energy Berhad": 0.35
    }
}

def calculate_scope1(df):
    """
    计算 Scope 1 直接排放（柴油燃烧）
    :param df: Raw_Data 表的 DataFrame
    :return: Scope 1 总排放量（tCO₂e）
    """
    try:
        # 读取柴油消耗量（对应Excel的F8/F9）
        diesel_consumption = df.loc[7:8, 5].astype(float).sum()  # pandas索引从0开始，7=第8行，8=第9行
        
        # 计算：消耗量(L) * 转换因子(GJ/L) * 排放因子(mt CO₂e/GJ) → 转换为 tCO₂e（mt=吨，1mt=1t）
        scope1_total = diesel_consumption * EMISSION_FACTORS["scope1"]["diesel"]["conversion_factor"] * EMISSION_FACTORS["scope1"]["diesel"]["emission_factor"]
        
        return round(scope1_total, 5)
    except Exception as e:
        print(f"Scope 1 计算错误: {e}")
        return 0.0

def calculate_scope2(df):
    """
    计算 Scope 2 间接排放（电力消耗）
    :param df: Raw_Data 表的 DataFrame
    :return: Scope 2 总排放量（tCO₂e）
    """
    try:
        # 读取电力数据（对应Excel的E14-E20）
        power_data = df.loc[13:19, [3, 4]]  # D列=电网区域，E列=用电量(kWh)
        power_data.columns = ["region", "consumption"]
        power_data = power_data.dropna(subset=["region", "consumption"])
        
        scope2_total = 0.0
        for _, row in power_data.iterrows():
            region = str(row["region"]).strip()
            consumption_kwh = float(row["consumption"])
            consumption_mwh = consumption_kwh / 1000  # 转换为MWh
            
            # 匹配排放因子
            factor = EMISSION_FACTORS["scope2"].get(region, 0.0)
            scope2_total += consumption_mwh * factor
        
        return round(scope2_total, 5)
    except Exception as e:
        print(f"Scope 2 计算错误: {e}")
        return 0.0

def calculate_emission_intensity(scope1_total, scope2_total, revenue):
    """
    计算排放强度（tCO₂e/百万令吉）
    :param scope1_total: Scope 1 总排放
    :param scope2_total: Scope 2 总排放
    :param revenue: 营收（令吉）
    :return: 各维度强度
    """
    try:
        revenue_million = revenue / 1000000  # 转换为百万令吉
        if revenue_million == 0:
            return {"scope1_intensity": "-", "scope2_intensity": "-", "total_intensity": "-"}
        
        scope1_intensity = round(scope1_total / revenue_million, 5)
        scope2_intensity = round(scope2_total / revenue_million, 5)
        total_intensity = round((scope1_total + scope2_total) / revenue_million, 5)
        
        return {
            "scope1_intensity": scope1_intensity,
            "scope2_intensity": scope2_intensity,
            "total_intensity": total_intensity
        }
    except Exception as e:
        print(f"强度计算错误: {e}")
        return {"scope1_intensity": "-", "scope2_intensity": "-", "total_intensity": "-"}

def calculate_carbon_emission(file_path):
    """
    主函数：读取Excel，计算所有碳排放指标
    :param file_path: 上传的Excel文件路径
    :return: 计算结果字典
    """
    try:
        # 读取Raw_Data表
        df = pd.read_excel(file_path, sheet_name="Raw_Data", header=None)
        
        # 计算Scope 1和Scope 2
        scope1_total = calculate_scope1(df)
        scope2_total = calculate_scope2(df)
        total_emission = round(scope1_total + scope2_total, 5)
        
        # 读取营收（对应Excel的D5）
        revenue = float(df.loc[4, 3])  # 4=第5行，D列
        
        # 计算强度
        intensity = calculate_emission_intensity(scope1_total, scope2_total, revenue)
        
        # 组装结果
        result = {
            "scope1_total": scope1_total,
            "scope2_total": scope2_total,
            "total_emission": total_emission,
            "revenue": revenue,
            "intensity": intensity
        }
        
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": f"计算失败: {str(e)}"}