FROM python:3.10.6

VOLUME ["/core"]

WORKDIR /core

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN python3 -m venv env

COPY ./requirements.txt /core/requirements.txt

#RUN /core/env/bin/pip install --no-cache-dir -r /core/requirements.txt

RUN pip install --no-cache-dir -r /core/requirements.txt

COPY . /core
#RUN alembic upgrade head
EXPOSE 8000
#CMD /core/env/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
CMD uvicorn app:app --host 0.0.0.0 --port 8000 --reload
