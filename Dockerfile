FROM python:3.9

WORKDIR /app

ADD . /app

RUN pip install pip --upgrade
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -w 4 -b :$PORT app:app