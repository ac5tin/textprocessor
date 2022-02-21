from flask import Flask, request, jsonify
import cld3
import spacy
from lib.scorer import Scorer


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

        return jsonify(output)
    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500


@app.route("/api/tokenise", methods=['POST'])
def tokenise():
    try:
        # todo
        texts = request.get_json(force=True)
        output = []

        for text in texts:
            lang = en if text["lang"] == "en" else zh
            darr = Scorer.tfidf(text["text"], lang)

            darr = sorted(darr, key=lambda x: x["score"], reverse=True)
            output.append(darr)
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500


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
        return jsonify(output)
    except Exception as e:
        return jsonify({'error': f'Error: {e}'}), 500


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000, debug=True)
