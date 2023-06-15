FROM python:3.11-slim-bullseye

RUN pip --no-cache-dir install -U pip setuptools wheel poetry &&  \
    rm -rf /root/.cache/pip

RUN mkdir -p /opt/shopper
WORKDIR /opt/shopper

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-cache &&  \
    rm -rf /root/.cache/pip
COPY . .