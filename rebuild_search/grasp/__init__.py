from .KeywordGrasp import GraspByKeyword

def getDateInGrasp(word: str) -> None:
    GraspByKeyword(word).start()