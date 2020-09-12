FROM python:3.8
LABEL MAINTAINER = 'arezoo darvishi'
ENV PYTHONUNBUFFERED 1

RUN mkdir /django_shopper
WORKDIR /django_shopper
COPY . /django_shopper


ADD requirements.txt /shopper
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]