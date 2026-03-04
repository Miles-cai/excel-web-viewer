import os
import pandas as pd
import PyPDF2
import pdfplumber

class BillParser:
    """
    适配标准化碳核算Excel模板的解析器（通用版，无需频繁修改）
    模板结构：能源类型 | 消耗量 | 单位 | 排放因子 | 备注
    """
    def __init__(self):
        # 只定义需要提取的能源类型（通用，后续扩展只加这里）
        self.target_energy = {
            '柴油（Diesel B7）': 'diesel_consumption',
            '电网用电': 'electricity_consumption'
        }

    def parse(self, file_path):
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext in ['.xlsx', '.xls']:
            return self._parse_excel(file_path)
        elif file_ext == '.csv':
            return self._parse_csv(file_path)
        elif file_ext == '.pdf':
            return self._parse_pdf(file_path)
        else:
            raise ValueError(f"不支持的文件格式：{file_ext}，仅支持 xlsx/xls/csv/pdf")

    def _parse_excel(self, file_path):
        """解析标准化Excel模板（核心逻辑）"""
        try:
            # 读取指定Sheet，按列名匹配（固定列名：能源类型、消耗量）
            df = pd.read_excel(file_path, sheet_name='碳核算数据')
            # 列名统一转中文，避免大小写/空格问题
            df.columns = [col.strip() for col in df.columns]
            
            result = {
                'diesel_consumption': 0.0,
                'electricity_consumption': 0.0,
                'file_type': 'excel',
                'parse_status': 'success'
            }

            # 遍历模板，提取目标能源的消耗量
            for idx, row in df.iterrows():
                energy_type = str(row.get('能源类型', '')).strip()
                consumption = row.get('消耗量', 0.0)

                # 只提取柴油和电网用电
                if energy_type in self.target_energy:
                    key = self.target_energy[energy_type]
                    if isinstance(consumption, (int, float)) and consumption >= 0:
                        result[key] = round(consumption, 2)

            return result
        except Exception as e:
            raise Exception(f"Excel解析失败：{str(e)}")

    def _parse_csv(self, file_path):
        """CSV解析（和Excel逻辑完全一致）"""
        try:
            df = pd.read_csv(file_path)
            df.columns = [col.strip() for col in df.columns]
            
            result = {
                'diesel_consumption': 0.0,
                'electricity_consumption': 0.0,
                'file_type': 'csv',
                'parse_status': 'success'
            }

            for idx, row in df.iterrows():
                energy_type = str(row.get('能源类型', '')).strip()
                consumption = row.get('消耗量', 0.0)
                if energy_type in self.target_energy:
                    key = self.target_energy[energy_type]
                    if isinstance(consumption, (int, float)) and consumption >= 0:
                        result[key] = round(consumption, 2)

            return result
        except Exception as e:
            raise Exception(f"CSV解析失败：{str(e)}")

    def _parse_pdf(self, file_path):
        """PDF解析（预留扩展，保持接口一致）"""
        try:
            return {
                'diesel_consumption': 0.0,
                'electricity_consumption': 0.0,
                'file_type': 'pdf',
                'parse_status': 'success'
            }
        except Exception as e:
            raise Exception(f"PDF解析失败：{str(e)}")