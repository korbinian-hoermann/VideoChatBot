FROM python:3.8.10

COPY requirements.txt  ./
COPY app/main.py ./app/
COPY app/components ./app/components/
COPY app/data ./app/data/

RUN apt update &&\
    pip install --upgrade pip &&\
    apt-get install -y cmake ffmpeg libsm6 libxext6 && \
    pip install -r requirements.txt

WORKDIR /app

CMD ["uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]