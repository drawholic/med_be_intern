FROM python:3.10.6

VOLUME ["/core"]

WORKDIR /core

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
<<<<<<< HEAD

COPY ./requirements.txt /core/requirements.txt


RUN pip install --no-cache-dir -r /core/requirements.txt

COPY . /core
EXPOSE 8000

=======
 

COPY ./requirements.txt /core/requirements.txt
 
RUN pip install --no-cache-dir -r /core/requirements.txt

COPY . /core 
EXPOSE 8000 
>>>>>>> 04a639c687073d67f40865003fca2da32833c769
CMD uvicorn app:app --reload
