from typing import List
import jieba

class WordCutter:
    def __init__(self, word: str):
        self.word = word

    def cut(self) -> List[str]:
        return list(jieba.cut(self.word, cut_all=True))


