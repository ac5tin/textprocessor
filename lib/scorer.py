import string
from rank_bm25 import BM25Okapi
from spacy import Language
from sklearn.feature_extraction.text import TfidfVectorizer


class Scorer:
    data: list[str] = []

    def __init__(self, tokenisedText: list[str]):
        self.data = tokenisedText

    def bm25(self) -> list[dict[str, str | float]]:
        bm25 = BM25Okapi(corpus=self.data)
        lst: list[dict[str, str | float]]

        for q in self.data:
            qscore: float = sum(bm25.get_scores(q))
            lst.append({"token": q, "score": qscore})
        return lst

    def tfidf(text: str, lang: Language) -> list[dict[str, str | float]]:
        tokeniser = lang.tokenizer
        stopwords = lang.Defaults.stop_words

        vec = TfidfVectorizer(tokenizer=tokeniser,
                              min_df=1, use_idf=True, stop_words=stopwords)
        corpus = text.split("\n")
        vec.fit_transform(corpus)
        idf = vec.idf_
        d = {}

        for k, v in vec.vocabulary_.items():
            word = "".join(
                [ch.strip() for ch in k.orth_ if ch not in string.punctuation])
            if word == "":
                continue
            if word in stopwords:
                continue

            minlen = 2
            if len(word) < minlen:
                continue
            d[word] = idf[v] + d.get(word, 0)

        # d -> array
        darr = []
        for k, v in d.items():
            darr.append({"token": k, "score": v})
        return darr
