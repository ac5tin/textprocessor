FROM python:3.10

WORKDIR /app

ADD . /app

# protoc
RUN apt-get update && apt-get install -y protobuf-compiler

# python dependencies
RUN pip install pip --upgrade
RUN pip install Cython
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# spacy
RUN python -m spacy download zh_core_web_lg
RUN python -m spacy download en_core_web_lg

CMD gunicorn -w $PARA -b :$PORT app:app