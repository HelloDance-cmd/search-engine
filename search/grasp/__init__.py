from .KeywordGrasp import GraspByKeywordNews
from .HotpointsGrasp import HotpotsNewGrasp
import threading


def getDateInGrasp(word: str, user_id: int) -> None:
    GraspByKeywordNews(word, user_id).start()
    HotpotsNewGrasp().start()


threading.Timer(60 * 60 * 4, HotpotsNewGrasp().start).start()
print('开启更新')
threading.Timer(10, HotpotsNewGrasp().start).start()
