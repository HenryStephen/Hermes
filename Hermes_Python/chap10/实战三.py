import jieba
from wordcloud import WordCloud
# 读取数据
with open('华为笔记本.txt','r',encoding='utf-8') as file:
    s=file.read()
# 中文分词
lst=jieba.lcut(s)
# 排除词
stopword=['运行速度','屏幕效果','散热性能','外形外观','轻薄程度','其他特色']

txt=''.join(lst)
# 绘制词云图
wordcloud=WordCloud(background_color='white',font_path='msyh.ttc',stopwords=stopword,
                    width=800,height=600)

# 由txt生成词云图
wordcloud.generate(txt)
# 保存图片
wordcloud.to_file('华为笔记本评价词云图.png')