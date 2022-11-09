FROM python:3.8.10

VOLUME ["/core"]

WORKDIR /core

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
 

COPY ./requirements.txt /core/requirements.txt
 
RUN pip install --no-cache-dir -r /core/requirements.txt

COPY . /core 
EXPOSE 8000 



#CMD uvicorn app:app --host ${BACK_HOST} --port ${BACK_PORT} --reload
