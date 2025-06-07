from haystack import indexes
from .models import Article
import jieba
from whoosh.analysis import Tokenizer, Token, StemmingAnalyzer
import re

class JiebaAndEnglishTokenizer(Tokenizer):
    """支持中文 + 英文混合分词"""
    
    def __call__(self, text, **kwargs):
        token = Token()
        words = []
        
        # 使用 jieba 分词（处理中文）
        seg_list = jieba.cut(text, cut_all=False)
        words.extend(seg_list)

        # 处理英文，按照单词分割
        english_words = []
        for word in words:
            if re.match(r'^[a-zA-Z]+$', word):  # 纯英文
                english_words.append(word)
            else:  # 中英混合，如 "Django框架"
                split_words = re.findall(r'[a-zA-Z]+|[\u4e00-\u9fa5]+', word)
                english_words.extend(split_words)

        # 为每个单词生成一个新的 Token 对象
        for pos, word in enumerate(english_words):
            t = Token()
            t.text = word.lower()
            t.boost = 1.0  # 词权重
            t.pos = pos    # 设置分词位置
            yield t

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """文章索引"""
    text = indexes.CharField(document=True, use_template=True, stored=True, analyzer=JiebaAndEnglishTokenizer())
    title = indexes.CharField(model_attr='title', stored=True, analyzer=JiebaAndEnglishTokenizer())
    content = indexes.CharField(model_attr='content', stored=True, analyzer=JiebaAndEnglishTokenizer())
    english_content = indexes.CharField(model_attr='content', stored=True, analyzer=StemmingAnalyzer())

    def get_model(self):
        return Article  # 指定模型

    def index_queryset(self, using=None):
        """获取所有数据进行索引"""
        return self.get_model().objects.all()
