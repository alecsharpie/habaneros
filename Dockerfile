FROM python:3.8.6-buster

RUN pip install -U pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY futsal/ futsal/
COPY app.py app.py

EXPOSE $PORT

CMD streamlit run app.py --server.port $PORT
