from pathlib import Path
import re

def pack_articles_to_read(
    source_dir=".",
    out_dir="read",
    n_outputs=10,
    separator="\n=============================《文章分隔符》=============================\n",
    encoding="utf-8"
):
    """
    将当前目录下的单篇 md 文档合并为 read/ 目录下的 10 个 md 文档。
    - 仅处理文件名中包含数字编号的 .md 文件（如 article 12.md / aritcle 12.md / any 12.md）。
    - 按编号排序后，尽量平均分配到 n_outputs 份。
    - 合并时以一行 `separator` 分隔各篇内容。
    """
    src = Path(source_dir)
    dst = src / out_dir
    dst.mkdir(exist_ok=True)

    # 1) 收集候选 md 文件（排除已经在 read/ 内的）
    md_files = [p for p in src.glob("*.md") if p.is_file()]
    # 兼容子目录？题意是当前路径下，所以只取顶层 *.md 即可

    # 2) 从文件名中提取数字编号用于排序；无法提取编号的文件将被忽略
    num_pattern = re.compile(r"(\d+)")
    items = []
    for p in md_files:
        m = num_pattern.search(p.stem)
        if not m:
            continue
        idx = int(m.group(1))
        items.append((idx, p))

    # 没有可处理文件则直接返回
    if not items:
        print("未找到可处理的 md 文件（文件名需包含数字编号）。")
        return

    # 3) 按编号排序
    items.sort(key=lambda x: x[0])
    files_sorted = [p for _, p in items]

    # 4) 切成 n_outputs 个尽量均匀的块（保持原顺序）
    n = len(files_sorted)
    base = n // n_outputs
    extra = n % n_outputs  # 前 extra 份每份多 1 个
    chunks = []
    start = 0
    for i in range(n_outputs):
        size = base + (1 if i < extra else 0)
        chunks.append(files_sorted[start:start+size])
        start += size

    # 5) 写入 read/article 0..9.md
    for i, chunk in enumerate(chunks):
        out_path = dst / f"article {i}.md"
        with out_path.open("w", encoding=encoding, newline="\n") as f:
            for j, file_path in enumerate(chunk):
                content = file_path.read_text(encoding=encoding)
                f.write(content.rstrip() + "\n")
                # 仅在非最后一篇后写分隔符，文件尾部不额外加
                if j != len(chunk) - 1:
                    f.write(separator + "\n")
        # 若该份为空，也会生成空文件，保证总数为 n_outputs

    print(f"已将 {n} 篇文档合并为 {n_outputs} 个文件，输出目录：{dst.resolve()}")

if __name__ == "__main__":
    pack_articles_to_read()