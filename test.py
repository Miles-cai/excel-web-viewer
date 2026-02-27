# test_cache.py - 测试缓存文件是否生成
print("测试Python缓存文件是否生成...")
# 可以加一行简单逻辑，确保脚本能正常运行
a = 1 + 2
print(f"简单计算结果：{a}")
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 打印环境变量，验证是否加载成功
print("是否禁用缓存：", os.getenv("PYTHONDONTWRITEBYTECODE"))
print("测试密钥：", os.getenv("TEST_KEY"))