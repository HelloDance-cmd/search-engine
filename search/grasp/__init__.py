from .KeywordGrasp import GraspByKeywordNews

def getDateInGrasp(word: str, user_id: int) -> None:
    GraspByKeywordNews(word, user_id).start()