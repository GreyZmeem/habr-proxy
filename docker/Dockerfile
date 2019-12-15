FROM python:3.8.0-alpine3.10

RUN apk --no-cache add \
    ca-certificates \
    curl \
    build-base \
    gcc \
    git \
    libxml2-dev \
    libxslt-dev \
    openssl \
    musl-dev
RUN curl https://raw.githubusercontent.com/kennethreitz/pipenv/master/get-pipenv.py | python

WORKDIR /app
COPY ./Pipfile ./Pipfile.lock /app/
RUN pipenv sync

COPY ./docker/entry.sh /docker-entrypoint.sh
RUN chmod +x "/docker-entrypoint.sh"
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 8080
CMD ["pipenv", "run", "./main.py"]

COPY . /app
