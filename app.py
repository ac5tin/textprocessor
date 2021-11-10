import json
from flask import Flask, request
import cld3
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

en = spacy.load("en_core_web_lg")
zh = spacy.load("zh_core_web_lg")

app = Flask(__name__)


@app.route("/api/langdet", methods=['POST'])
def langdet():
    try:
        # texts
        texts = request.get_json(force=True)
        output = []

        for text in texts:
            lang = cld3.get_language(text)
            output.append(lang.language)

        return json.dumps(output)
    except Exception as e:
        return json.dumps({'error': f'Error: {e}'}), 500


@app.route("/api/tokenise", methods=['POST'])
def tokenise():
    try:
        # todo
        texts = request.get_json(force=True)
        output = []

        for text in texts:
            tokeniser = en.tokenizer if text["lang"] == "en" else zh.tokenizer
            stopwords = en.Defaults.stop_words if text["lang"] == "en" else zh.Defaults.stop_words
            # word importance (tf-idf)
            vec = TfidfVectorizer(tokenizer=tokeniser, min_df=1, use_idf=True)
            corpus = text["text"].split("\n")
            vec.fit_transform(corpus)
            idf = vec.idf_
            d = {}

            for k, v in vec.vocabulary_.items():
                d[k.orth_] = idf[v] + d.get(k.orth_, 0)

            tokens = tokeniser(text["text"])
            # dedupe tokens
            t = {}
            tokens_uniq = []
            for token in tokens:
                if token.orth_ not in t:
                    t[token.orth_] = True
                    tokens_uniq.append(token)

            # push tokens to output
            output.append(sorted([{"token": token.orth_, "score": d[token.orth_]} for token in tokens_uniq if not token.is_space and
                                  not token.is_punct and len(token.orth_) >= (2 if text["lang"] == "zh" else 3) and (token.orth_ not in stopwords)], key=lambda x: x["score"], reverse=True))
        return json.dumps(output)
    except Exception as e:
        return json.dumps({'error': f'Error: {e}'}), 500


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000, debug=True)
