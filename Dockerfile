FROM python:3.9

WORKDIR /app

ADD . /app

RUN pip install pip --upgrade
RUN pip install Cython
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# spacy
RUN python -m spacy download zh_core_web_lg
RUN python -m spacy download en_core_web_lg

CMD gunicorn -w 4 -b :$PORT app:app