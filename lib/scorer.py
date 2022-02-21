from rank_bm25 import BM25Okapi


class Scorer:
    data: list[str] = []

    def __init__(self, data: list[str]):
        self.data = data

    def bm25(self) -> list[dict]:
        bm25 = BM25Okapi(corpus=self.data)
        lst: list[dict[str, str | float]]

        for q in self.data:
            qscore: float = sum(bm25.get_scores(q))
            lst.append({"text": q, "score": qscore})
        return lst
