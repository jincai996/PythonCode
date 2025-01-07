import re
import time

from data import word4000
from data import color


# 获取词汇
def get_level_keys(d, level=1, times=2):
    if isinstance(d, dict):
        if level == times:
            return list(d.keys())  # 返回第三层的键
        else:
            # 递归遍历字典，增加层级
            keys = []
            for value in d.values():
                keys.extend(get_level_keys(value, level + 1))
            return keys
    return []


# 获取词汇变位
def get_level_values(d, level=1, times=3):
    if isinstance(d, dict):
        if level == times:
            return list(d.values())  # 返回第三层的值
        else:
            # 递归遍历字典，增加层级
            values = []
            for value in d.values():
                values.extend(get_level_values(value, level + 1))
            return values
    return []


# 聚合词汇和词汇变位
def get_mark_words(book):
    return get_level_keys(word4000[book]) + get_level_values(word4000[book])


def mark_article(filename):
    with open(
        file=f"/home/king/PythonCode/Atricle/input/{filename}",
        mode="r",
        encoding="utf-8",
    ) as f:
        article = f.read()

    word_list = set(article.replace("\n", "").split(" "))  # 文章分解为单词并去重复

    for book in ["BOOK1", "BOOK2", "BOOK3", "BOOK4", "BOOK5", "BOOK6"]:
        for word in word_list:  # 遍历文章词汇
            if word in get_mark_words(book):  # 与课本词汇匹配
                article = re.sub(
                    r"\b({0})\b".format(re.escape(f"{word}")),  # 全词匹配
                    f'<b style="color: {color[book]};">{word}</b>',  # 颜色标记
                    article,  # 全文替换
                )

    with open(
        file=f"/home/king/PythonCode/Atricle/output/{filename}",
        mode="a+",
        encoding="utf-8",
    ) as f:
        f.write(article)


mark_article("S01E02.md")
