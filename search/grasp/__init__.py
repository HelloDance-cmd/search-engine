from .KeywordGrasp import GraspByKeywordNews
from .HotpointsGrasp import HotpotsNewGrasp

def crawl_data(word: str, user_id: int) -> None:
    GraspByKeywordNews(word, user_id).start()
    HotpotsNewGrasp().start()