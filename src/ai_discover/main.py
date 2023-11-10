"""
1. 输入: 用户输入config、first query
2. 初始化: config启动pipeline实例
3. 采集: 产生多个note
4. 索引: 用top n个note建立
    - 第一层:summary
    - 第二层:outline
    - 第三层:document
5. 加工: note作为输入，上下文长度和数量取决于具体情况
    - 分类
        - 不同条件分类
    - 过滤
        - 广告过滤
    - 排序
        - 评估质量
        - 热度、时效性排序
    - 关键词
        - 抽取关键词
        - 词频
    - 二次总结
    - 推荐
6. 整理
7. 互动
8. 格式化: 多目录、多链接
    - PDF
    - MD
"""
import index
from spider import bilibili

query = '仲尼'
top_n = 20


def crawl_notes(query, top_n):
    notes = bilibili.VideoSpider().get_notes(query, top_n)
    return notes


def create_index(notes):
    for note in notes:
        docs = index.split_text(note.summary.get_docs())
        index.vts.add_documents(docs)
