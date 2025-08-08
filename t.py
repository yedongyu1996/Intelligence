import os
import re

def md_to_txt(content):
    # 去除 Markdown 格式符号
    content = re.sub(r'(?m)^#{1,6}\s*', '', content)              # 标题
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)            # 粗体
    content = re.sub(r'\*(.*?)\*', r'\1', content)                # 斜体
    content = re.sub(r'`{1,3}(.*?)`{1,3}', r'\1', content)        # 代码
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)             # 图片
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)   # 链接
    content = re.sub(r'>\s*', '', content)                        # 引用
    content = re.sub(r'-{3,}', '', content)                       # 分隔线
    content = re.sub(r'[*\-+]\s+', '', content)                   # 无序列表
    content = re.sub(r'\d+\.\s+', '', content)                    # 有序列表
    content = re.sub(r'\n{3,}', '\n\n', content)                  # 多余空行
    return content

def convert_md_dir_to_txt_in_current():
    md_dir = os.getcwd()  # 当前路径
    txt_dir = os.path.join(md_dir, "txt")  # 当前路径下的 txt 文件夹
    os.makedirs(txt_dir, exist_ok=True)

    for root, _, files in os.walk(md_dir):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)

                # 构造相对路径并转换为 txt 路径
                rel_path = os.path.relpath(md_path, md_dir)
                txt_rel_path = os.path.splitext(rel_path)[0] + ".txt"
                txt_path = os.path.join(txt_dir, txt_rel_path)

                # 确保中间目录存在
                os.makedirs(os.path.dirname(txt_path), exist_ok=True)

                # 读取并转换内容
                with open(md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                txt_content = md_to_txt(content)

                # 写入 txt 文件
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(txt_content)

# 执行转换
convert_md_dir_to_txt_in_current()