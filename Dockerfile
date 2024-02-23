FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update \
    # dependencies
    && apt-get install -y build-essential gettext postgresql-client netcat-traditional \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install uwsgi

COPY entrypoint.sh /entrypoint

COPY . .

ENTRYPOINT ["/entrypoint"]
