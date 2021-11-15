import json
import string
from flask import Flask, request, jsonify
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
            vec = TfidfVectorizer(tokenizer=tokeniser,
                                  min_df=1, use_idf=True, stop_words=stopwords)
            corpus = text["text"].split("\n")
            vec.fit_transform(corpus)
            idf = vec.idf_
            d = {}

            for k, v in vec.vocabulary_.items():
                text = "".join(
                    [ch.strip() for ch in k.orth_ if ch not in string.punctuation])
                if text == "":
                    continue
                if text in stopwords:
                    continue
                d[k.orth_] = idf[v] + d.get(k.orth_, 0)

            # d -> array
            darr = []
            for k, v in d.items():
                darr.append({"token": k, "score": v})

            darr = sorted(darr, key=lambda x: x["score"], reverse=True)
            output.append(darr)
        return jsonify(output)
    except Exception as e:
        return json.dumps({'error': f'Error: {e}'}), 500


@app.route("/api/entity", methods=['POST'])
def entity():
    try:
        texts = request.get_json(force=True)
        output = []

        for text in texts:
            tokeniser = en if text["lang"] == "en" else zh
            tokens = tokeniser(text["text"])

            output.append([(tk.lemma_ if len(tk.lemma_) > 0 else tk.text).lower().strip(
            ) for tk in tokens.ents if not tk.text.isdecimal() and not len(tk.text.strip()) == 0])
        return json.dumps(output)
    except Exception as e:
        return json.dumps({'error': f'Error: {e}'}), 500


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000, debug=True)
