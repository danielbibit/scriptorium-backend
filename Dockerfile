FROM python:3.11

RUN apt install -y \
    git

RUN pip install poetry
