import json
from flask import Flask, request
import cld3
import spacy

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
            if text["lang"] == "en":
                tokens = en.tokenizer(text["text"])
                output.append(sorted([{"token": token.orth_, "score": token.rank} for token in tokens if not token.is_space and
                              not token.is_punct and len(token.orth_) >= 3 and (token.orth_ not in en.Defaults.stop_words)], key=lambda x: x["score"], reverse=True))
        return json.dumps(output)
    except Exception as e:
        return json.dumps({'error': f'Error: {e}'}), 500


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8000, debug=True)
