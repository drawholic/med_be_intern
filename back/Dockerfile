FROM python:3.10.6

WORKDIR /core

RUN python3 -m venv env

COPY ./requirements.txt /core/requirements.txt

RUN  . /core/env/bin/activate && pip install --no-cache-dir -r /core/requirements.txt

COPY . /core

CMD . /core/env/bin/activate && uvicorn app:app --port 80
