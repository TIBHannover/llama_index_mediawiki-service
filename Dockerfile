FROM python:3.11

COPY src/requirements.txt /app/

WORKDIR /app

RUN pip install llama-cpp-python

RUN pip install -r requirements.txt
