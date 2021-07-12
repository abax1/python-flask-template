FROM python:3.7-alpine
WORKDIR /opt/did
RUN mkdir -p /opt/did /var/log/did

RUN apk update && \
    apk add --no-cache \
        python3 \
        python3-dev \
	curl \
        linux-headers \
        libffi-dev \
        gcc \
        make \
        musl-dev \
        py-pip \
        mysql-client \
        git \
        openssl-dev \
        build-base

COPY . /opt/did

RUN pip install -r requirements.txt --no-cache-dir

RUN adduser -D -u 1001 -s /bin/sh did
RUN chown -R 1001:1001 /opt/did /var/log/did
RUN chmod +x /opt/did/docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/opt/did/docker-entrypoint.sh"]
