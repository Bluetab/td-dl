FROM python:3.6.1-alpine3.6 as base

FROM base as builder

MAINTAINER The True-Dat Dev Team

RUN apk add --no-cache curl pkgconfig openssl-dev libffi-dev musl-dev make gcc

RUN mkdir -p /install
COPY . /install
WORKDIR /install

RUN pip install -e .

FROM base

COPY --from=builder /install /usr
COPY . /app
WORKDIR /app

CMD ["python","run.py"]
