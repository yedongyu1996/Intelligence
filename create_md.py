import os
import re

# 目标文件名前缀和后缀
prefix = "article "
suffix = ".md"

# 匹配类似 "article 29.md" 的文件
pattern = re.compile(rf"{re.escape(prefix)}(\d+){re.escape(suffix)}")

# 获取当前目录中的所有文件
files = os.listdir('.')

# 找出所有匹配的文件编号
numbers = []
for filename in files:
    match = pattern.fullmatch(filename)
    if match:
        numbers.append(int(match.group(1)))

# 计算下一个编号
next_num = max(numbers) + 1 if numbers else 1

# 新文件名
new_filename = f"{prefix}{next_num}{suffix}"

# 创建文件（内容可以自定义）
with open(new_filename, 'w', encoding='utf-8') as f:
    f.write(f" ")  # 可根据需要设置初始内容

print(f"Created: {new_filename}")