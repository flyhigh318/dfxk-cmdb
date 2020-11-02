FROM alpine:latest

COPY requiement.txt /tmp/requiement.txt

RUN apk add --no-cache python3 && \
    apk add --no-cache python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com -r /tmp/requiement.txt && \
    rm -r /root/.cache
