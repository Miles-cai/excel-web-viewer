import csv
import re

def extract_data_from_csv(file_path):
    """
    解析CSV能源账单，提取燃料/用电列的数值总和
    :param file_path: CSV文件的路径（比如'./test_bill.csv'）
    :return: 字典，包含燃料总和、用电总和、匹配的列名、错误信息
    """
    # 初始化返回结果（先给默认值）
    result = {
        "fuel_total": 0.0,       # 燃料/柴油列的数值总和
        "electricity_total": 0.0,# 用电/电量列的数值总和
        "matched_fuel_cols": [], # 匹配到的燃料相关列名
        "matched_elec_cols": [], # 匹配到的用电相关列名
        "error": ""              # 错误信息（无错误则为空）
    }

    # 定义关键词规则（根据你的CSV列名调整）
    fuel_keywords = ["柴油"]  # 只保留“柴油”，去掉“燃料”
    elec_keywords = ["用电", "电量", "kwh"]

    try:
        # 打开CSV文件（解决中文乱码）
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            csv_reader = csv.DictReader(f)
            headers = csv_reader.fieldnames

            if not headers:
                result["error"] = "CSV文件没有表头列名"
                return result

            # 匹配列名
            for col_name in headers:
                clean_col = col_name.strip().lower()
                # 匹配燃料列
                for keyword in fuel_keywords:
                    if keyword.lower() in clean_col:
                        result["matched_fuel_cols"].append(col_name)
                        break
                # 匹配用电列
                for keyword in elec_keywords:
                    if keyword.lower() in clean_col:
                        result["matched_elec_cols"].append(col_name)
                        break

            # 计算数值总和
            for row in csv_reader:
                # 计算燃料列总和
                for fuel_col in result["matched_fuel_cols"]:
                    cell_value = row.get(fuel_col, "")
                    clean_value = re.sub(r'[^\d.-]', '', str(cell_value))
                    if clean_value:
                        try:
                            result["fuel_total"] += float(clean_value)
                        except ValueError:
                            pass

                # 计算用电列总和
                for elec_col in result["matched_elec_cols"]:
                    cell_value = row.get(elec_col, "")
                    clean_value = re.sub(r'[^\d.-]', '', str(cell_value))
                    if clean_value:
                        try:
                            result["electricity_total"] += float(clean_value)
                        except ValueError:
                            pass

        # 保留两位小数
        result["fuel_total"] = round(result["fuel_total"], 2)
        result["electricity_total"] = round(result["electricity_total"], 2)

    except FileNotFoundError:
        result["error"] = f"找不到文件：{file_path}"
    except Exception as e:
        result["error"] = f"解析失败：{str(e)}"

    return result

# 测试代码
if __name__ == "__main__":
    # 注意：你的CSV文件名是 test_bill.csv，这里要对应上
    csv_file_path = "./test_bill.csv"
    parse_result = extract_data_from_csv(csv_file_path)

    print("===== CSV解析结果 =====")
    if parse_result["error"]:
        print(f"错误：{parse_result['error']}")
    else:
        print(f"匹配到的燃料列：{parse_result['matched_fuel_cols']}")
        print(f"燃料列数值总和：{parse_result['fuel_total']}")
        print(f"匹配到的用电列：{parse_result['matched_elec_cols']}")
        print(f"用电列数值总和：{parse_result['electricity_total']}")